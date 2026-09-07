"""Command-line entry points for inspecting the benchmark and checking Lean."""

from __future__ import annotations

import argparse
from pathlib import Path

from .benchmark import load_benchmark
from .verifier import LeanVerifier


def main() -> int:
    parser = argparse.ArgumentParser(description="Lean autoformalization research tools")
    parser.add_argument("--benchmark", default="data/benchmark.jsonl", help="benchmark JSONL path")
    parser.add_argument("--list-benchmark", action="store_true", help="print benchmark items")
    parser.add_argument("--check", type=Path, help="check a complete Lean theorem file")
    parser.add_argument("--lean-command", help="Lean command, e.g. 'lake env lean'")
    parser.add_argument("--timeout", type=float, default=20, help="checker timeout in seconds")
    args = parser.parse_args()

    if args.list_benchmark:
        for item in load_benchmark(args.benchmark):
            print(f"{item.id}\t{item.split}\t{', '.join(item.tags)}\t{item.natural_language}")
    if args.check:
        result = LeanVerifier(args.lean_command, args.timeout).check(
            args.check.read_text(encoding="utf-8")
        )
        print("accepted" if result.accepted else "rejected")
        if result.diagnostics:
            print(result.diagnostics)
        return 0 if result.accepted else 1
    if not args.list_benchmark and not args.check:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
