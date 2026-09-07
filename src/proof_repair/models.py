"""Typed records shared by generation, verification, and evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class BenchmarkItem:
    """A natural-language theorem and its reference Lean statement."""

    id: str
    split: Literal["dev", "test"]
    natural_language: str
    reference_statement: str
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class CheckResult:
    """Result returned by a proof assistant invocation."""

    accepted: bool
    diagnostics: str = ""
    elapsed_seconds: float = 0.0


@dataclass(frozen=True)
class Attempt:
    """One generated Lean artifact and the outcome of checking it."""

    item_id: str
    phase: Literal["formalize", "prove", "repair"]
    source: str
    check: CheckResult
    round: int = 0
    metadata: dict[str, str] = field(default_factory=dict)
