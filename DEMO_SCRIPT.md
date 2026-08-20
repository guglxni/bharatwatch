# BharatWatch Demo Script (2–3 minutes)

## 1. Open the project
```bash
cd ~/scrape-verse/bharatwatch
```

## 2. Show the modular codebase
```bash
tree bharatwatch/modules -L 2
```
Highlight: every module has schema.py, sources.yaml, and a Bright Data collector ID.

## 3. Show the live collector IDs
cat bharatwatch/modules/tendersentry/sources.yaml
cat bharatwatch/modules/mandiwatch/sources.yaml
cat bharatwatch/modules/collegecutoff/sources.yaml
cat bharatwatch/modules/startuppulse/sources.yaml

## 4. Run a live scraper (TenderSentry example)
```bash
npx @brightdata/cli scraper run c_mt0uqsr9275nljkmec "https://alexandria-circles-chassis-hub.trycloudflare.com/tender/" --pretty
```
Show clean JSON output with tender_id, title, department, estimated_value, closing_date, document_link.

## 5. Run the backend API
```bash
.venv/bin/python -m bharatwatch.cli serve
```

In another terminal, verify:
```bash
curl -s http://localhost:8000/api/v1/health
curl -s http://localhost:8000/api/v1/modules
curl -s http://localhost:8000/api/v1/tendersentry/changes
```

## 6. Show the dashboard
```bash
cd dashboard && npm run dev
```
Open http://localhost:3000. Walk through:
- Health cards (5 modules, 4 live + 1 demo)
- Change feed with real data
- Heal event log showing self-healing attempt

## 7. Closing line
"BharatWatch turns messy Indian public data into a reliable, self-healing intelligence layer — built with Bright Data Scraper Studio."
