"""Tests for the Bright Data multi-product scraper module."""
import pytest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bharatwatch.core import brightdata_scrape


def test_module_scrapers_registered():
    """All 5 modules should have scraper functions."""
    expected = {"nauktrialert", "tendersentry", "mandiwatch", "collegecutoff", "startuppulse"}
    assert expected.issubset(set(brightdata_scrape.MODULE_SCRAPERS.keys()))


def test_scrape_module_unknown_returns_error():
    """Unknown module should return error."""
    r = brightdata_scrape.scrape_module("nonexistent")
    assert r["ok"] is False
    assert "no scraper" in r["error"]


def test_get_api_key_missing():
    """Should return empty string when credentials file doesn't exist."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        key = brightdata_scrape._get_api_key()
    assert key == ""


def test_run_cli_parses_json():
    """_run_cli should parse JSON from CLI output."""
    fake = MagicMock()
    fake.returncode = 0
    fake.stdout = '{"status":"done","data":"test"}\n'
    fake.stderr = ""
    with patch("subprocess.run", return_value=fake):
        r = brightdata_scrape._run_cli(["scrape", "https://example.com"], 30)
    assert r["ok"] is True
    assert r["data"]["status"] == "done"


def test_run_cli_handles_timeout():
    """_run_cli should handle timeout gracefully."""
    import subprocess
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("npx", 30)):
        r = brightdata_scrape._run_cli(["scrape", "https://example.com"], 30)
    assert r["ok"] is False
    assert "timeout" in r["raw"]


def test_scraper_run_extracts_items():
    """scraper_run should extract items from CLI output."""
    fake = MagicMock()
    fake.returncode = 0
    fake.stdout = '[{"title":"Test Job","company":"Test Co"}]\n'
    fake.stderr = ""
    with patch("subprocess.run", return_value=fake):
        r = brightdata_scrape.scraper_run("c_test", "https://example.com")
    assert r["ok"] is True
    assert r["count"] == 1
    assert r["items"][0]["title"] == "Test Job"


def test_web_unlocker_scrape_extracts_content():
    """web_unlocker_scrape should return content from CLI."""
    fake = MagicMock()
    fake.returncode = 0
    fake.stdout = '{"content":"# Page Title\\n\\nSome markdown content"}\n'
    fake.stderr = ""
    with patch("subprocess.run", return_value=fake):
        r = brightdata_scrape.web_unlocker_scrape("https://example.com", "markdown")
    assert r["ok"] is True
    assert "markdown content" in r["content"]


def test_serp_search_extracts_organic():
    """serp_search should extract organic results."""
    fake = MagicMock()
    fake.returncode = 0
    fake.stdout = '{"organic":[{"title":"Test","link":"https://example.com"}]}\n'
    fake.stderr = ""
    with patch("subprocess.run", return_value=fake):
        r = brightdata_scrape.serp_search("test query", country="in")
    assert r["ok"] is True
    assert r["count"] == 1
    assert r["results"][0]["title"] == "Test"
