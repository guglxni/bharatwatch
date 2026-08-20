import os
import json
import hashlib
import httpx
from datetime import datetime
from typing import List, Dict, Any
from bharatwatch.core.config import BRIGHT_DATA_API_TOKEN, BRIGHT_DATA_COLLECTOR_BASE_URL
from bharatwatch.core.database import SessionLocal
from bharatwatch.core.models import Source, Snapshot, Change, HealEvent
from bharatwatch.core.diff_engine import compute_diff, compute_hash
from bharatwatch.core.schema_registry import validate_items
from bharatwatch.modules.nauktrialert.schema import NaukriAlertItem

NAUKRI_KEY_FIELDS = ["title", "department"]

def trigger_collector(collector_id: str, url: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {BRIGHT_DATA_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"collector_id": collector_id, "url": url}
    resp = httpx.post(BRIGHT_DATA_COLLECTOR_BASE_URL, headers=headers, json=payload, timeout=120.0)
    resp.raise_for_status()
    return resp.json()

def parse_naukri_output(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # common wrapper shapes
        for k in ["recruitment_notices", "notices", "jobs", "results", "data"]:
            if k in data and isinstance(data[k], list):
                return data[k]
    return []

def run_source(source: Source, db) -> Dict[str, Any]:
    result = {"success": False, "items": [], "error": None}
    try:
        data = trigger_collector(source.collector_id, source.url)
        items = parse_naukri_output(data)
        if items:
            sample = NaukriAlertItem.model_json_schema().get("properties", {})
            ok, valid = validate_items(items, sample)
            if ok:
                result["success"] = True
                result["items"] = valid
                snapshot_hash = compute_hash(valid)
                snapshot = Snapshot(source_id=source.id, raw_json=valid, hash=snapshot_hash, status="ok")
                db.add(snapshot)
                db.commit()

                # diff
                last = db.query(Snapshot).filter_by(source_id=source.id).order_by(Snapshot.captured_at.desc()).offset(1).first()
                if last:
                    changes = compute_diff(last.raw_json, valid, NAUKRI_KEY_FIELDS)
                    for c in changes:
                        db.add(Change(source_id=source.id, change_type=c["change_type"], before=c["before"], after=c["after"]))
                    db.commit()

                source.health = "healthy"
            else:
                result["error"] = "schema validation failed"
                source.health = "broken"
        else:
            result["error"] = "empty output"
            source.health = "broken"
    except Exception as e:
        result["error"] = str(e)
        source.health = "broken"
    source.last_run_at = datetime.utcnow()
    db.commit()
    return result

def run_all():
    db = SessionLocal()
    try:
        sources = db.query(Source).all()
        for s in sources:
            print(f"Running {s.name} ({s.collector_id})...")
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
