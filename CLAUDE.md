# BharatWatch — Claude / Hermes Agent Instructions

## Project
BharatWatch is a self-healing local intelligence platform for Indian public data, built for the WeMakeDevs × Bright Data "Into the Scrape-Verse" hackathon (Aug 17–23, 2026).

## Before You Start
1. Read `docs/PRD.html`, `docs/ARCHITECTURE.html`, and `docs/PLAN.html`.
2. Check `docs/INDEX.html` for current status.
3. Verify environment: Python 3.11+, Node 20+, `gh` CLI, Bright Data credits.

## Coding Conventions
- Python: black formatting, type hints, Pydantic, SQLAlchemy.
- Frontend: Next.js App Router, Tailwind, shadcn/ui.
- Every scraper has a Pydantic schema in `bharatwatch/modules/<module>/schema.py`.
- All API calls are async with `httpx`.
- All database models use SQLAlchemy declarative base.

## Bright Data CLI
```bash
npx @@brightdata/cli bdata login
npx @@brightdata/cli bdata scraper create <url> "<description>"
npx @@brightdata/cli bdata scraper run <collector_id> <url> --pretty
npx @@brightdata/cli bdata scraper heal <collector_id> "<what changed>"
```

## Self-Healing Rule
After every scraper run, validate output against the schema. If empty/invalid, run `bdata scraper heal`, re-run, and log the event.

## Git
- Atomic commits, clear messages.
- Run `pytest` before pushing.
- Never push `.env` or tokens.

## When Stuck
- Read `docs/SCRAPER_STUDIO.html`.
- Check https://docs.brightdata.com.
- Use local static HTML mirrors for testing heals.
