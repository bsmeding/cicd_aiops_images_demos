#!/usr/bin/env python3
"""Quick LiteLLM smoke check — used as a standalone CI step.

Exits 0 on success, 1 on any failure.
"""
from __future__ import annotations

import os
import sys

from litellm import completion


def smoke(model: str, api_key_env: str) -> bool:
    if not os.getenv(api_key_env):
        print(f"  SKIP  {model}  ({api_key_env} not set)")
        return True

    try:
        response = completion(
            model=model,
            messages=[
                {"role": "system", "content": "Answer in one sentence."},
                {"role": "user", "content": "What is NetDevOps?"},
            ],
        )
        content = response.choices[0].message.content
        assert content and len(content) > 5
        print(f"  OK    {model}  — {content[:80]!r}")
        return True
    except Exception as exc:
        print(f"  FAIL  {model}  — {exc}")
        return False


def main() -> None:
    checks = [
        ("gpt-4o-mini", "OPENAI_API_KEY"),
        ("claude-haiku-4-5-20251001", "ANTHROPIC_API_KEY"),
    ]
    results = [smoke(model, key) for model, key in checks]
    if not all(results):
        sys.exit(1)
    print("All smoke checks passed.")


if __name__ == "__main__":
    main()
