from fastapi import FastAPI
from bharatwatch.core.database import SessionLocal, init_db
from bharatwatch.core.models import Source, Snapshot, Change, HealEvent

app = FastAPI(title="BharatWatch API", version="0.1.0")
init_db()

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
        return {"modules": [r[0] for r in rows]}
    finally:
        db.close()

@app.get("/api/v1/{module}/sources")
def sources(module: str):
    db = SessionLocal()
    try:
        rows = db.query(Source).filter_by(module=module).all()
        return [{"id": s.id, "name": s.name, "url": s.url, "health": s.health, "last_run_at": s.last_run_at} for s in rows]
    finally:
        db.close()

@app.get("/api/v1/{module}/changes")
def changes(module: str, limit: int = 50):
    db = SessionLocal()
    try:
        source_ids = [s.id for s in db.query(Source).filter_by(module=module).all()]
        rows = db.query(Change).filter(Change.source_id.in_(source_ids)).order_by(Change.detected_at.desc()).limit(limit).all()
        return [{"id": c.id, "change_type": c.change_type, "before": c.before, "after": c.after, "detected_at": c.detected_at} for c in rows]
    finally:
        db.close()

@app.get("/api/v1/heal-events")
def heal_events(limit: int = 50):
    db = SessionLocal()
    try:
        rows = db.query(HealEvent).order_by(HealEvent.created_at.desc()).limit(limit).all()
        return [{"id": h.id, "source_id": h.source_id, "description": h.description, "success": h.success, "created_at": h.created_at} for h in rows]
    finally:
        db.close()
