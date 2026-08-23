#!/usr/bin/env bash
# BharatWatch — Render production start
# Seeds the DB if empty, installs Playwright browsers, then serves the FastAPI app.
set -e

echo "[render_start] seeding database if needed..."
python -m bharatwatch.cli init_db || true

# Seed rich demo data (idempotent upsert) so the API has live content
if [ -f seed_rich_data.py ]; then
  python seed_rich_data.py || echo "[render_start] seed_rich_data skipped"
fi

# Install Playwright Chromium for the direct scraper fallback
echo "[render_start] installing Playwright Chromium..."
python -m playwright install chromium --with-deps 2>/dev/null || python -m playwright install chromium 2>/dev/null || echo "[render_start] Playwright install skipped"

PORT="${PORT:-8000}"
echo "[render_start] starting uvicorn on 0.0.0.0:${PORT}"
exec python -m uvicorn bharatwatch.api.main:app --host 0.0.0.0 --port "${PORT}"
