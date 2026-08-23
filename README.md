# BharatWatch

Self-healing local intelligence for India.

Built for the **WeMakeDevs × Bright Data "Into the Scrape-Verse"** hackathon, August 17–23, 2026.

## 🌐 Live Demo

| Surface | URL |
|---|---|
| **Dashboard (Vercel)** | https://bharatwatch-live.vercel.app |
| **Landing page** | https://bharatwatch-live.vercel.app |
| **API (Render)** | https://bharatwatch-api.onrender.com |
| API health | https://bharatwatch-api.onrender.com/api/v1/health |
| API overview | https://bharatwatch-api.onrender.com/api/v1/overview |
| **Source code** | https://github.com/guglxni/bharatwatch |

**Stack:** Next.js 16 dashboard on **Vercel** · FastAPI + SQLite backend on **Render** · Bright Data Scraper Studio collectors.

> **The problem:** Public data across Indian portals (jobs, tenders, mandi prices, college cutoffs, startup schemes) is scattered, changes layout without warning, and quietly breaks scrapers.
> **The solution:** BharatWatch uses Bright Data Scraper Studio to build custom scrapers, monitors them for failures, and heals them with a single prompt when the target site changes — all exposed through a clean API and dashboard.

---

## Tracks Entered

- **Web-Slinger** (Best Use of Bright Data) — custom Scraper Studio collectors driving the entire pipeline
- **Suit-Up** (Best UI) — Next.js dashboard with module navigation, change feeds, and health indicators
- **Spider-Sense** (Cleanest Code) — modular Python backend, Pydantic schemas, diff engine, GitHub Actions CI
- **Daily Bugle** — LinkedIn post about the build, tagging WeMakeDevs

---

## What It Does

BharatWatch collects publicly available Indian civic data across five verticals:

| Module | Collector ID | Status |
|--------|--------------|--------|
| **NaukriAlert** | `c_mt5yz3z91f5nm13h9x` | ✅ Live — verified run extracts 5 job notices |
| **TenderSentry** | `c_mt0uqsr9275nljkmec` | ✅ Healthy — verified run |
| **MandiWatch** | `c_mt1h2pqy2fdtlurkwq` | ✅ Healthy — verified run |
| **CollegeCutoff** | `c_mt1h6w0ukc2lut11g` | ✅ Healthy — verified run |
| **StartupPulse** | `c_mt1hcxap876dyo54k` | ✅ Healthy — verified run |

Each module has:
- A Bright Data collector ID (custom, not a pre-built library scraper)
- A Pydantic schema
- A change-diff engine
- A dashboard page

---

## Tech Stack

- **Bright Data Scraper Studio** — `@brightdata/cli` for `create`, `run`, and `heal`
- **Python + FastAPI** — orchestration, diff engine, storage API
- **SQLite** — lightweight snapshot + change tracking
- **Next.js + Tailwind + shadcn/ui** — dashboard
- **GitHub Actions** — scheduled scrapes and heal monitors

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/guglxni/bharatwatch.git
cd bharatwatch

# 2. Install Python dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Set your Bright Data API token
#    Get it from https://brightdata.com/cp/settings/api
export BRIGHT_DATA_API_TOKEN="your_api_token"
#    Optional: export BRIGHT_DATA_COLLECTOR_BASE_URL="https://api.brightdata.com/dca/trigger"

# 4. Start the API server
python -m bharatwatch.cli serve

# 5. In another terminal, start the dashboard
cd dashboard
npm install
npm run dev

# 6. Open http://localhost:3000
```

---

## Bright Data CLI Setup

```bash
# Login via device code (recommended for headless agents)
npx @brightdata/cli login --device
# Approve the code at https://brightdata.com/cp/device_approve

# Verify your account
npx @brightdata/cli budget
```

Use the promo code `wemakedevs` in the Bright Data billing section to get $50 in credits.

---

## Scraper Studio Workflow

All commands are executed from the terminal via the Bright Data CLI.

### 1. Create a custom scraper

```bash
npx @brightdata/cli scraper create "https://ssc.nic.in"   "Extract all government job notifications. For each item, return title, department, notification_date, last_application_date, exam_date, number_of_vacancies, qualification_required, and official_link. Return as a JSON array."
```

The command returns a collector ID: `c_mt0srxto15g4to0is3`.

### 2. Run the scraper

```bash
npx @brightdata/cli scraper run c_mt0srxto15g4to0is3 "https://ssc.nic.in" --pretty
```

Returns clean, structured JSON.

### 3. Self-heal when the site changes

```bash
npx @brightdata/cli scraper heal c_mt0srxto15g4to0is3   "The page layout changed. The notice cards are now article elements with class notice-card. The official_link is no longer in an anchor tag; it is now the text content of a div with class notice-link and data-url attribute. Do not navigate any links. Extract from the single page only."

# Approve the generated fix
npx @brightdata/cli scraper approve c_mt0srxto15g4to0is3

# Re-run to verify data is recovered
npx @brightdata/cli scraper run c_mt0srxto15g4to0is3 "https://ssc.nic.in" --pretty
```

The collector ID stays the same; downstream code and the dashboard never change.

---

## Project Structure

```
bharatwatch/
├── bharatwatch/
│   ├── api/            # FastAPI routes
│   ├── cli/            # CLI commands (serve, run, heal, etc.)
│   ├── core/           # config, database, models, diff engine, orchestrator
│   └── modules/        # One module per civic vertical
│       ├── nauktrialert/
│       ├── tendersentry/
│       ├── mandiwatch/
│       ├── collegecutoff/
│       └── startuppulse/
├── dashboard/          # Next.js dashboard
├── tests/              # Unit tests and local fixture sites
├── .github/workflows/  # CI cron and heal monitor
├── docs/               # HTML planning docs (PRD, architecture, etc.)
├── CLAUDE.md           # Agent instructions for Claude Code
└── .cursorrules        # Agent instructions for Cursor
```

---

## AI Disclosure

AI coding assistants (Claude, Cursor, Codex) were used to scaffold, document, and iterate on this project. All generated code was reviewed, tested, and refined by the human participant. The project architecture, module design, and demo narrative are original work created during the hackathon.

---

## License

MIT © 2026 Aaryan Guglani
