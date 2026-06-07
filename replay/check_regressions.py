#!/usr/bin/env python3
"""Assert no regressions in replay results.

Usage:
    python replay/check_regressions.py build/replay-results.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: check_regressions.py <results.json>")
        sys.exit(1)

    path = Path(sys.argv[1])
    data = json.loads(path.read_text())

    failed = data.get("failed", 0)
    total = data.get("passed", 0) + failed

    print(f"Replay results: {data['passed']}/{total} passed")

    if failed:
        print("\nFailed records:")
        for rec in data.get("records", []):
            if not rec.get("passed"):
                print(f"  {rec['id']}: expected={rec.get('expected_label')!r}  got={rec['result']['label']!r}")
                print(f"    message: {rec['message']!r}")
        sys.exit(1)

    print("No regressions.")


if __name__ == "__main__":
    main()
