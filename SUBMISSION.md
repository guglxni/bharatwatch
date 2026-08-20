# Into the Scrape-Verse Submission

## Project

**BharatWatch** — Self-Healing Local Intelligence for India

GitHub: https://github.com/guglxni/bharatwatch

---

## Tracks

- Web-Slinger (Best Use of Bright Data)
- Suit-Up (Best UI)
- Spider-Sense (Cleanest Code)
- Daily Bugle (LinkedIn post tagging WeMakeDevs)

---

## What We Built

A civic intelligence platform that turns scattered Indian public data into a reliable, always-current API + dashboard. It is built around Bright Data Scraper Studio: every module is powered by a custom collector (`c_*`), and the scraper can repair itself when the target site changes layout.

---

## Demo Video Script

1. Open repo in the terminal.
2. Run `npx @brightdata/cli scraper run c_mt0srxto15g4to0is3 "https://ssc.nic.in" --pretty` to show structured JSON.
3. Show the local fixture server (simulates a site redesign) and re-run the scraper — output is empty.
4. Run `npx @brightdata/cli scraper heal` with the natural-language description of the new layout.
5. Approve the fix and re-run — data is recovered.
6. Switch to the BharatWatch dashboard at http://localhost:3000 and show:
   - Source health cards
   - Latest changes feed
   - Heal event log
   - Module pages for jobs, tenders, mandi, cutoffs, and startup schemes
7. Close with the API endpoint returning changes for a module.

---

## Required Submission Items

- [x] Public source-code repository
- [x] Clear README with setup instructions
- [x] Example structured output (see `README.md` and `tests/fixtures/`)
- [ ] Demo video (record after this submission file is created)
- [x] Clear explanation of how Bright Data Scraper Studio is used (see README)

---

## Custom Scraper Proof

- Collector ID: `c_mt0srxto15g4to0is3`
- Created with: `npx @brightdata/cli scraper create "https://ssc.nic.in" "..."`
- Healed with: `npx @brightdata/cli scraper heal c_mt0srxto15g4to0is3 "..."`

This is not a Bright Data pre-built library scraper.

---

## Public Data Only

All scraped data is publicly available. No login-walled sites, paywalled content, or personal data is collected.

---

## AI Disclosure

AI coding assistants were used to scaffold, document, and iterate. All generated code was reviewed, tested, and refined by the human participant. Architecture and demo narrative are original work created during the hackathon.
