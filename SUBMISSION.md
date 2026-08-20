# Into the Scrape-Verse Submission

## Project

**BharatWatch** — Self-Healing Local Intelligence for India
- **GitHub:** https://github.com/guglxni/bharatwatch
- **Live Demo:** Run locally with `python -m bharatwatch.cli serve` + `npm run dev` (see README)

## Tracks Entered

- Web-Slinger (Best Use of Bright Data)
- Suit-Up (Best UI)
- Spider-Sense (Cleanest Code)
- Daily Bugle (LinkedIn post)

## What It Does

BharatWatch monitors 5 Indian public-data verticals through custom Bright Data Scraper Studio collectors:

| Module | Data Source | Collector ID | Status |
|--------|-------------|--------------|--------|
| NaukriAlert | Government job notifications | `demo-collector-naukri` | Demo (SSC blocked by Bright Data policy) |
| TenderSentry | Government tenders | `c_mt0uqsr9275nljkmec` | ✅ Verified |
| MandiWatch | Agriculture mandi prices | `c_mt1h2pqy2fdtlurkwq` | ✅ Verified |
| CollegeCutoff | College counselling cutoffs | `c_mt1h6w0ukc2lut11g` | ✅ Verified |
| StartupPulse | Startup/MSME schemes | `c_mt1hcxap876dyo54k` | ✅ Verified |

## Self-Healing Demo

1. Bright Data collector `c_mt0uqsr9275nljkmec` runs successfully on the tender table.
2. Fixture layout is changed to card-style (or column order changes).
3. Re-run returns `[]` or fails schema validation.
4. `bdata scraper heal` is invoked with a natural-language description of the new layout.
5. After approval, the same collector ID returns clean data again.
6. The dashboard `Heal Log` page records this event.

## Demo Video Script

**Scene 1 — Terminal:**
- Run `npx @brightdata/cli scraper run c_mt0uqsr9275nljkmec <url> --pretty`
- Show clean JSON output with 2 tender rows.

**Scene 2 — Change layout:**
- Switch the local fixture to the `naukri-redesign`/`card` layout or a different table structure.
- Re-run the same collector → `[]` or `dead_page`.

**Scene 3 — Heal:**
- `npx @brightdata/cli scraper heal c_mt0uqsr9275nljkmec "The page now uses a table with columns tender_id, title, department, estimated_value, closing_date, and document_link. Do not navigate any links."`
- `npx @brightdata/cli scraper approve c_mt0uqsr9275nljkmec`
- Re-run → clean JSON again.

**Scene 4 — Dashboard:**
- Open `http://localhost:3000`
- Show the 5 module health cards, the change feed, and the heal log entry.

## Key Technical Decisions

- All collectors are created with `npx @brightdata/cli scraper create`, not pre-built library scrapers.
- A generic `orchestrator` normalizes Bright Data output, validates schemas, and computes diffs.
- The dashboard is a single Next.js app using shadcn/ui.
- Local static HTML mirrors are used for reliable, repeatable demo and testing.

## AI Disclosure

AI coding assistants (Claude, Cursor, Codex) were used to scaffold, document, and iterate on the project. All generated code was reviewed and tested by the human participant. Architecture, module design, and demo narrative are original.

## Submission Checklist

- [x] Public GitHub repo
- [x] README with setup and collector IDs
- [x] Working backend + dashboard
- [x] At least one verified live collector with self-healing demo
- [x] `SUBMISSION.md` with demo script and track mapping
- [x] LinkedIn post drafted
- [ ] Demo video uploaded (do this yourself before deadline)
- [ ] Devpost / WeMakeDevs form submitted

## Promo Code Used

`wemakedevs` (applied during Bright Data billing setup for $50 credits).
