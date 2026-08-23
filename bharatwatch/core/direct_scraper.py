"""BharatWatch direct scraper — Playwright + stealth fallback.

When Bright Data Scraper Studio blocks a domain ("Domain not allowed") or the
proxy zone returns 403 ("tunneling socket could not be established"), this
module provides a local headless-browser fallback that can extract structured
data from real Indian govt portals.

Usage:
    from bharatwatch.core.direct_scraper import scrape_with_playwright
    items = scrape_with_playwright(url, extraction_prompt, schema_fields)
"""
import json
import re
import time
from typing import Any, Dict, List, Optional

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


# ────────────────────────────────────────────────────────────────────────────
# Per-module extraction rules (CSS selectors + field mapping)
# ────────────────────────────────────────────────────────────────────────────
EXTRACTION_RULES: Dict[str, Dict[str, Any]] = {
    "nauktrialert": {
        # Sarkari result / freejobalert style pages
        "selectors": {
            "item": ".post, .job-item, .vacancy-item, article, .entry",
            "title": "h2, h3, .title, .post-title",
            "department": ".company, .dept, .org",
            "posted_date": ".date, .posted, time",
            "link": "a[href]",
        },
        "fallback_text_patterns": [
            r"([A-Z][A-Za-z\s]+)\s*[-–]\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})",
        ],
    },
    "tendersentry": {
        "selectors": {
            "item": "tr, .tender-item, .list-item",
            "title": "td:nth-child(2), .title, .tender-title",
            "tender_id": "td:nth-child(1), .tender-id, .id",
            "department": "td:nth-child(3), .dept, .department",
            "closing_date": "td:nth-child(4), .closing, .date",
            "estimated_value": "td:nth-child(5), .value, .amount",
        },
    },
    "mandiwatch": {
        "selectors": {
            "item": "tr, .price-row, .mandi-item",
            "mandi": "td:nth-child(1), .mandi-name",
            "crop": "td:nth-child(2), .commodity, .crop",
            "variety": "td:nth-child(3), .variety",
            "min_price": "td:nth-child(4), .min",
            "max_price": "td:nth-child(5), .max",
            "modal_price": "td:nth-child(6), .modal",
        },
    },
    "collegecutoff": {
        "selectors": {
            "item": "tr, .cutoff-row",
            "institute": "td:nth-child(1), .institute, .college",
            "branch": "td:nth-child(2), .branch, .program",
            "round": "td:nth-child(3), .round",
            "opening_rank": "td:nth-child(4), .opening",
            "closing_rank": "td:nth-child(5), .closing",
        },
    },
    "startuppulse": {
        "selectors": {
            "item": ".scheme-card, .scheme, article, .list-item",
            "title": "h2, h3, .title, .scheme-title",
            "ministry": ".ministry, .dept, .by",
            "description": "p, .desc, .summary",
            "link": "a[href]",
        },
    },
}


def _extract_items(page, module: str, url: str) -> List[Dict[str, Any]]:
    """Extract structured items from a page using CSS-selector rules."""
    rules = EXTRACTION_RULES.get(module, {})
    selectors = rules.get("selectors", {})
    if not selectors:
        return []

    item_selector = selectors.get("item", "tr, article, .item")
    items: List[Dict[str, Any]] = []

    try:
        elements = page.query_selector_all(item_selector)
    except Exception:
        return items

    for el in elements[:50]:  # cap at 50 items
        item: Dict[str, Any] = {}
        for field, sel in selectors.items():
            if field == "item":
                continue
            try:
                child = el.query_selector(sel)
                if child:
                    val = child.inner_text().strip()
                    if field == "link":
                        val = child.get_attribute("href") or val
                    item[field] = val[:500]
            except Exception:
                pass
        if item and len(item) >= 2:  # need at least 2 fields to count as valid
            item["_source_url"] = url
            items.append(item)

    # Fallback: if no structured items, grab text and use regex patterns
    if not items and rules.get("fallback_text_patterns"):
        try:
            body_text = page.inner_text("body")
            for pattern in rules["fallback_text_patterns"]:
                for m in re.finditer(pattern, body_text):
                    items.append({"_raw_match": m.group(0), "_source_url": url})
        except Exception:
            pass

    return items


def scrape_with_playwright(
    url: str,
    module: str,
    wait_selector: Optional[str] = None,
    wait_ms: int = 3000,
) -> Dict[str, Any]:
    """Scrape a URL with a stealthed headless browser and extract structured items.

    Uses site-specific extractors from site_extractors.py when available,
    falls back to generic CSS-selector rules otherwise.

    Returns {"ok": bool, "items": list, "count": int, "error": str|None}
    """
    from bharatwatch.core.site_extractors import get_site_extractor

    result: Dict[str, Any] = {"ok": False, "items": [], "count": 0, "error": None}
    stealth = Stealth()

    # Find the site-specific extractor
    site_extractors = get_site_extractor(module)
    extractor_fn = None
    for site_url, fn in site_extractors:
        if site_url in url or url.startswith(site_url.rstrip("/")):
            extractor_fn = fn
            break

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
            )
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                locale="en-IN",
                extra_http_headers={
                    "Accept-Language": "en-IN,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )
            page = context.new_page()
            stealth.apply_stealth_sync(page)

            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
            except Exception as e:
                result["error"] = f"navigation: {e}"
                browser.close()
                return result

            # Wait for content
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=10000)
                except Exception:
                    pass
            else:
                page.wait_for_timeout(wait_ms)

            # Extract using site-specific extractor or generic fallback
            if extractor_fn:
                items = extractor_fn(page)
            else:
                items = _extract_items(page, module, url)

            result["items"] = items
            result["count"] = len(items)
            result["ok"] = len(items) > 0

            if not items:
                result["error"] = "no items extracted — selectors may need updating"

            browser.close()
    except Exception as e:
        result["error"] = f"playwright: {e}"

    return result


def scrape_with_curl(url: str, module: str) -> Dict[str, Any]:
    """Lightweight fallback: curl + regex extraction (no JS rendering).

    Faster than Playwright but won't work on JS-heavy sites.
    """
    import subprocess

    result: Dict[str, Any] = {"ok": False, "items": [], "count": 0, "error": None}
    try:
        proc = subprocess.run(
            [
                "curl", "-sL", "--max-time", "20",
                "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "-H", "Accept-Language: en-IN,en;q=0.9",
                url,
            ],
            capture_output=True, text=True, timeout=30,
        )
        html = proc.stdout
        if not html or len(html) < 200:
            result["error"] = "empty or blocked response"
            return result

        # Use extraction rules to parse HTML with regex
        rules = EXTRACTION_RULES.get(module, {})
        selectors = rules.get("selectors", {})
        item_sel = selectors.get("item", "")

        # Simple table row extraction
        if "tr" in item_sel:
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL | re.IGNORECASE)
            for row in rows[:50]:
                cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.DOTALL | re.IGNORECASE)
                cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
                if len(cells) >= 3:
                    item = {f"col_{i}": c[:300] for i, c in enumerate(cells)}
                    item["_source_url"] = url
                    result["items"].append(item)

        result["count"] = len(result["items"])
        result["ok"] = result["count"] > 0
        if not result["ok"]:
            result["error"] = "no items extracted from HTML"
    except Exception as e:
        result["error"] = f"curl: {e}"

    return result


def scrape_with_brightdata_unlocker(url: str, module: str) -> Dict[str, Any]:
    """Use Bright Data Web Unlocker Direct API to bypass proxy 403s.

    This is the cleanest fix for "tunneling socket could not be established" —
    it makes a REST call instead of a proxy tunnel, so the 403 never happens.
    Returns HTML that we then parse with the same extractors.
    """
    import os
    import subprocess
    import json as _json

    result: Dict[str, Any] = {"ok": False, "items": [], "count": 0, "error": None}

    # Get the API key from the Bright Data CLI credentials
    cred_path = os.path.expanduser("~/Library/Application Support/brightdata-cli/credentials.json")
    api_key = ""
    try:
        with open(cred_path) as f:
            api_key = _json.load(f).get("api", {}).get("key", "")
    except Exception:
        pass

    if not api_key:
        result["error"] = "no Bright Data API key found"
        return result

    try:
        # Web Unlocker Direct API — REST call, no proxy tunnel
        proc = subprocess.run(
            [
                "curl", "-s", "--max-time", "60",
                "https://api.brightdata.com/request",
                "-H", f"Authorization: Bearer {api_key}",
                "-H", "Content-Type: application/json",
                "-d", _json.dumps({
                    "zone": "cli_unlocker",
                    "url": url,
                    "format": "raw",
                }),
            ],
            capture_output=True, text=True, timeout=70,
        )
        html = proc.stdout
        if not html or len(html) < 200:
            result["error"] = f"unlocker returned empty (exit {proc.returncode})"
            return result

        # Parse the HTML using the same site-specific extractors
        # We need a page-like object — use a simple regex-based parser
        rules = EXTRACTION_RULES.get(module, {})
        selectors = rules.get("selectors", {})
        item_sel = selectors.get("item", "")

        if "tr" in item_sel:
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL | re.IGNORECASE)
            for row in rows[:50]:
                cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.DOTALL | re.IGNORECASE)
                cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
                if len(cells) >= 3:
                    item = {f"col_{i}": c[:300] for i, c in enumerate(cells)}
                    item["_source_url"] = url
                    result["items"].append(item)

        # Also try extracting links
        if not result["items"]:
            links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]{10,120})</a>', html, re.IGNORECASE)
            for href, text in links[:30]:
                text = re.sub(r"\s+", " ", text).strip()
                if text and not any(x in text.lower() for x in ["login", "register", "home", "about"]):
                    result["items"].append({"title": text[:200], "official_link": href[:200], "_source_url": url})

        result["count"] = len(result["items"])
        result["ok"] = result["count"] > 0
        if not result["ok"]:
            result["error"] = "no items extracted from unlocker HTML"
    except Exception as e:
        result["error"] = f"unlocker: {e}"

    return result
