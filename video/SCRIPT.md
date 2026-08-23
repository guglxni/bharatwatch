# BharatWatch Demo Video — SCRIPT.md

**Total runtime target:** ~170 seconds (under 3 min, with breathing room)
**Voice:** ElevenLabs — Sarah (`EXAVITQu4vr4xnSDxMaL`), model `eleven_multilingual_v2`
**Pace:** ~145 wpm, calm and confident. ~410 words total.

---

## Segment timings (for audio + scene sync)

| # | Scene | Dur (s) | Words |
|---|-------|---------|-------|
| 1 | Cold open / hook | 0–12 | ~30 |
| 2 | The problem | 12–30 | ~40 |
| 3 | What BharatWatch is | 30–52 | ~50 |
| 4 | The five collectors | 52–80 | ~62 |
| 5 | Tech stack & architecture | 80–105 | ~55 |
| 6 | Live demo — dashboard | 105–140 | ~75 |
| 7 | Self-healing showcase | 140–160 | ~42 |
| 8 | Close / CTA | 160–170 | ~20 |

---

## NARRATION TEXT (verbatim, one file per segment)

### 01 — Hook  (`vo/01-hook.txt`)
"Every day, India's public portals publish thousands of job alerts, tenders, and market prices. And every day, that data quietly changes, moves, and disappears. BharatWatch was built to watch it all — automatically."

### 02 — Problem  (`vo/02-problem.txt`)
"Government websites are notoriously fragile. They redesign without warning, break scrapers overnight, and offer no APIs. So critical public data stays locked in pages that nobody can reliably track. Until now."

### 03 — What it is  (`vo/03-what.txt`)
"BharatWatch is a self-healing local intelligence platform. Five live collectors monitor India's most important public data sources. It's built entirely on Bright Data's Scraper Studio — every single scraper is custom-generated from a plain-English prompt, not pulled from a prebuilt library."

### 04 — Five collectors  (`vo/04-modules.txt`)
"NaukriAlert tracks Sarkari job notifications with vacancies and deadlines. TenderSentry watches GeM and public procurement worth crores. MandiWatch follows daily crop prices across mandis. CollegeCutoff monitors JoSAA admission ranks. And StartupPulse surfaces government funding schemes. Five verticals. One mission."

### 05 — Tech & architecture  (`vo/05-arch.txt`)
"Under the hood, a Python and FastAPI orchestrator runs every scrape, validates each record against typed Pydantic schemas, and stores snapshots in SQLite. A diff engine compares every snapshot to the last and emits field-level changes. And a dark-native Next.js dashboard visualizes it all in real time."

### 06 — Live demo  (`vo/06-demo.txt`)
"Here's the live dashboard. Mission Control shows five healthy sources, over thirty records, and forty-eight changes caught this week. Drilling into NaukriAlert, you can see the actual extracted rows — the SSC CGL with seventeen thousand seven hundred and twenty-seven vacancies, application deadlines, and exam dates. Every chart is fed by real scraped data, with seven days of history."

### 07 — Self-healing  (`vo/07-heal.txt`)
"But here's the real magic. When a portal changes its layout, the scraper doesn't break — it heals. The diff engine detects selector drift, Bright Data's AI regenerates the extraction code, and the pipeline resumes. Zero manual fixes. Five out of five heals succeeded."

### 08 — Close  (`vo/08-close.txt`)
"BharatWatch. India's public data, watched for you — self-healing, open, and always on. Built for Into the Scrape-Verse."
