"""Provider-neutral LLM interface and prompts for Lean generation."""

from __future__ import annotations

from typing import Protocol

from .models import BenchmarkItem


class TextGenerator(Protocol):
    """The only capability required from an LLM provider."""

    def complete(self, prompt: str) -> str: ...


FORMALIZE_INSTRUCTIONS = """You formalize elementary mathematics in Lean 4 with Mathlib.
Return only a complete `theorem target ... := by ...` declaration. Do not use
markdown fences, explanations, `sorry`, or `admit`."""

REPAIR_INSTRUCTIONS = """You repair a Lean 4 theorem using compiler feedback.
Return only a complete replacement `theorem target ... := by ...` declaration.
Preserve the intended theorem, do not use `sorry` or `admit`, and make the
smallest valid change you can."""


def formalization_prompt(item: BenchmarkItem) -> str:
    return f"{FORMALIZE_INSTRUCTIONS}\n\nEnglish theorem:\n{item.natural_language}\n"


def proof_prompt(statement: str) -> str:
    return f"{FORMALIZE_INSTRUCTIONS}\n\nProve this Lean statement:\n{statement}\n"


def repair_prompt(source: str, diagnostics: str) -> str:
    return f"{REPAIR_INSTRUCTIONS}\n\nCurrent source:\n{source}\n\nCompiler feedback:\n{diagnostics}\n"


def strip_code_fences(text: str) -> str:
    """Normalize a common model formatting mistake without changing Lean code."""
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        return "\n".join(lines[1:-1]).strip()
    return text
