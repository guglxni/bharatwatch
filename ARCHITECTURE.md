# BharatWatch Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Vercel (Next.js Dashboard)               │
│  Landing · Mission Control · Module Pages · Heal Feed       │
└──────────────────────────┬──────────────────────────────────┘
                           │ /api/* proxy
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Render (FastAPI Backend)                  │
│  Overview · Modules · Data · History · Heal Events          │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator (3-layer)                    │
│                                                              │
│  Layer 1: Bright Data Scraper Studio                        │
│    └─ scraper run <collector_id> <url> --json               │
│       Fails? (403 tunneling / domain not allowed)           │
│                                                              │
│  Layer 2: Bright Data Web Unlocker Direct API               │
│    └─ POST api.brightdata.com/request {zone, url, format}   │
│       Fails? (empty / blocked)                              │
│                                                              │
│  Layer 3: Playwright + Stealth (headless Chromium)          │
│    └─ Site-specific CSS extractors                           │
│       Fails? → Trigger self-heal loop                       │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Self-Healing Engine                       │
│                                                              │
│  1. Detect breakage (empty output / schema mismatch)        │
│  2. Build context-aware prompt (from last good snapshot)    │
│  3. scraper heal --auto-approve --auto-save                  │
│  4. Re-run collector + validate real data returned           │
│  5. Mark healthy ✓ or retry 3× → escalate                   │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Storage                            │
│  sources · snapshots · changes · heal_events                │
│  Diff engine: field-level created/updated/deleted           │
└─────────────────────────────────────────────────────────────┘
```

## Bright Data Platform Usage

BharatWatch uses three Bright Data products:

### 1. Scraper Studio (`@brightdata/cli`)
- **`scraper create`** — AI generates extraction code from a natural-language description
- **`scraper run`** — executes the collector against a target URL, returns structured JSON
- **`scraper heal --auto-approve --auto-save`** — AI regenerates extraction code when the site changes, applied and saved automatically

Collector lifecycle:
```
Create → Run → (fails) → Heal → Auto-approve → Auto-save → Re-run → Validate
```

### 2. Web Unlocker Direct API
- REST endpoint at `https://api.brightdata.com/request`
- Bypasses the proxy tunnel layer that causes 403 "tunneling socket" errors
- 98% success rate for fetching raw HTML from any URL
- Used as Layer 2 fallback when Scraper Studio's proxy fails

### 3. Scraping Browser (available, not yet wired)
- Cloud-hosted Chrome via Playwright CDP WebSocket
- For JS-rendered pages that need full browser execution
- Future enhancement for tender/mandi portals with dynamic content

## Data Flow

```
1. Orchestrator triggers run_source(source, db)
2. Tries Bright Data collector (Layer 1)
3. If 403/empty → tries Web Unlocker API (Layer 2)
4. If still failing → tries Playwright stealth (Layer 3)
5. Items validated against Pydantic schema
6. Snapshot stored with content hash
7. Diff engine compares to previous snapshot
8. Changes (created/updated/deleted) recorded
9. Source health updated (healthy/broken)
10. If broken → self-heal loop triggered
```

## Self-Healing Details

The heal prompt is **context-aware** — it reads the last successful snapshot to know exactly which fields to extract:

```python
def build_heal_prompt(source, db, last_error=None):
    last_good = db.query(Snapshot).filter_by(
        source_id=source.id, status="ok"
    ).order_by(Snapshot.captured_at.desc()).first()

    fields = sorted(last_good.raw_json[0].keys()) if last_good else []
    field_hint = f"Expected fields: {', '.join(fields)}." if fields else ""
    err_hint = f"Previous failure: {last_error}." if last_error else ""

    return f"The page at {source.url} changed layout. {err_hint} Re-extract: {field_hint}"
```

This means the AI heal gets told: "The page changed. Last time we got these 8 fields: title, department, vacancies... Re-extract them from the new layout."

## Deployment Architecture

```
GitHub (guglxni/bharatwatch)
  ├── main branch
  │     ├── Render auto-deploys backend (render.yaml blueprint)
  │     └── Vercel auto-deploys dashboard (git-connected)
  │
  ├── Render free tier
  │     ├── Python 3.14 + FastAPI + SQLite
  │     ├── render_start.sh: seed DB → uvicorn on $PORT
  │     └── Health check: /api/v1/health
  │
  └── Vercel
        ├── Next.js 16 production build
        ├── /api/* rewrites to Render backend
        └── SSO protection disabled (public demo)
```
