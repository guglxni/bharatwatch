"""BharatWatch real-site extractors.

Site-specific CSS selectors for Indian govt/job/data portals that are scraped
via the Playwright stealth fallback (when Bright Data blocks the domain).

Each extractor returns a list of structured dicts matching the module schema.
"""
import re
from typing import Any, Dict, List


def extract_sarkariresult(page) -> List[Dict[str, Any]]:
    """Extract latest job notifications from sarkariresult.com."""
    items = []
    links = page.query_selector_all("a")
    seen = set()
    for link in links:
        try:
            txt = link.inner_text().strip()
            href = link.get_attribute("href") or ""
            # Filter: job-like titles (not nav/footer links)
            if (txt and 15 < len(txt) < 120 and
                href and "sarkariresult.com/20" in href and
                href not in seen and
                not any(x in txt.lower() for x in
                    ["instagram", "facebook", "youtube", "telegram", "twitter",
                     "download", "home", "about", "contact", "privacy"])):
                seen.add(href)
                # Try to find date from nearby text
                date = ""
                try:
                    parent = link.evaluate("el => el.parentElement?.textContent || ''")
                    date_match = re.search(r"(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})", parent)
                    if date_match:
                        date = date_match.group(1)
                except Exception:
                    pass
                items.append({
                    "title": txt.replace("\xa0", " ").strip(),
                    "department": "",  # not available on listing page
                    "notification_date": date,
                    "official_link": href,
                    "number_of_vacancies": "",
                    "qualification_required": "",
                    "last_application_date": "",
                    "exam_date": "",
                })
        except Exception:
            pass
    return items[:30]


def extract_freejobalert(page) -> List[Dict[str, Any]]:
    """Extract latest govt job alerts from freejobalert.com."""
    items = []
    # The site has job posts in table rows or div elements
    selectors = [
        "table tr",
        ".job-item",
        ".post",
        ".entry",
        "article",
    ]
    for sel in selectors:
        try:
            rows = page.query_selector_all(sel)
            if rows and len(rows) > 3:
                for row in rows[1:31]:  # skip header
                    try:
                        cells = row.query_selector_all("td, th, p, h2, h3, a")
                        texts = [c.inner_text().strip() for c in cells if c.inner_text().strip()]
                        links = row.query_selector_all("a[href]")
                        href = links[0].get_attribute("href") if links else ""
                        if texts and len(texts[0]) > 10:
                            items.append({
                                "title": texts[0][:200],
                                "department": texts[1] if len(texts) > 1 else "",
                                "notification_date": "",
                                "official_link": href,
                                "number_of_vacancies": "",
                                "qualification_required": "",
                                "last_application_date": "",
                                "exam_date": "",
                            })
                    except Exception:
                        pass
                if items:
                    break
        except Exception:
            pass

    # Fallback: just grab job links
    if not items:
        links = page.query_selector_all("a")
        seen = set()
        for link in links:
            try:
                txt = link.inner_text().strip()
                href = link.get_attribute("href") or ""
                if (txt and 15 < len(txt) < 120 and
                    href and "freejobalert.com" in href and
                    href not in seen and
                    not any(x in txt.lower() for x in
                        ["download", "home", "about", "contact", "app",
                         "instagram", "facebook", "youtube"])):
                    seen.add(href)
                    items.append({
                        "title": txt,
                        "department": "",
                        "notification_date": "",
                        "official_link": href,
                        "number_of_vacancies": "",
                        "qualification_required": "",
                        "last_application_date": "",
                        "exam_date": "",
                    })
            except Exception:
                pass
    return items[:30]


def extract_gktoday(page) -> List[Dict[str, Any]]:
    """Extract current affairs/scheme items from gktoday.in."""
    items = []
    selectors = ["article", ".post", ".entry", ".topic-item", ".list-item"]
    for sel in selectors:
        try:
            entries = page.query_selector_all(sel)
            if entries and len(entries) > 2:
                for entry in entries[:20]:
                    try:
                        title_el = entry.query_selector("h2, h3, h4, .title, a")
                        title = title_el.inner_text().strip() if title_el else ""
                        link_el = entry.query_selector("a[href]")
                        href = link_el.get_attribute("href") if link_el else ""
                        desc_el = entry.query_selector("p, .excerpt, .summary")
                        desc = desc_el.inner_text().strip()[:300] if desc_el else ""
                        if title and len(title) > 10:
                            items.append({
                                "title": title[:200],
                                "ministry": "",
                                "description": desc,
                                "official_link": href,
                            })
                    except Exception:
                        pass
                if items:
                    break
        except Exception:
            pass

    # Fallback: links containing topic-like text
    if not items:
        links = page.query_selector_all("a")
        seen = set()
        for link in links:
            try:
                txt = link.inner_text().strip()
                href = link.get_attribute("href") or ""
                if (txt and 15 < len(txt) < 150 and
                    href and "gktoday.in/" in href and
                    href not in seen and
                    not any(x in txt.lower() for x in
                        ["login", "register", "account", "quiz", "book", "home"])):
                    seen.add(href)
                    items.append({
                        "title": txt[:200],
                        "ministry": "",
                        "description": "",
                        "official_link": href,
                    })
            except Exception:
                pass
    return items[:20]


def extract_jagranjosh(page) -> List[Dict[str, Any]]:
    """Extract govt job / exam listings from jagranjosh.com."""
    items = []
    links = page.query_selector_all("a")
    seen = set()
    for link in links:
        try:
            txt = link.inner_text().strip()
            href = link.get_attribute("href") or ""
            if (txt and 15 < len(txt) < 120 and
                href and href not in seen and
                any(kw in txt.lower() for kw in
                    ["recruitment", "vacancy", "job", "form", "result",
                     "admit card", "notification", "exam"]) and
                not any(x in txt.lower() for x in
                    ["login", "register", "subscribe", "download app"])):
                seen.add(href)
                items.append({
                    "title": txt[:200],
                    "department": "",
                    "notification_date": "",
                    "official_link": href,
                    "number_of_vacancies": "",
                    "qualification_required": "",
                    "last_application_date": "",
                    "exam_date": "",
                })
        except Exception:
            pass
    return items[:30]


# ────────────────────────────────────────────────────────────────────────────
# Registry: module → (extractor_fn, url, wait_selector)
# ────────────────────────────────────────────────────────────────────────────
SITE_REGISTRY = {
    "nauktrialert": {
        "urls": [
            ("https://www.sarkariresult.com/", extract_sarkariresult),
            ("https://www.freejobalert.com/", extract_freejobalert),
        ],
        "primary": "https://www.sarkariresult.com/",
    },
    "startuppulse": {
        "urls": [
            ("https://www.gktoday.in/current-affairs/", extract_gktoday),
        ],
        "primary": "https://www.gktoday.in/current-affairs/",
    },
}


def get_site_extractor(module: str):
    """Get the (url, extractor_fn) list for a module."""
    entry = SITE_REGISTRY.get(module)
    if not entry:
        return []
    return entry["urls"]
