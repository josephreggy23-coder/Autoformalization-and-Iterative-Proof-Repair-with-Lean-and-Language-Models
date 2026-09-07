"""Loading and validating the local JSONL benchmark."""

from __future__ import annotations

import json
from pathlib import Path

from .models import BenchmarkItem


def load_benchmark(path: str | Path) -> list[BenchmarkItem]:
    """Load benchmark items, rejecting duplicate IDs and malformed records."""
    items: list[BenchmarkItem] = []
    seen: set[str] = set()
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        required = {"id", "split", "natural_language", "reference_statement"}
        missing = required - record.keys()
        if missing:
            raise ValueError(f"line {number}: missing {sorted(missing)}")
        if record["id"] in seen:
            raise ValueError(f"line {number}: duplicate id {record['id']}")
        if record["split"] not in {"dev", "test"}:
            raise ValueError(f"line {number}: invalid split")
        seen.add(record["id"])
        items.append(BenchmarkItem(
            id=record["id"], split=record["split"],
            natural_language=record["natural_language"],
            reference_statement=record["reference_statement"],
            tags=tuple(record.get("tags", [])),
        ))
    return items
