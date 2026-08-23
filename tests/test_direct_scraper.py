"""Tests for the direct scraper fallback module."""
import pytest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bharatwatch.core import direct_scraper


def test_extraction_rules_have_all_modules():
    """Every module should have extraction rules defined."""
    expected = {"nauktrialert", "tendersentry", "mandiwatch", "collegecutoff", "startuppulse"}
    assert expected.issubset(set(direct_scraper.EXTRACTION_RULES.keys()))


def test_extraction_rules_have_item_selectors():
    """Each module's rules must have an 'item' selector."""
    for module, rules in direct_scraper.EXTRACTION_RULES.items():
        assert "selectors" in rules, f"{module} missing selectors"
        assert "item" in rules["selectors"], f"{module} missing item selector"


def test_site_registry_has_real_urls():
    """Site registry should have at least nauktrialert with real URLs."""
    from bharatwatch.core.site_extractors import SITE_REGISTRY
    assert "nauktrialert" in SITE_REGISTRY
    urls = SITE_REGISTRY["nauktrialert"]["urls"]
    assert len(urls) >= 1
    assert urls[0][0].startswith("https://")  # real URL
    assert callable(urls[0][1])  # extractor function


def test_scrape_with_curl_handles_empty_response():
    """curl scraper should handle empty/blocked responses gracefully."""
    fake = MagicMock()
    fake.returncode = 0
    fake.stdout = ""
    with patch("subprocess.run", return_value=fake):
        result = direct_scraper.scrape_with_curl("https://example.com", "nauktrialert")
    assert result["ok"] is False
    assert "empty" in result["error"]


def test_scrape_with_brightdata_unlocker_no_key():
    """Unlocker should fail gracefully when no API key is found."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = direct_scraper.scrape_with_brightdata_unlocker("https://example.com", "nauktrialert")
    assert result["ok"] is False
    assert "api key" in result["error"].lower()
