import os
import json
import hashlib
import httpx
import importlib
from datetime import datetime
from typing import List, Dict, Any
from bharatwatch.core.config import BRIGHT_DATA_API_TOKEN, BRIGHT_DATA_COLLECTOR_BASE_URL
from bharatwatch.core.database import SessionLocal
from bharatwatch.core.models import Source, Snapshot, Change, HealEvent
from bharatwatch.core.diff_engine import compute_diff, compute_hash
from bharatwatch.core.schema_registry import validate_items

MODULE_KEY_FIELDS = {
    "nauktrialert": ["title", "department"],
    "tendersentry": ["tender_id", "title"],
    "mandiwatch": ["mandi", "crop", "variety"],
    "collegecutoff": ["institute", "branch", "round"],
    "startuppulse": ["title", "ministry"],
}

def flatten_value(v: Any) -> Any:
    if isinstance(v, dict):
        if "value" in v:
            return v["value"]
        # If it's a dict with one string value, return that
        if len(v) == 1 and isinstance(list(v.values())[0], str):
            return list(v.values())[0]
    return v

def flatten_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {k: flatten_value(v) for k, v in item.items()}

def load_module_schema(module: str) -> type:
    try:
        mod = importlib.import_module(f"bharatwatch.modules.{module}.schema")
        for name in dir(mod):
            if name.endswith("Item") and name != "BaseModel":
                return getattr(mod, name)
    except Exception as e:
        print(f"Could not load schema for {module}: {e}")
    return None

def trigger_collector(collector_id: str, url: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {BRIGHT_DATA_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"collector_id": collector_id, "url": url}
    resp = httpx.post(BRIGHT_DATA_COLLECTOR_BASE_URL, headers=headers, json=payload, timeout=120.0)
    resp.raise_for_status()
    return resp.json()

def parse_output(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        if len(data) == 1 and isinstance(data[0], dict):
            # Find the first list inside the dict
            for v in data[0].values():
                if isinstance(v, list):
                    return v
        return data
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list):
                return v
    return []

def run_source(source: Source, db, auto_heal: bool = True) -> Dict[str, Any]:
    result = {"success": False, "items": [], "error": None}
    schema = load_module_schema(source.module)
    try:
        data = trigger_collector(source.collector_id, source.url)
        items = parse_output(data)
        items = [flatten_item(item) for item in items]
        if items and schema:
            sample = schema.model_json_schema().get("properties", {})
            ok, valid = validate_items(items, sample)
            if ok:
                result["success"] = True
                result["items"] = valid
                snapshot_hash = compute_hash(valid)
                snapshot = Snapshot(source_id=source.id, raw_json=valid, hash=snapshot_hash, status="ok")
                db.add(snapshot)
                db.commit()

                last = db.query(Snapshot).filter_by(source_id=source.id).order_by(Snapshot.captured_at.desc()).offset(1).first()
                if last:
                    key_fields = MODULE_KEY_FIELDS.get(source.module, ["title"])
                    changes = compute_diff(last.raw_json, valid, key_fields)
                    for c in changes:
                        db.add(Change(source_id=source.id, change_type=c["change_type"], before=c["before"], after=c["after"]))
                    db.commit()

                source.health = "healthy"
            else:
                result["error"] = "schema validation failed"
                source.health = "broken"
        elif not items:
            result["error"] = "empty output"
            source.health = "broken"
        else:
            result["error"] = "no schema loaded"
            source.health = "broken"
    except Exception as e:
        result["error"] = str(e)
        source.health = "broken"

    # ── Layer 2: Bright Data Web Unlocker Direct API fallback ──
    if not result["success"]:
        try:
            from bharatwatch.core.direct_scraper import scrape_with_brightdata_unlocker
            from bharatwatch.core.site_extractors import get_site_extractor
            # Try the source URL first, then fallback site URLs
            unlocker_urls = [source.url]
            for site_url, _ in get_site_extractor(source.module):
                if site_url not in unlocker_urls:
                    unlocker_urls.append(site_url)
            for try_url in unlocker_urls:
                unlocker_result = scrape_with_brightdata_unlocker(try_url, source.module)
                if unlocker_result["ok"] and unlocker_result["items"]:
                    items = unlocker_result["items"]
                    result["items"] = items
                    result["success"] = True
                    result["error"] = None
                    result["fallback"] = "brightdata_unlocker"
                    result["unlocker_url"] = try_url
                    snapshot_hash = compute_hash(items)
                    snapshot = Snapshot(source_id=source.id, raw_json=items, hash=snapshot_hash, status="ok")
                    db.add(snapshot)
                    db.commit()
                    last = db.query(Snapshot).filter_by(source_id=source.id).order_by(Snapshot.captured_at.desc()).offset(1).first()
                    if last:
                        key_fields = MODULE_KEY_FIELDS.get(source.module, ["title"])
                        changes = compute_diff(last.raw_json, items, key_fields)
                        for c in changes:
                            db.add(Change(source_id=source.id, change_type=c["change_type"], before=c["before"], after=c["after"]))
                        db.commit()
                    source.health = "healthy"
                    break
        except Exception as ue:
            result["unlocker_error"] = str(ue)

    # ── Layer 3: Playwright + Stealth fallback ──
    if not result["success"]:
        try:
            from bharatwatch.core.direct_scraper import scrape_with_playwright
            from bharatwatch.core.site_extractors import get_site_extractor
            # Use the primary site URL for this module
            sites = get_site_extractor(source.module)
            fallback_url = sites[0][0] if sites else source.url
            pw_result = scrape_with_playwright(fallback_url, source.module)
            if pw_result["ok"] and pw_result["items"]:
                items = pw_result["items"]
                result["items"] = items
                result["success"] = True
                result["error"] = None
                result["fallback"] = "playwright"
                snapshot_hash = compute_hash(items)
                snapshot = Snapshot(source_id=source.id, raw_json=items, hash=snapshot_hash, status="ok")
                db.add(snapshot)
                db.commit()
                last = db.query(Snapshot).filter_by(source_id=source.id).order_by(Snapshot.captured_at.desc()).offset(1).first()
                if last:
                    key_fields = MODULE_KEY_FIELDS.get(source.module, ["title"])
                    changes = compute_diff(last.raw_json, items, key_fields)
                    for c in changes:
                        db.add(Change(source_id=source.id, change_type=c["change_type"], before=c["before"], after=c["after"]))
                    db.commit()
                source.health = "healthy"
        except Exception as fe:
            result["fallback_error"] = str(fe)

    source.last_run_at = datetime.utcnow()
    db.commit()

    # Closed loop: a broken run triggers an immediate self-heal attempt.
    if not result["success"] and auto_heal:
        try:
            from bharatwatch.core.healer import heal_source_with_retries
            heal = heal_source_with_retries(source.id)
            result["heal"] = heal
            if heal.get("success"):
                source.health = "healthy"
                db.commit()
                result["recovered"] = True
        except Exception as he:  # healing must never crash the run
            result["heal_error"] = str(he)
    return result

def run_all():
    db = SessionLocal()
    try:
        sources = db.query(Source).all()
        for s in sources:
            print(f"Running {s.module}/{s.name} ({s.collector_id})...")
            res = run_source(s, db)
            print(f"  -> {res['success']}, items={len(res['items'])}, error={res.get('error')}")
    finally:
        db.close()

def run_module(module: str):
    db = SessionLocal()
    try:
        sources = db.query(Source).filter_by(module=module).all()
        for s in sources:
            print(f"Running {s.name}...")
            res = run_source(s, db)
            print(f"  -> {res['success']}, items={len(res['items'])}, error={res.get('error')}")
    finally:
        db.close()
