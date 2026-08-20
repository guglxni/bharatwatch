# BharatWatch 🇮🇳

**Self-Healing Local Intelligence Layer for India**

Built for the [WeMakeDevs × Bright Data](https://www.wemakedevs.org) "Into the Scrape-Verse" hackathon (Aug 17–23, 2026).

## Problem
Indian public data is fragmented across slow, frequently redesigned websites. Job seekers, students, farmers, MSMEs, and founders miss critical deadlines because monitoring 50+ portals manually is impossible.

## Solution
BharatWatch uses [Bright Data Scraper Studio](https://brightdata.com) to build custom scrapers for Indian public sites, automatically heals them when layouts change, and presents structured updates in a unified dashboard.

## Modules
- **NaukriAlert** — Government job notifications (SSC, UPSC, IBPS, etc.)
- **TenderSentry** — Public tenders and corrigendums
- **CollegeCutoff** — Engineering/medical counselling cutoffs
- **StartupPulse** — Startup policies, schemes, and compliance updates
- **MandiWatch** — Agricultural mandi prices

## Tech Stack
- Bright Data Scraper Studio (CLI + Collector IDs)
- Python + FastAPI + SQLAlchemy + SQLite
- Next.js + React + TypeScript + Tailwind CSS + shadcn/ui
- GitHub Actions (cron + heal + notify)

## Quick Start
```bash
# 1. Clone
gh repo clone <your-github>/bharatwatch
cd bharatwatch

# 2. Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Frontend
cd dashboard
pnpm install
pnpm dev

# 4. Env
cp .env.example .env
# Edit .env with your Bright Data token
```

## Docs
Open `docs/INDEX.html` in your browser for the full documentation suite.

## Self-Healing Demo
1. Run `python -m bharatwatch.cli run-module nauktrialert`
2. Change the local test HTML in `tests/fixtures/`
3. Run `python -m bharatwatch.cli heal`
4. Re-run and watch the dashboard update

## License
MIT
