"""
Rich seed for BharatWatch demo: realistic live data for all 5 modules,
7-day history timeline of snapshots, change events, and heal events.
Run: .venv/bin/python seed_rich_data.py
"""
import sys
import os
import json
import hashlib
import random
from datetime import datetime, timedelta, timezone

# Resolve paths relative to the repo root regardless of cwd (Render runs from repo root).
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO_ROOT, "bharatwatch"))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base, Source, Snapshot, Change, HealEvent
from core.database import init_db

random.seed(42)
init_db()
DB_PATH = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(REPO_ROOT, 'storage.db')}")
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
db = Session()


def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ---------------------------------------------------------------- collectors
COLLECTORS = {
    "nauktrialert": "c_mt6ateu71enq29ce1m",
    "tendersentry": "c_mt0uqsr9275nljkmec",
    "mandiwatch": "c_mt1h2pqy2fdtlurkwq",
    "collegecutoff": "c_mt1h6w0ukc2lut11g",
    "startuppulse": "c_mt1hcxap876dyo54k",
}

SOURCES_META = {
    "nauktrialert": ("SarkariResult — Latest Govt Jobs (BD Scraper Studio)", "https://www.sarkariresult.com/latestjob/"),
    "tendersentry": ("GeM + CPPP Government Tenders", "https://gem.gov.in/"),
    "mandiwatch": ("Agmarknet Mandi Prices", "https://agmarknet.gov.in/"),
    "collegecutoff": ("JoSAA Cutoff Ranks", "https://josaa.nic.in/"),
    "startuppulse": ("GKToday — Current Affairs & Schemes", "https://www.gktoday.in/current-affairs/"),
}


# ---------------------------------------------------------------- datasets
def naukri(day: int):
    base = [
        {"title": "SSC CGL 2024", "department": "Staff Selection Commission", "notification_date": "2024-06-24",
         "last_application_date": "2024-07-24", "exam_date": "2024-09-09", "number_of_vacancies": 17727,
         "qualification_required": "Bachelor's Degree", "official_link": "https://ssc.nic.in/cgl-2024"},
        {"title": "SSC CHSL 2024", "department": "Staff Selection Commission", "notification_date": "2024-04-08",
         "last_application_date": "2024-05-07", "exam_date": "2024-07-01", "number_of_vacancies": 3712,
         "qualification_required": "12th Pass", "official_link": "https://ssc.nic.in/chsl-2024"},
        {"title": "UPSC CSE 2024", "department": "Union Public Service Commission", "notification_date": "2024-02-14",
         "last_application_date": "2024-03-05", "exam_date": "2024-05-26", "number_of_vacancies": 1056,
         "qualification_required": "Bachelor's Degree", "official_link": "https://upsc.gov.in/cse-2024"},
        {"title": "IBPS PO 2024", "department": "Institute of Banking Personnel Selection", "notification_date": "2024-07-30",
         "last_application_date": "2024-08-28", "exam_date": "2024-10-19", "number_of_vacancies": 4455,
         "qualification_required": "Bachelor's Degree", "official_link": "https://ibps.in/po-2024"},
    ]
    items = [dict(x) for x in base]
    # late arrivals -> drives "created" change events
    if day >= 2:
        items.append({"title": "SSC MTS 2024", "department": "Staff Selection Commission", "notification_date": "2024-08-10",
                      "last_application_date": "2024-09-10", "exam_date": "2024-11-05", "number_of_vacancies": 8326,
                      "qualification_required": "10th Pass", "official_link": "https://ssc.nic.in/mts-2024"})
    if day >= 4:
        items.append({"title": "RBI Assistant 2024", "department": "Reserve Bank of India", "notification_date": "2024-08-14",
                      "last_application_date": "2024-09-04", "exam_date": "2024-10-30", "number_of_vacancies": 950,
                      "qualification_required": "Bachelor's Degree", "official_link": "https://rbi.org.in/assistant-2024"})
    # vacancy corrections -> drives "updated" events
    for it in items:
        if it["title"] == "SSC CGL 2024" and day >= 3:
            it["number_of_vacancies"] = 17727 + 213  # revised vacancy count
    return items


def tender(day: int):
    base = [
        {"tender_id": "GEM/2024/B/5821340", "title": "Supply of Computer Hardware & Peripherals",
         "department": "Ministry of Electronics & IT", "estimated_value": 2500000, "closing_date": "2024-08-30",
         "document_link": "https://eprocure.gov.in/tender/5821340"},
        {"tender_id": "CPPP/2024/6789012", "title": "Civil Work for Regional Office Building",
         "department": "CPWD", "estimated_value": 12000000, "closing_date": "2024-09-15",
         "document_link": "https://eprocure.gov.in/tender/6789012"},
        {"tender_id": "GEM/2024/B/5833101", "title": "Annual Maintenance of Data Centre Equipment",
         "department": "NIC", "estimated_value": 4800000, "closing_date": "2024-09-02",
         "document_link": "https://eprocure.gov.in/tender/5833101"},
    ]
    items = [dict(x) for x in base]
    if day >= 3:
        items.append({"tender_id": "GEM/2024/B/5841220", "title": "Procurement of EV Charging Stations",
                      "department": "Ministry of Power", "estimated_value": 18500000, "closing_date": "2024-09-20",
                      "document_link": "https://eprocure.gov.in/tender/5841220"})
    if day >= 5:
        items.append({"tender_id": "CPPP/2024/6790444", "title": "Solar Panel Installation — Phase II",
                      "department": "MNRE", "estimated_value": 32000000, "closing_date": "2024-09-28",
                      "document_link": "https://eprocure.gov.in/tender/6790444"})
    return items


def mandi(day: int):
    base = [
        {"state": "Karnataka", "district": "Bengaluru", "mandi": "Yeshwanthpur", "crop": "Tomato", "variety": "Hybrid",
         "min_price": 1200, "max_price": 1800, "modal_price": 1500, "date": ""},
        {"state": "Maharashtra", "district": "Pune", "mandi": "Pune Market Yard", "crop": "Onion", "variety": "Red",
         "min_price": 2200, "max_price": 3000, "modal_price": 2600, "date": ""},
        {"state": "Punjab", "district": "Ludhiana", "mandi": "Ludhiana", "crop": "Wheat", "variety": "Sharbati",
         "min_price": 2350, "max_price": 2550, "modal_price": 2450, "date": ""},
        {"state": "Gujarat", "district": "Rajkot", "mandi": "Rajkot", "crop": "Groundnut", "variety": "Bold",
         "min_price": 5200, "max_price": 5900, "modal_price": 5550, "date": ""},
        {"state": "Tamil Nadu", "district": "Erode", "mandi": "Erode", "crop": "Turmeric", "variety": "Finger",
         "min_price": 9800, "max_price": 11200, "modal_price": 10500, "date": ""},
        {"state": "Uttar Pradesh", "district": "Agra", "mandi": "Agra", "crop": "Potato", "variety": "Kufri Jyoti",
         "min_price": 900, "max_price": 1400, "modal_price": 1150, "date": ""},
    ]
    items = []
    for x in base:
        it = dict(x)
        drift = 1 + random.uniform(-0.04, 0.05) * (1 + day * 0.15)
        it["min_price"] = int(it["min_price"] * drift)
        it["max_price"] = int(it["max_price"] * drift)
        it["modal_price"] = int(it["modal_price"] * drift)
        it["date"] = (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d")
        items.append(it)
    return items


def cutoff(day: int):
    base = [
        {"institute": "IIT Bombay", "branch": "Computer Science & Engg", "opening_rank": 1, "closing_rank": 60,
         "round": "Round 1", "status": "Closed"},
        {"institute": "IIT Delhi", "branch": "Electrical Engineering", "opening_rank": 120, "closing_rank": 450,
         "round": "Round 1", "status": "Closed"},
        {"institute": "IIT Madras", "branch": "Mechanical Engineering", "opening_rank": 400, "closing_rank": 2100,
         "round": "Round 1", "status": "Closed"},
        {"institute": "NIT Trichy", "branch": "Computer Science & Engg", "opening_rank": 800, "closing_rank": 4200,
         "round": "Round 1", "status": "Closed"},
        {"institute": "IIT Kanpur", "branch": "Aerospace Engineering", "opening_rank": 900, "closing_rank": 3800,
         "round": "Round 1", "status": "Closed"},
    ]
    items = [dict(x) for x in base]
    if day >= 3:  # Round 2 closes ranks (slightly relaxed) -> updated events
        round2 = [
            {"institute": "IIT Bombay", "branch": "Computer Science & Engg", "opening_rank": 1, "closing_rank": 72,
             "round": "Round 2", "status": "Closed"},
            {"institute": "IIT Delhi", "branch": "Electrical Engineering", "opening_rank": 130, "closing_rank": 495,
             "round": "Round 2", "status": "Closed"},
            {"institute": "NIT Trichy", "branch": "Computer Science & Engg", "opening_rank": 820, "closing_rank": 4650,
             "round": "Round 2", "status": "Open"},
        ]
        items += round2
    if day >= 5:
        items.append({"institute": "IIT Kharagpur", "branch": "Computer Science & Engg", "opening_rank": 200,
                      "closing_rank": 1400, "round": "Round 2", "status": "Open"})
    return items


def startup(day: int):
    base = [
        {"title": "Startup India Seed Fund Scheme", "ministry": "DPIIT", "scheme_type": "Funding",
         "deadline": "2024-12-31", "summary": "Grants up to Rs 20 lakh for proof of concept and Rs 50 lakh convertible for prototype & market entry.",
         "link": "https://startupindia.gov.in/seed-fund"},
        {"title": "MSME Champions — Design Intervention Scheme", "ministry": "Ministry of MSME", "scheme_type": "Grant",
         "deadline": "2024-10-15", "summary": "Reimbursement of 75% of design costs for design-led innovation in MSMEs.",
         "link": "https://msme.gov.in/design-scheme"},
        {"title": "National Startup Awards", "ministry": "DPIIT", "scheme_type": "Recognition",
         "deadline": "2024-09-30", "summary": "National recognition for startups across 10 categories; includes mentorship and media visibility.",
         "link": "https://startupindia.gov.in/awards"},
    ]
    items = [dict(x) for x in base]
    if day >= 2:
        items.append({"title": "PLI Scheme for White Goods", "ministry": "Ministry of Heavy Industries", "scheme_type": "Incentive",
                      "deadline": "2024-11-20", "summary": "Production-linked incentives for AC & LED component manufacturers; 4-6% on incremental sales.",
                      "link": "https://heavyindustry.gov.in/pli-white-goods"})
    if day >= 4:
        items.append({"title": "AgriSure Fund", "ministry": "Ministry of Agriculture", "scheme_type": "Funding",
                      "deadline": "2025-01-15", "summary": "Rs 750 crore fund of funds for agri-tech startups; equity support up to Rs 10 crore.",
                      "link": "https://agricoop.nic.in/agrisure"})
    if day >= 6:
        items.append({"title": "Deep Tech Research Fund", "ministry": "MeitY", "scheme_type": "Funding",
                      "deadline": "2025-02-28", "summary": "Rs 1,000 crore fund for AI, quantum & semiconductor deep-tech startups.",
                      "link": "https://meity.gov.in/deep-tech-fund"})
    return items


GENERATORS = {
    "nauktrialert": naukri,
    "tendersentry": tender,
    "mandiwatch": mandi,
    "collegecutoff": cutoff,
    "startuppulse": startup,
}

KEY_FIELDS = {
    "nauktrialert": ["title", "department"],
    "tendersentry": ["tender_id", "title"],
    "mandiwatch": ["mandi", "crop", "variety"],
    "collegecutoff": ["institute", "branch", "round"],
    "startuppulse": ["title", "ministry"],
}


# ---------------------------------------------------------------- rebuild
# wipe old rows, keep nothing
db.query(Change).delete()
db.query(Snapshot).delete()
db.query(HealEvent).delete()
db.query(Source).delete()
db.commit()

sources = {}
for module, (name, url) in SOURCES_META.items():
    s = Source(module=module, name=name, url=url, collector_id=COLLECTORS[module],
               health="healthy", last_run_at=now())
    db.add(s)
    db.commit()
    sources[module] = s

HISTORY_DAYS = 7
for module, gen in GENERATORS.items():
    s = sources[module]
    prev = None
    for day in range(HISTORY_DAYS - 1, -1, -1):  # oldest -> newest
        ts = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=day)
        items = gen(HISTORY_DAYS - 1 - day)
        snap = Snapshot(source_id=s.id, raw_json=items,
                        hash=hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest(),
                        status="ok", captured_at=ts)
        db.add(snap)
        if prev is not None:
            old_map = {"|".join(str(i.get(k, "")) for k in KEY_FIELDS[module]): i for i in prev}
            new_map = {"|".join(str(i.get(k, "")) for k in KEY_FIELDS[module]): i for i in items}
            for k, v in new_map.items():
                if k not in old_map:
                    db.add(Change(source_id=s.id, change_type="created", before=None, after=v, detected_at=ts))
                elif json.dumps(old_map[k], sort_keys=True) != json.dumps(v, sort_keys=True):
                    db.add(Change(source_id=s.id, change_type="updated", before=old_map[k], after=v, detected_at=ts))
            for k, v in old_map.items():
                if k not in new_map:
                    db.add(Change(source_id=s.id, change_type="deleted", before=v, after=None, detected_at=ts))
        prev = items
    db.commit()

# heal events — the self-healing story across modules
heals = [
    (2, "Target site migrated from card layout to a table layout. Healed selectors: tender_id, title, department, estimated_value, closing_date, document_link.", "true"),
    (1, "SSC notification page redesigned; table#notices columns reordered. AI regenerated extraction code and re-verified against live page.", "true"),
    (3, "Agmarknet mirror changed price cell markup from span to raw text; price parsers re-anchored.", "true"),
    (4, "JoSAA published Round 2 cutoffs with new rows; collector auto-extended to new round without code changes.", "true"),
    (2, "GeM portal added anti-bot challenge; retried via Bright Data Unlocker proxy — recovered automatically.", "true"),
]
for i, (sid, desc, ok) in enumerate(heals):
    db.add(HealEvent(source_id=sid, description=desc, success=ok,
                     created_at=now() - timedelta(hours=(i + 1) * 9)))
db.commit()

# summary
for module, s in sources.items():
    snaps = db.query(Snapshot).filter_by(source_id=s.id).count()
    changes = db.query(Change).filter_by(source_id=s.id).count()
    items = db.query(Snapshot).filter_by(source_id=s.id).order_by(Snapshot.captured_at.desc()).first()
    print(f"{module}: {snaps} snapshots, {changes} changes, latest has {len(items.raw_json)} items")
print("heal events:", db.query(HealEvent).count())
db.close()
