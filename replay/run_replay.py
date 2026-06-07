#!/usr/bin/env python3
"""Run incident replay and write results to JSON.

Usage:
    python replay/run_replay.py replay/incidents/*.jsonl --output build/replay-results.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def classify(record: dict[str, Any]) -> dict[str, Any]:
    text = (record.get("message") or "").lower()
    if "bgp" in text:
        return {"label": "bgp_issue", "severity": "high", "tool": "nautobot_get_device"}
    if "interface" in text and "down" in text:
        return {"label": "interface_down", "severity": "medium", "tool": "nautobot_get_interfaces"}
    return {"label": "unknown", "severity": "low", "tool": None}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--output", default="build/replay-results.json")
    args = parser.parse_args()

    results = []
    passed = failed = 0

    for pattern in args.files:
        for fpath in sorted(Path(".").glob(pattern) if "*" in pattern else [Path(pattern)]):
            for rec in load_jsonl(fpath):
                result = classify(rec)
                expected = rec.get("expected_label")
                ok = result["label"] == expected
                if ok:
                    passed += 1
                else:
                    failed += 1
                results.append({**rec, "result": result, "passed": ok})

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"passed": passed, "failed": failed, "records": results}, indent=2))

    print(f"Replay: {passed} passed, {failed} failed → {output}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
