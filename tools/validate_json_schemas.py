#!/usr/bin/env python3
"""Stand-alone JSON Schema validator — used as a CI step before tests.

Usage:
    python tools/validate_json_schemas.py schemas/
    python tools/validate_json_schemas.py schemas/incident_triage.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def validate_file(path: Path) -> bool:
    try:
        schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(schema)
        print(f"  OK    {path}")
        return True
    except Exception as exc:
        print(f"  FAIL  {path}  — {exc}")
        return False


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate_json_schemas.py <path>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if target.is_dir():
        files = list(target.glob("*.json"))
    else:
        files = [target]

    if not files:
        print(f"No JSON schema files found in {target}")
        sys.exit(0)

    results = [validate_file(f) for f in files]
    if not all(results):
        print(f"\n{results.count(False)}/{len(results)} schemas failed.")
        sys.exit(1)
    print(f"\nAll {len(results)} schemas valid.")


if __name__ == "__main__":
    main()
