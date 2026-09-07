"""Artifact writing and transparent aggregate metrics."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from .models import Attempt


def summarize(attempts: Iterable[Attempt]) -> dict[str, float | int]:
    """Report verification outcomes without equating attempts with examples."""
    by_item: dict[str, list[Attempt]] = defaultdict(list)
    for attempt in attempts:
        by_item[attempt.item_id].append(attempt)
    total = len(by_item)
    initially_accepted = sum(records[0].check.accepted for records in by_item.values())
    eventually_accepted = sum(any(a.check.accepted for a in records) for records in by_item.values())
    repaired = eventually_accepted - initially_accepted
    return {
        "examples": total,
        "initial_successes": initially_accepted,
        "eventual_successes": eventually_accepted,
        "repaired_successes": repaired,
        "initial_success_rate": initially_accepted / total if total else 0.0,
        "eventual_success_rate": eventually_accepted / total if total else 0.0,
    }


def write_attempts(path: str | Path, attempts: Iterable[Attempt]) -> None:
    """Persist append-free JSONL artifacts suitable for later auditing."""
    lines = []
    for attempt in attempts:
        lines.append(json.dumps({
            "item_id": attempt.item_id, "phase": attempt.phase,
            "round": attempt.round, "source": attempt.source,
            "accepted": attempt.check.accepted,
            "diagnostics": attempt.check.diagnostics,
            "elapsed_seconds": attempt.check.elapsed_seconds,
            "metadata": attempt.metadata,
        }, ensure_ascii=False))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
