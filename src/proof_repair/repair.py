"""Bounded compiler-feedback loop for LLM-generated Lean theorems."""

from __future__ import annotations

from typing import Protocol

from .generation import TextGenerator, formalization_prompt, repair_prompt, strip_code_fences
from .models import Attempt, BenchmarkItem, CheckResult


class Checker(Protocol):
    def check(self, source: str) -> CheckResult: ...


class RepairEngine:
    """Generate once, then repair from diagnostics until success or budget exhaustion."""

    def __init__(self, generator: TextGenerator, checker: Checker, max_repairs: int = 3):
        if max_repairs < 0:
            raise ValueError("max_repairs must be non-negative")
        self.generator = generator
        self.checker = checker
        self.max_repairs = max_repairs

    def run(self, item: BenchmarkItem) -> list[Attempt]:
        source = strip_code_fences(self.generator.complete(formalization_prompt(item)))
        attempts: list[Attempt] = []
        for round_number in range(self.max_repairs + 1):
            result = self.checker.check(source)
            phase = "formalize" if round_number == 0 else "repair"
            attempts.append(Attempt(item.id, phase, source, result, round_number))
            if result.accepted or round_number == self.max_repairs:
                break
            source = strip_code_fences(
                self.generator.complete(repair_prompt(source, result.diagnostics))
            )
        return attempts
