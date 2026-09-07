"""Loading and validating the local JSONL benchmark."""

from __future__ import annotations

import json
from collections import Counter
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


def benchmark_statistics(items: list[BenchmarkItem]) -> dict[str, object]:
    """Return transparent corpus counts for a benchmark report or experiment log."""
    split_counts = Counter(item.split for item in items)
    tag_counts = Counter(tag for item in items for tag in item.tags)
    return {
        "examples": len(items),
        "splits": dict(sorted(split_counts.items())),
        "tags": dict(sorted(tag_counts.items())),
        "mean_statement_characters": (
            sum(len(item.natural_language) for item in items) / len(items) if items else 0.0
        ),
    }
