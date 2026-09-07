"""Lean-backed, timeout-bounded verification of generated theorem files."""

from __future__ import annotations

import os
import shlex
import subprocess
import tempfile
import time
from pathlib import Path

from .models import CheckResult


class LeanVerifier:
    """Check a complete Lean declaration in an isolated temporary file."""

    def __init__(self, command: str | None = None, timeout_seconds: float = 20.0):
        self.command = command or os.environ.get("LEAN_COMMAND", "lake env lean")
        self.timeout_seconds = timeout_seconds

    def check(self, source: str) -> CheckResult:
        if "sorry" in source or "admit" in source:
            return CheckResult(False, "Rejected: generated source contains sorry or admit.")
        started = time.monotonic()
        with tempfile.TemporaryDirectory(prefix="proof-repair-") as directory:
            path = Path(directory) / "Generated.lean"
            path.write_text("import Mathlib\n\n" + source + "\n", encoding="utf-8")
            try:
                completed = subprocess.run(
                    [*shlex.split(self.command, posix=False), str(path)],
                    text=True, capture_output=True, timeout=self.timeout_seconds,
                    check=False,
                )
            except FileNotFoundError:
                return CheckResult(False, f"Lean command not found: {self.command}")
            except subprocess.TimeoutExpired:
                return CheckResult(False, f"Lean timed out after {self.timeout_seconds:g} seconds.")
        elapsed = time.monotonic() - started
        diagnostics = (completed.stdout + completed.stderr).strip()
        return CheckResult(completed.returncode == 0, diagnostics, elapsed)
