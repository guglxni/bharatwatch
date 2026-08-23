#!/usr/bin/env bash
# BharatWatch — Render production start
# Seeds the DB if empty, then serves the FastAPI app on Render's $PORT.
set -e

echo "[render_start] seeding database if needed..."
python -m bharatwatch.cli init_db || true

# Seed rich demo data (idempotent upsert) so the API has live content
if [ -f seed_rich_data.py ]; then
  python seed_rich_data.py || echo "[render_start] seed_rich_data skipped"
fi

PORT="${PORT:-8000}"
echo "[render_start] starting uvicorn on 0.0.0.0:${PORT}"
exec python -m uvicorn bharatwatch.api.main:app --host 0.0.0.0 --port "${PORT}"
