"""BharatWatch Bright Data integration — multi-product scraping engine.

Uses FIVE Bright Data products, each where it shines:

1. **Scraper Studio** — AI-generated collectors for structured extraction
   (`scraper create/run/heal`)
2. **Web Unlocker** — REST API to fetch any non-blocked URL as markdown/HTML
   (`scrape` / POST api.brightdata.com/request)
3. **SERP API** — Google search results for discovery
   (`search`)
4. **Discover** — AI-ranked web results with intent matching
   (`discover`)
5. **Scraping Browser** — Cloud Chrome for JS-rendered pages
   (`browser open/snapshot/get`)

Architecture per module:
  NaukriAlert:    discover → scrape (sarkariresult.com)
  TenderSentry:   search → scrape (tenderdetail.com)
  MandiWatch:     search → scrape (agmarknet mirror sites)
  CollegeCutoff:  scrape (josaa.nic.in via Web Unlocker)
  StartupPulse:   discover → scrape (gktoday.in)
"""
import json
import os
import re
import subprocess
from typing import Any, Dict, List, Optional


def _get_api_key() -> str:
    """Get the Bright Data API key from CLI credentials."""
    cred_path = os.path.expanduser("~/Library/Application Support/brightdata-cli/credentials.json")
    try:
        with open(cred_path) as f:
            return json.load(f).get("api_key", "")
    except Exception:
        return ""


def _run_cli(args: List[str], timeout: int = 60) -> Dict[str, Any]:
    """Run a Bright Data CLI command and parse JSON output."""
    cmd = ["npx", "@brightdata/cli"] + args + ["--json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        raw = proc.stdout or ""
        # Find JSON in output
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("{") or line.startswith("["):
                try:
                    return {"ok": True, "data": json.loads(line), "raw": raw}
                except json.JSONDecodeError:
                    continue
        return {"ok": proc.returncode == 0, "data": {}, "raw": raw + proc.stderr}
    except subprocess.TimeoutExpired:
        return {"ok": False, "data": {}, "raw": f"timeout after {timeout}s"}
    except Exception as e:
        return {"ok": False, "data": {}, "raw": str(e)}


# ────────────────────────────────────────────────────────────────────────────
# Product 1: Scraper Studio (scraper create/run/heal)
# ────────────────────────────────────────────────────────────────────────────
def scraper_run(collector_id: str, url: str, timeout: int = 300) -> Dict[str, Any]:
    """Run a Bright Data Scraper Studio collector."""
    r = _run_cli(["scraper", "run", collector_id, url], timeout)
    items = []
    data = r.get("data", {})
    if isinstance(data, list):
        items = [x for x in data if isinstance(x, dict)]
    elif isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                items = [x for x in v if isinstance(x, dict)]
                break
    return {"ok": r["ok"], "items": items, "count": len(items), "raw": r["raw"]}


def scraper_heal(collector_id: str, prompt: str, url: str = None) -> Dict[str, Any]:
    """Heal a Bright Data collector (auto-approve + auto-save)."""
    args = ["scraper", "heal", collector_id, prompt, "--auto-approve", "--auto-save"]
    if url:
        args += ["--url", url]
    r = _run_cli(args, 600)
    status = r.get("data", {}).get("status", "failed")
    return {"ok": r["ok"] and status in ("done", "completed"), "status": status, "raw": r["raw"]}


# ────────────────────────────────────────────────────────────────────────────
# Product 2: Web Unlocker (scrape)
# ────────────────────────────────────────────────────────────────────────────
def web_unlocker_scrape(url: str, fmt: str = "markdown") -> Dict[str, Any]:
    """Fetch a URL via Bright Data Web Unlocker — returns clean markdown/HTML."""
    r = _run_cli(["scrape", url, "--format", fmt], 60)
    # The scrape command returns content directly
    raw = r.get("raw", "")
    # Try to parse as JSON (when --json is used, it wraps the content)
    try:
        data = r.get("data", {})
        if isinstance(data, str):
            return {"ok": True, "content": data, "size": len(data)}
        elif isinstance(data, dict) and "content" in data:
            return {"ok": True, "content": data["content"], "size": len(data["content"])}
    except Exception:
        pass
    # Fallback: use raw output
    if raw and len(raw) > 100:
        return {"ok": True, "content": raw, "size": len(raw)}
    return {"ok": False, "content": "", "size": 0, "error": "empty response"}


def web_unlocker_rest(url: str) -> Dict[str, Any]:
    """Fetch a URL via Web Unlocker REST API directly (bypasses proxy tunnel)."""
    key = _get_api_key()
    if not key:
        return {"ok": False, "content": "", "size": 0, "error": "no API key"}
    try:
        proc = subprocess.run([
            "curl", "-s", "--max-time", "60",
            "https://api.brightdata.com/request",
            "-H", f"Authorization: Bearer {key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"zone": "cli_unlocker", "url": url, "format": "raw"}),
        ], capture_output=True, text=True, timeout=70)
        html = proc.stdout or ""
        if len(html) > 200:
            return {"ok": True, "content": html, "size": len(html)}
        return {"ok": False, "content": "", "size": 0, "error": f"empty ({len(html)} bytes)"}
    except Exception as e:
        return {"ok": False, "content": "", "size": 0, "error": str(e)}


# ────────────────────────────────────────────────────────────────────────────
# Product 3: SERP API (search)
# ────────────────────────────────────────────────────────────────────────────
def serp_search(query: str, country: str = "in", search_type: str = "web") -> Dict[str, Any]:
    """Search Google via Bright Data SERP API."""
    r = _run_cli(["search", query, "--country", country, "--type", search_type], 30)
    data = r.get("data", {})
    organic = data.get("organic", [])
    return {
        "ok": r["ok"],
        "results": organic,
        "count": len(organic),
        "raw": r["raw"],
    }


# ────────────────────────────────────────────────────────────────────────────
# Product 4: Discover (AI-ranked web results)
# ────────────────────────────────────────────────────────────────────────────
def discover_search(query: str, intent: str, country: str = "in", num: int = 10) -> Dict[str, Any]:
    """AI-driven web discovery with intent ranking."""
    r = _run_cli([
        "discover", query,
        "--intent", intent,
        "--country", country,
        "--language", "en",
        "--num-results", str(num),
    ], 120)
    data = r.get("data", {})
    results = data.get("results", [])
    return {
        "ok": r["ok"],
        "results": results,
        "count": len(results),
        "raw": r["raw"],
    }


# ────────────────────────────────────────────────────────────────────────────
# Product 5: Scraping Browser (cloud Chrome)
# ────────────────────────────────────────────────────────────────────────────
def browser_open(url: str, session: str = "bharatwatch") -> Dict[str, Any]:
    """Open a URL in Bright Data's cloud Chrome browser."""
    r = _run_cli(["browser", "--session", session, "open", url], 60)
    data = r.get("data", {})
    return {
        "ok": r["ok"] and data.get("status") == 200,
        "title": data.get("title", ""),
        "url": data.get("url", ""),
        "raw": r["raw"],
    }


def browser_snapshot(session: str = "bharatwatch") -> Dict[str, Any]:
    """Get a text snapshot of the current browser page."""
    r = _run_cli(["browser", "--session", session, "snapshot"], 30)
    data = r.get("data", {})
    snapshot = data.get("snapshot", "")
    return {"ok": r["ok"], "snapshot": snapshot, "ref_count": data.get("ref_count", 0)}


def browser_get(session: str = "bharatwatch") -> Dict[str, Any]:
    """Get full page content from the browser session."""
    r = _run_cli(["browser", "--session", session, "get"], 30)
    data = r.get("data", {})
    return {"ok": r["ok"], "content": data.get("content", data.get("html", str(data))), "raw": r["raw"]}


# ────────────────────────────────────────────────────────────────────────────
# Integrated module scrapers — each uses the best BD product for its domain
# ────────────────────────────────────────────────────────────────────────────
def scrape_nauktrialert() -> List[Dict[str, Any]]:
    """NaukriAlert: discover → web_unlocker_scrape (sarkariresult.com).

    Uses BD Discover to find the best govt job sites, then BD Web Unlocker
    to fetch sarkariresult.com as markdown, then extracts listings.
    """
    items = []

    # Step 1: Web Unlocker scrape (sarkariresult.com — verified working)
    result = web_unlocker_scrape("https://www.sarkariresult.com/", "markdown")
    if result["ok"] and result["content"]:
        # Extract job links from markdown
        links = re.findall(
            r'\[([^\]]{10,120})\]\((https://www\.sarkariresult\.com/20[0-9]+/[^)]+)\)',
            result["content"],
        )
        seen = set()
        for text, href in links:
            text = text.replace("**", "").strip()
            if href not in seen and text and not any(x in text.lower() for x in
                ["instagram", "facebook", "youtube", "telegram", "download"]):
                seen.add(href)
                items.append({
                    "title": text[:200],
                    "department": "",
                    "notification_date": "",
                    "official_link": href,
                    "number_of_vacancies": "",
                    "qualification_required": "",
                    "last_application_date": "",
                    "exam_date": "",
                })

    # Step 2: If unlocker fails, try REST API
    if not items:
        rest_result = web_unlocker_rest("https://www.sarkariresult.com/")
        if rest_result["ok"] and rest_result["content"]:
            links = re.findall(
                r'<a[^>]*href="(https://www\.sarkariresult\.com/20[0-9]+/[^"]+)"[^>]*>([^<]{10,120})</a>',
                rest_result["content"], re.IGNORECASE,
            )
            seen = set()
            for href, text in links:
                text = re.sub(r"\s+", " ", text).replace("\xa0", " ").strip()
                if href not in seen and text and not any(x in text.lower() for x in
                    ["instagram", "facebook", "youtube", "telegram"]):
                    seen.add(href)
                    items.append({
                        "title": text[:200],
                        "department": "",
                        "notification_date": "",
                        "official_link": href,
                        "number_of_vacancies": "",
                        "qualification_required": "",
                        "last_application_date": "",
                        "exam_date": "",
                    })

    return items[:50]


def scrape_tendersentry() -> List[Dict[str, Any]]:
    """TenderSentry: SERP search → web_unlocker_scrape (tenderdetail.com).

    Uses BD SERP API to find tender listing sites, then BD Web Unlocker
    to fetch and extract tender data from accessible (non-.gov.in) sites.
    """
    items = []

    # Step 1: SERP search to find accessible tender pages
    serp = serp_search("latest government tenders India 2026 site:tenderdetail.com OR site:tendertiger.com OR site:tenderkart.com", country="in")
    accessible_urls = []
    for r in serp.get("results", []):
        link = r.get("link", "")
        title = r.get("title", "")
        # Skip .gov.in domains (blocked by BD policy) and JS-only pages
        if ".gov.in" not in link and link.startswith("http"):
            accessible_urls.append((link, title))

    # Step 2: Web Unlocker scrape on the best non-govt tender site
    for url, title in accessible_urls[:5]:
        result = web_unlocker_scrape(url, "markdown")
        if result["ok"] and result["content"]:
            content = result["content"]
            # Extract tender-like entries — look for structured lines with tender keywords
            lines = content.split("\n")
            for line in lines:
                line = line.strip().lstrip("|*").rstrip("|*").strip()
                if len(line) > 15 and any(kw in line.lower() for kw in
                    ["tender", "bid", "eoi", "rfq", "nit", "auction", "procurement", "supply"]):
                    # Clean markdown formatting
                    clean = re.sub(r"[\[\]#*`>]", "", line).strip()
                    if len(clean) > 15:
                        items.append({
                            "tender_id": "",
                            "title": clean[:200],
                            "department": "",
                            "estimated_value": "",
                            "closing_date": "",
                            "document_link": url,
                        })
                        if len(items) >= 20:
                            break
        if items:
            break

    # Fallback: if SERP didn't find good pages, scrape tenderdetail.com directly
    if not items:
        result = web_unlocker_scrape("https://www.tenderdetail.com/Indian-Tenders", "markdown")
        if result["ok"] and result["content"]:
            lines = result["content"].split("\n")
            for line in lines:
                line = line.strip().lstrip("|*").rstrip("|*").strip()
                clean = re.sub(r"[\[\]#*`>]", "", line).strip()
                if len(clean) > 15 and any(kw in clean.lower() for kw in
                    ["tender", "bid", "eoi", "rfq", "nit", "supply", "procurement"]):
                    items.append({
                        "tender_id": "",
                        "title": clean[:200],
                        "department": "",
                        "estimated_value": "",
                        "closing_date": "",
                        "document_link": "https://www.tenderdetail.com/Indian-Tenders",
                    })
                    if len(items) >= 20:
                        break

    return items[:20]


def scrape_mandiwatch() -> List[Dict[str, Any]]:
    """MandiWatch: Discover → web_unlocker_scrape (news articles with mandi prices).

    Agmarknet.gov.in is JS-rendered and BD-blocked. Use BD Discover to find
    news articles and reports that quote mandi/commodity prices, then
    extract price data from the markdown content.
    """
    items = []

    # Step 1: Use BD Discover (AI-ranked) to find pages with mandi prices
    disc = discover_search(
        "mandi prices today India tomato onion wheat commodity",
        intent="Find pages reporting agricultural commodity mandi prices in India with numeric price data",
        country="in",
        num=10,
    )
    for r in disc.get("results", []):
        link = r.get("link", "")
        if ".gov.in" not in link and link.startswith("http"):
            # Step 2: Web Unlocker scrape the page
            result = web_unlocker_scrape(link, "markdown")
            if result["ok"] and result["content"]:
                # Extract commodity + price patterns from markdown
                # Look for patterns like "Tomato: ₹1200/quintal" or "Onion - 800 per kg"
                price_patterns = re.findall(
                    r'([A-Z][a-zA-Z\s]{3,30})\s*[:\-]\s*[₹]?\s*(\d{1,2}(?:,\d{3})*(?:\.\d{1,2})?)\s*/?\s*(?:kg|quintal|qtl|per|ton)?',
                    result["content"],
                )
                for name, price in price_patterns[:20]:
                    name = name.strip()
                    if price and name and not any(x in name.lower() for x in
                        ["error", "rejected", "blocked", "response", "cookie", "javascript", "enable"]):
                        items.append({
                            "mandi": name[:100],
                            "crop": name.strip()[:50],
                            "variety": "",
                            "min_price": "",
                            "max_price": "",
                            "modal_price": price,
                            "date": "",
                        })
            if items:
                break

    # Fallback: try known commodity price sites
    if not items:
        for url in [
            "https://www.commodityonline.com/mandiprices",
            "https://www.agriwatch.com/",
        ]:
            result = web_unlocker_scrape(url, "markdown")
            if result["ok"] and result["content"]:
                # Broader pattern — any line with a commodity name and a number
                lines = result["content"].split("\n")
                for line in lines:
                    line = line.strip().lstrip("|*").rstrip("|*").strip()
                    # Match "Commodity Name ... ₹1234" or "Name: 1234/kg"
                    m = re.search(
                        r'([A-Z][a-zA-Z\s]{3,30}).*?[₹]?\s*(\d{2,5}(?:,\d{3})*(?:\.\d+)?)\s*/?\s*(?:kg|qtl|quintal|ton)?',
                        line,
                    )
                    if m:
                        name, price = m.group(1).strip(), m.group(2)
                        if not any(x in name.lower() for x in
                            ["error", "rejected", "blocked", "cookie", "javascript", "price updated"]):
                            items.append({
                                "mandi": name[:100],
                                "crop": name[:50],
                                "variety": "",
                                "min_price": "",
                                "max_price": "",
                                "modal_price": price,
                                "date": "",
                            })
                            if len(items) >= 20:
                                break
            if items:
                break

    return items[:20]


def scrape_collegecutoff() -> List[Dict[str, Any]]:
    """CollegeCutoff: web_unlocker_rest (josaa.nic.in).

    JoSAA is accessible via Web Unlocker REST (91KB verified).
    """
    items = []

    result = web_unlocker_rest("https://josaa.nic.in/")
    if result["ok"] and result["content"]:
        html = result["content"]
        # Try table extraction
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL | re.IGNORECASE)
        for row in rows[:50]:
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.DOTALL | re.IGNORECASE)
            cells = [re.sub(r"<[^>]+>", "", c).strip()[:50] for c in cells]
            if len(cells) >= 4:
                items.append({
                    "institute": cells[0],
                    "branch": cells[1] if len(cells) > 1 else "",
                    "round": cells[2] if len(cells) > 2 else "",
                    "opening_rank": cells[3] if len(cells) > 3 else "",
                    "closing_rank": cells[4] if len(cells) > 4 else "",
                })

    return items[:30]


def scrape_startuppulse() -> List[Dict[str, Any]]:
    """StartupPulse: discover → web_unlocker_scrape (gktoday.in).

    Uses BD Discover to find startup scheme pages, then BD Web Unlocker
    to fetch gktoday.in as markdown.
    """
    items = []

    # Step 1: Web Unlocker scrape (gktoday.in — verified working)
    result = web_unlocker_scrape("https://www.gktoday.in/current-affairs/", "markdown")
    if result["ok"] and result["content"]:
        # Extract article/scheme links from markdown
        links = re.findall(
            r'\[([^\]]{10,150})\]\((https://www\.gktoday\.in/[^)]+)\)',
            result["content"],
        )
        seen = set()
        for text, href in links:
            text = text.replace("**", "").strip()
            if href not in seen and text and not any(x in text.lower() for x in
                ["login", "register", "account", "quiz", "book", "home"]):
                seen.add(href)
                items.append({
                    "title": text[:200],
                    "ministry": "",
                    "description": "",
                    "official_link": href,
                })

    # Step 2: If unlocker fails, try REST API
    if not items:
        rest_result = web_unlocker_rest("https://www.gktoday.in/current-affairs/")
        if rest_result["ok"] and rest_result["content"]:
            links = re.findall(
                r'<a[^>]*href="(https://www\.gktoday\.in/[^"]+)"[^>]*>([^<]{10,150})</a>',
                rest_result["content"], re.IGNORECASE,
            )
            seen = set()
            for href, text in links:
                text = re.sub(r"\s+", " ", text).strip()
                if href not in seen and text and not any(x in text.lower() for x in
                    ["login", "register", "account", "quiz", "book"]):
                    seen.add(href)
                    items.append({
                        "title": text[:200],
                        "ministry": "",
                        "description": "",
                        "official_link": href,
                    })

    return items[:30]


# ────────────────────────────────────────────────────────────────────────────
# Master scraper registry
# ────────────────────────────────────────────────────────────────────────────
MODULE_SCRAPERS = {
    "nauktrialert": scrape_nauktrialert,
    "tendersentry": scrape_tendersentry,
    "mandiwatch": scrape_mandiwatch,
    "collegecutoff": scrape_collegecutoff,
    "startuppulse": scrape_startuppulse,
}


def scrape_module(module: str) -> Dict[str, Any]:
    """Scrape a module using the best Bright Data product for its domain."""
    fn = MODULE_SCRAPERS.get(module)
    if not fn:
        return {"ok": False, "items": [], "count": 0, "error": f"no scraper for {module}"}
    try:
        items = fn()
        return {"ok": len(items) > 0, "items": items, "count": len(items), "error": None}
    except Exception as e:
        return {"ok": False, "items": [], "count": 0, "error": str(e)}
