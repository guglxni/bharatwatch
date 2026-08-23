"""Tests for the closed-loop self-healing engine.

These mock the Bright Data CLI subprocess so no network/credentials are needed.
"""
import json
import pytest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bharatwatch.core import healer


# --------------------------------------------------------------------------- #
# _run_cli JSON-envelope parsing
# --------------------------------------------------------------------------- #
def test_run_cli_parses_json_envelope():
    fake = MagicMock()
    fake.returncode = 0
    fake.stdout = 'some log line\n{"collector_id":"c_123","status":"done"}\n'
    fake.stderr = ""
    with patch("subprocess.run", return_value=fake):
        ok, parsed, raw = healer._run_cli(["scraper", "heal", "c_123", "x"], 60)
    assert ok is True
    assert parsed["status"] == "done"
    assert parsed["collector_id"] == "c_123"


def test_run_cli_handles_nonzero_exit():
    fake = MagicMock()
    fake.returncode = 1
    fake.stdout = ""
    fake.stderr = "boom"
    with patch("subprocess.run", return_value=fake):
        ok, parsed, raw = healer._run_cli(["scraper", "heal", "c_123", "x"], 60)
    assert ok is False
    assert parsed == {}
    assert "boom" in raw


def test_run_cli_timeout():
    with patch("subprocess.run", side_effect=healer.subprocess.TimeoutExpired("npx", 60)):
        ok, parsed, raw = healer._run_cli(["scraper", "heal"], 60)
    assert ok is False
    assert "timeout" in raw


# --------------------------------------------------------------------------- #
# heal_collector: auto-approve + auto-save flags + status mapping
# --------------------------------------------------------------------------- #
def test_heal_collector_done_maps_to_ok():
    with patch.object(healer, "_run_cli",
                      return_value=(True, {"status": "done"}, "")) as m:
        res = healer.heal_collector("c_1", "fix it", "https://x")
    assert res["ok"] is True
    assert res["status"] == "done"
    # confirm auto-approve + auto-save flags are passed to the CLI
    args = m.call_args[0][0]
    assert "--auto-approve" in args and "--auto-save" in args


def test_heal_collector_failed_maps_to_not_ok():
    with patch.object(healer, "_run_cli",
                      return_value=(False, {"status": "failed"}, "err")):
        res = healer.heal_collector("c_1", "fix it")
    assert res["ok"] is False


# --------------------------------------------------------------------------- #
# run_collector: item extraction from various envelope shapes
# --------------------------------------------------------------------------- #
def test_run_collector_extracts_data_list():
    parsed = {"data": [{"a": 1}, {"a": 2}]}
    with patch.object(healer, "_run_cli", return_value=(True, parsed, "")):
        res = healer.run_collector("c_1", "https://x")
    assert res["count"] == 2
    assert res["ok"] is True


def test_run_collector_extracts_nested_list():
    parsed = {"output": {"rows": [{"a": 1}]}}
    with patch.object(healer, "_run_cli", return_value=(True, parsed, "")):
        res = healer.run_collector("c_1", "https://x")
    assert res["count"] == 1


# --------------------------------------------------------------------------- #
# build_heal_prompt: context-aware from last good snapshot
# --------------------------------------------------------------------------- #
def _make_source(db):
    from bharatwatch.core.models import Source
    s = Source(module="nauktrialert", name="Test", url="https://x",
               collector_id="c_1", health="broken")
    db.add(s)
    db.commit()
    return s


def test_build_heal_prompt_uses_last_good_fields(tmp_path, monkeypatch):
    # use an isolated in-memory-ish db
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from bharatwatch.core.models import Base, Snapshot

    engine = create_engine(f"sqlite:///{tmp_path}/t.db")
    Base.metadata.create_all(engine)
    S = sessionmaker(bind=engine)
    db = S()
    s = _make_source(db)
    db.add(Snapshot(source_id=s.id, status="ok",
                    raw_json=[{"title": "T", "department": "D", "vacancies": "5"}],
                    hash="h"))
    db.commit()

    prompt = healer.build_heal_prompt(s, db, last_error="empty output")
    assert "title" in prompt and "department" in prompt
    assert "empty output" in prompt
    assert "https://x" in prompt
    assert len(prompt) <= 1000
    db.close()


def test_build_heal_prompt_without_snapshot_stays_generic(tmp_path):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from bharatwatch.core.models import Base

    engine = create_engine(f"sqlite:///{tmp_path}/t.db")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    s = _make_source(db)
    prompt = healer.build_heal_prompt(s, db)
    assert "changed layout" in prompt
    assert "https://x" in prompt
    db.close()
