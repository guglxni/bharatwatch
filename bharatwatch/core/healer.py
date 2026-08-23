"""BharatWatch self-healing engine.

Closed-loop: detect breakage -> build a context-aware prompt -> heal ->
auto-approve + auto-save -> re-run the collector -> validate real data came back.

The Bright Data CLI (`@brightdata/cli`) does the heavy lifting:
  scraper heal <collector_id> <prompt> --auto-approve --auto-save --json
returns a JSON envelope with a `status` field ("done", "awaiting_approval",
"failed", ...) that we parse to decide next steps.
"""
import json
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from bharatwatch.core.database import SessionLocal
from bharatwatch.core.models import Source, Snapshot, HealEvent

HEAL_TIMEOUT = 600        # seconds to let the AI heal job run
RUN_TIMEOUT = 600         # seconds to let a verification scrape run
MAX_HEAL_ATTEMPTS = 3     # fallback-strategy retries before escalating


# --------------------------------------------------------------------------- #
# Bright Data CLI wrappers
# --------------------------------------------------------------------------- #
def _run_cli(args: List[str], timeout: int) -> Tuple[bool, Dict[str, Any], str]:
    """Run the Bright Data CLI with --json and parse the envelope.

    Returns (ok, parsed_json_or_empty, raw_text).
    """
    cmd = ["npx", "@brightdata/cli"] + args + ["--json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, {}, f"cli timeout after {timeout}s"
    raw = (proc.stdout or "") + "\n" + (proc.stderr or "")
    parsed: Dict[str, Any] = {}
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                parsed = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
    ok = proc.returncode == 0
    return ok, parsed, raw


def heal_collector(collector_id: str, prompt: str, url: Optional[str] = None) -> Dict[str, Any]:
    """Heal a collector with auto-approve + auto-save (fully closed loop)."""
    args = ["scraper", "heal", collector_id, prompt, "--auto-approve", "--auto-save",
            "--timeout", str(HEAL_TIMEOUT)]
    if url:
        args += ["--url", url]
    ok, parsed, raw = _run_cli(args, HEAL_TIMEOUT + 30)
    status = parsed.get("status") or ("done" if ok and not parsed else "failed")
    return {"ok": ok and status in ("done", "completed", "success"),
            "status": status, "raw": raw, "parsed": parsed}


def run_collector(collector_id: str, url: str) -> Dict[str, Any]:
    """Re-run a collector and return parsed items (verification step)."""
    ok, parsed, raw = _run_cli(["scraper", "run", collector_id, url], RUN_TIMEOUT + 30)
    items: List[Dict[str, Any]] = []
    data = parsed.get("data") or parsed.get("results") or parsed.get("output") or parsed
    if isinstance(data, list):
        items = [x for x in data if isinstance(x, dict)]
    elif isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                items = [x for x in v if isinstance(x, dict)]
                break
    return {"ok": ok, "items": items, "count": len(items), "raw": raw}


# --------------------------------------------------------------------------- #
# Context-aware prompt building (from the last GOOD snapshot)
# --------------------------------------------------------------------------- #
def build_heal_prompt(source: Source, db, last_error: Optional[str] = None) -> str:
    last_good = (
        db.query(Snapshot)
        .filter_by(source_id=source.id, status="ok")
        .order_by(Snapshot.captured_at.desc())
        .first()
    )
    fields: List[str] = []
    if last_good and isinstance(last_good.raw_json, list) and last_good.raw_json:
        fields = sorted(last_good.raw_json[0].keys())
    field_hint = (" Expected fields: " + ", ".join(fields) + ".") if fields else ""
    err_hint = f" Previous failure: {last_error}." if last_error else ""
    prompt = (
        f"The page at {source.url} changed layout and extraction is failing.{err_hint}"
        f" Re-extract the SAME data as before from the CURRENT page structure.{field_hint}"
        " The page may have moved from a table to cards/list (or vice-versa);"
        " locate the equivalent containers and re-map selectors accordingly."
    )
    return prompt[:1000]  # CLI caps the prompt at 1000 chars


# --------------------------------------------------------------------------- #
# Core closed-loop heal
# --------------------------------------------------------------------------- #
def heal_source(source_id: int, description: Optional[str] = None,
                auto_validate: bool = True) -> Dict[str, Any]:
    """Full closed-loop heal for one source. Always recorded in heal_events."""
    db = SessionLocal()
    try:
        source = db.query(Source).get(source_id)
        if not source:
            return {"success": False, "error": "source not found"}

        prompt = description or build_heal_prompt(source, db)
        result: Dict[str, Any] = {"source_id": source_id, "module": source.module,
                                  "prompt": prompt, "healed": False,
                                  "validated": False, "recovered_items": 0}

        heal = heal_collector(source.collector_id, prompt, source.url)
        result["heal_status"] = heal["status"]
        result["healed"] = heal["ok"]

        # Verify by re-running the collector and confirming real data returns.
        if heal["ok"] and auto_validate:
            run = run_collector(source.collector_id, source.url)
            result["recovered_items"] = run["count"]
            if run["ok"] and run["count"] > 0:
                result["validated"] = True
                source.health = "healthy"
                source.last_run_at = datetime.utcnow()
            else:
                source.health = "broken"
        elif not heal["ok"]:
            source.health = "broken"

        result["success"] = bool(result["healed"] and (result["validated"] or not auto_validate))

        event = HealEvent(
            source_id=source_id,
            description=prompt,
            success="true" if result["success"] else "false",
            response_text=json.dumps(
                {k: v for k, v in result.items() if k not in ("prompt",)}, default=str
            )[:4000],
        )
        db.add(event)
        db.commit()
        return result
    finally:
        db.close()


def heal_source_with_retries(source_id: int, max_attempts: int = MAX_HEAL_ATTEMPTS) -> Dict[str, Any]:
    """Retry the heal loop with progressively more specific prompts."""
    last: Dict[str, Any] = {"success": False}
    for attempt in range(1, max_attempts + 1):
        db = SessionLocal()
        try:
            source = db.query(Source).get(source_id)
            if not source:
                return {"success": False, "error": "source not found"}
            err = last.get("heal_status") if attempt > 1 else None
            prompt = build_heal_prompt(source, db, last_error=err)
        finally:
            db.close()
        last = heal_source(source_id, description=prompt)
        if last.get("success"):
            last["attempts"] = attempt
            return last
    last["attempts"] = max_attempts
    last["escalate"] = True   # all strategies failed -> human review
    return last


def heal_monitor(auto_approve: bool = True, retries: bool = True) -> List[Dict[str, Any]]:
    """Scan for broken/unknown sources and heal each one, closed-loop."""
    db = SessionLocal()
    try:
        sources = db.query(Source).filter(Source.health.in_(["broken", "unknown"])).all()
        ids = [s.id for s in sources]
    finally:
        db.close()

    results = []
    for sid in ids:
        print(f"[heal_monitor] healing source {sid}...")
        res = (heal_source_with_retries(sid) if retries else heal_source(sid))
        results.append(res)
        status = "OK" if res.get("success") else ("ESCALATE" if res.get("escalate") else "FAILED")
        print(f"[heal_monitor] source {sid}: {status} "
              f"(healed={res.get('healed')}, validated={res.get('validated')}, "
              f"recovered={res.get('recovered_items', 0)})")
    return results
