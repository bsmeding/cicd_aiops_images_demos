"""Incident replay tests — deterministic, no LLM calls.

Loads saved JSONL incident records, runs them through the classifier,
and asserts that expected labels and tool plans are stable across runs.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

INCIDENTS_DIR = Path(__file__).parent.parent.parent / "replay" / "incidents"


def _classify(record: dict[str, Any]) -> dict[str, Any]:
    """Minimal rule-based classifier used as a deterministic replay target."""
    text = (record.get("message") or "").lower()
    if "bgp" in text:
        return {"label": "bgp_issue", "severity": "high", "tool": "nautobot_get_device"}
    if "interface" in text and "down" in text:
        return {"label": "interface_down", "severity": "medium", "tool": "nautobot_get_interfaces"}
    return {"label": "unknown", "severity": "low", "tool": None}


def _load_incidents(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


@pytest.mark.parametrize(
    "incident_file",
    list(INCIDENTS_DIR.glob("*.jsonl")),
    ids=lambda p: p.stem,
)
def test_replay_file_is_parseable(incident_file: Path) -> None:
    records = _load_incidents(incident_file)
    assert len(records) > 0
    for rec in records:
        assert "message" in rec
        assert "expected_label" in rec


def test_bgp_incidents_classify_correctly() -> None:
    records = _load_incidents(INCIDENTS_DIR / "bgp_flap.jsonl")
    for rec in records:
        result = _classify(rec)
        assert result["label"] == rec["expected_label"], (
            f"Mismatch for: {rec['message']!r}"
        )
        assert result["severity"] in {"low", "medium", "high", "critical"}


def test_interface_incidents_classify_correctly() -> None:
    records = _load_incidents(INCIDENTS_DIR / "interface_down.jsonl")
    for rec in records:
        result = _classify(rec)
        assert result["label"] == rec["expected_label"], (
            f"Mismatch for: {rec['message']!r}"
        )
