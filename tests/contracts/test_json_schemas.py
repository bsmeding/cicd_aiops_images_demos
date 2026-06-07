"""Structured output contract tests — no LLM, no secrets required."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

SCHEMAS_DIR = Path(__file__).parent.parent.parent / "schemas"


def _all_schemas():
    return list(SCHEMAS_DIR.glob("*.json"))


@pytest.mark.parametrize("schema_file", _all_schemas(), ids=lambda p: p.stem)
def test_schema_is_valid_draft2020(schema_file: Path) -> None:
    schema = json.loads(schema_file.read_text())
    Draft202012Validator.check_schema(schema)


def test_incident_triage_schema_has_required_fields() -> None:
    schema_file = SCHEMAS_DIR / "incident_triage.json"
    schema = json.loads(schema_file.read_text())
    required = schema.get("required", [])
    assert "severity" in required
    assert "summary" in required
    assert "recommended_action" in required


def test_incident_triage_severity_is_enum() -> None:
    schema_file = SCHEMAS_DIR / "incident_triage.json"
    schema = json.loads(schema_file.read_text())
    severity_def = schema["properties"]["severity"]
    assert "enum" in severity_def
    assert set(severity_def["enum"]) == {"low", "medium", "high", "critical"}


def test_device_lookup_schema_has_required_fields() -> None:
    schema_file = SCHEMAS_DIR / "device_lookup.json"
    schema = json.loads(schema_file.read_text())
    required = schema.get("required", [])
    assert "name" in required
    assert "site" in required


def test_incident_triage_sample_validates() -> None:
    schema_file = SCHEMAS_DIR / "incident_triage.json"
    schema = json.loads(schema_file.read_text())
    validator = Draft202012Validator(schema)
    sample = {
        "severity": "high",
        "summary": "BGP sessions down on edge-ams1",
        "recommended_action": "Check BGP neighbor state and routing tables.",
    }
    errors = list(validator.iter_errors(sample))
    assert not errors, errors
