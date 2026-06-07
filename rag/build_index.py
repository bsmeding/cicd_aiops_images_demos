#!/usr/bin/env python3
"""Build a lightweight in-memory BM25 index from markdown runbooks.

This is intentionally simple — no external vector store required.
For demo and CI purposes only.

Usage:
    python rag/build_index.py --source docs/runbooks --output build/index
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def chunk_markdown(text: str, chunk_size: int = 300) -> list[str]:
    words = text.split()
    return [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def build(source_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    index = []

    for md_file in sorted(source_dir.glob("**/*.md")):
        text = md_file.read_text()
        chunks = chunk_markdown(text)
        for i, chunk in enumerate(chunks):
            index.append({
                "id": f"{md_file.stem}:{i}",
                "path": str(md_file),
                "text": chunk,
            })

    index_path = output_dir / "index.json"
    index_path.write_text(json.dumps(index, indent=2))
    print(f"Built index with {len(index)} chunks → {index_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="docs/runbooks")
    parser.add_argument("--output", default="build/index")
    args = parser.parse_args()

    build(Path(args.source), Path(args.output))


if __name__ == "__main__":
    main()
