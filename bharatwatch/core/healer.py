import subprocess
from datetime import datetime
from bharatwatch.core.database import SessionLocal
from bharatwatch.core.models import Source, HealEvent

def heal_source(source_id: int, description: str) -> dict:
    db = SessionLocal()
    try:
        source = db.query(Source).get(source_id)
        if not source:
            return {"success": False, "error": "source not found"}
        cmd = [
            "npx", "@brightdata/cli", "scraper", "heal",
            source.collector_id, description
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        success = proc.returncode == 0 and "awaiting_approval" in proc.stdout
        event = HealEvent(
            source_id=source_id,
            description=description,
            success="true" if success else "false",
            response_text=proc.stdout + proc.stderr
        )
        db.add(event)
        db.commit()
        return {"success": success, "output": proc.stdout, "error": proc.stderr}
    finally:
        db.close()

def heal_monitor():
    db = SessionLocal()
    try:
        sources = db.query(Source).filter(Source.health.in_(["broken", "unknown"])).all()
        for s in sources:
            print(f"Healing {s.name}...")
            desc = f"The page layout may have changed. Re-extract the same fields from {s.url}."
            heal_source(s.id, desc)
    finally:
        db.close()
