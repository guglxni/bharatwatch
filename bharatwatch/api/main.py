from datetime import datetime, timedelta
from collections import defaultdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func

from bharatwatch.core.database import SessionLocal, init_db
from bharatwatch.core.models import Source, Snapshot, Change, HealEvent

app = FastAPI(title="BharatWatch API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
init_db()

MODULE_META = {
    "nauktrialert": {
        "label": "NaukriAlert",
        "tagline": "Govt job notifications, the moment they drop",
        "icon": "🔔",
        "accent": "from-orange-500 to-amber-500",
        "source_name": "Indeed.com — Government Jobs India",
    },
    "tendersentry": {
        "label": "TenderSentry",
        "tagline": "Every government tender, tracked & priced",
        "icon": "📄",
        "accent": "from-blue-500 to-cyan-500",
        "source_name": "GeM + CPPP e-procurement",
    },
    "mandiwatch": {
        "label": "MandiWatch",
        "tagline": "Mandi prices across India, daily",
        "icon": "🌾",
        "accent": "from-green-500 to-emerald-500",
        "source_name": "Agmarknet price boards",
    },
    "collegecutoff": {
        "label": "CollegeCutoff",
        "tagline": "JoSAA cutoff ranks, round by round",
        "icon": "🎓",
        "accent": "from-violet-500 to-purple-500",
        "source_name": "JoSAA counselling boards",
    },
    "startuppulse": {
        "label": "StartupPulse",
        "tagline": "Schemes & grants for Indian startups",
        "icon": "🚀",
        "accent": "from-pink-500 to-rose-500",
        "source_name": "GKToday.in + Startup India portals",
    },
}


def _latest_snapshot(db, source_id):
    return (
        db.query(Snapshot)
        .filter_by(source_id=source_id)
        .order_by(Snapshot.captured_at.desc())
        .first()
    )


@app.get("/api/v1/health")
def health():
    db = SessionLocal()
    try:
        total = db.query(Source).count()
        healthy = db.query(Source).filter_by(health="healthy").count()
        return {"status": "ok", "sources": total, "healthy": healthy}
    finally:
        db.close()


@app.get("/api/v1/modules")
def modules():
    db = SessionLocal()
    try:
        rows = db.query(Source.module).distinct().all()
        out = []
        for (module,) in rows:
            meta = MODULE_META.get(module, {})
            src = db.query(Source).filter_by(module=module).first()
            snap = _latest_snapshot(db, src.id) if src else None
            changes = db.query(Change).filter(
                Change.source_id == src.id,
                Change.detected_at >= datetime.utcnow() - timedelta(days=7),
            ).count()
            out.append({
                "id": module,
                "label": meta.get("label", module),
                "tagline": meta.get("tagline", ""),
                "icon": meta.get("icon", ""),
                "accent": meta.get("accent", ""),
                "source_name": meta.get("source_name", ""),
                "source_url": src.url if src else "",
                "collector_id": src.collector_id if src else None,
                "health": src.health if src else "unknown",
                "item_count": len(snap.raw_json) if snap and isinstance(snap.raw_json, list) else 0,
                "changes_7d": changes,
                "last_run_at": src.last_run_at,
            })
        return {"modules": out}
    finally:
        db.close()


@app.get("/api/v1/overview")
def overview():
    """Aggregate stats for the dashboard overview page."""
    db = SessionLocal()
    try:
        sources = db.query(Source).all()
        total_items = 0
        total_changes_7d = 0
        per_module = []
        activity_by_day = defaultdict(int)

        for s in sources:
            snap = _latest_snapshot(db, s.id)
            n_items = len(snap.raw_json) if snap and isinstance(snap.raw_json, list) else 0
            total_items += n_items
            rows = db.query(Change.detected_at, Change.change_type).filter(
                Change.source_id == s.id,
                Change.detected_at >= datetime.utcnow() - timedelta(days=7),
            ).all()
            total_changes_7d += len(rows)
            for (ts, _ct) in rows:
                activity_by_day[ts.strftime("%Y-%m-%d")] += 1

            # sparkline: item count per snapshot
            snaps = (
                db.query(Snapshot.captured_at, Snapshot.raw_json)
                .filter_by(source_id=s.id)
                .order_by(Snapshot.captured_at.asc())
                .all()
            )
            sparkline = [
                {"t": cap.strftime("%Y-%m-%d"), "v": len(raw) if isinstance(raw, list) else 0}
                for (cap, raw) in snaps
            ]
            per_module.append({
                "id": s.module,
                "label": MODULE_META.get(s.module, {}).get("label", s.module),
                "icon": MODULE_META.get(s.module, {}).get("icon", ""),
                "accent": MODULE_META.get(s.module, {}).get("accent", ""),
                "health": s.health,
                "item_count": n_items,
                "changes_7d": len(rows),
                "sparkline": sparkline,
                "collector_id": s.collector_id,
                "last_run_at": s.last_run_at,
            })

        # fill missing days
        series = []
        for i in range(6, -1, -1):
            day = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
            series.append({"date": day, "changes": activity_by_day.get(day, 0)})

        heal_count = db.query(HealEvent).count()
        heal_success = db.query(HealEvent).filter_by(success="true").count()

        return {
            "sources": len(sources),
            "healthy": sum(1 for s in sources if s.health == "healthy"),
            "total_items": total_items,
            "total_changes_7d": total_changes_7d,
            "heal_events": heal_count,
            "heal_success": heal_success,
            "activity_series": series,
            "modules": per_module,
        }
    finally:
        db.close()


@app.get("/api/v1/{module}/sources")
def sources(module: str):
    db = SessionLocal()
    try:
        rows = db.query(Source).filter_by(module=module).all()
        return [{"id": s.id, "name": s.name, "url": s.url, "health": s.health,
                 "collector_id": s.collector_id, "last_run_at": s.last_run_at} for s in rows]
    finally:
        db.close()


@app.get("/api/v1/{module}/data")
def module_data(module: str):
    """Live extracted data: latest snapshot for every source of the module."""
    db = SessionLocal()
    try:
        src = db.query(Source).filter_by(module=module).first()
        if not src:
            return {"module": module, "items": [], "captured_at": None}
        snap = _latest_snapshot(db, src.id)
        return {
            "module": module,
            "meta": MODULE_META.get(module, {}),
            "source": {"name": src.name, "url": src.url, "collector_id": src.collector_id,
                       "health": src.health, "last_run_at": src.last_run_at},
            "items": snap.raw_json if snap else [],
            "captured_at": snap.captured_at if snap else None,
        }
    finally:
        db.close()


@app.get("/api/v1/{module}/history")
def module_history(module: str):
    db = SessionLocal()
    try:
        src = db.query(Source).filter_by(module=module).first()
        if not src:
            return {"history": [], "changes": []}
        snaps = (
            db.query(Snapshot)
            .filter_by(source_id=src.id)
            .order_by(Snapshot.captured_at.asc())
            .all()
        )
        history = [
            {"t": s.captured_at.strftime("%Y-%m-%d %H:%M"), "items": len(s.raw_json) if isinstance(s.raw_json, list) else 0,
             "status": s.status}
            for s in snaps
        ]
        changes = (
            db.query(Change)
            .filter_by(source_id=src.id)
            .order_by(Change.detected_at.desc())
            .limit(30)
            .all()
        )
        change_list = [
            {"id": c.id, "change_type": c.change_type, "before": c.before, "after": c.after,
             "detected_at": c.detected_at}
            for c in changes
        ]
        return {"history": history, "changes": change_list}
    finally:
        db.close()


@app.get("/api/v1/{module}/changes")
def changes(module: str, limit: int = 50):
    db = SessionLocal()
    try:
        source_ids = [s.id for s in db.query(Source).filter_by(module=module).all()]
        rows = (
            db.query(Change)
            .filter(Change.source_id.in_(source_ids))
            .order_by(Change.detected_at.desc())
            .limit(limit)
            .all()
        )
        return [{"id": c.id, "change_type": c.change_type, "before": c.before, "after": c.after,
                 "detected_at": c.detected_at} for c in rows]
    finally:
        db.close()


@app.get("/api/v1/heal-events")
def heal_events(limit: int = 50):
    db = SessionLocal()
    try:
        rows = db.query(HealEvent).order_by(HealEvent.created_at.desc()).limit(limit).all()
        sources_by_id = {s.id: s.module for s in db.query(Source).all()}
        return [{"id": h.id, "source_id": h.source_id,
                 "module": sources_by_id.get(h.source_id, ""),
                 "module_label": MODULE_META.get(sources_by_id.get(h.source_id, ""), {}).get("label", ""),
                 "icon": MODULE_META.get(sources_by_id.get(h.source_id, ""), {}).get("icon", ""),
                 "description": h.description, "success": h.success, "created_at": h.created_at}
                for h in rows]
    finally:
        db.close()
