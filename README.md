# Autoformalization and Iterative Proof Repair with Lean

A small, reproducible research scaffold for studying whether language models can
translate short mathematical statements into Lean and repair proofs from Lean
compiler feedback.

The project deliberately separates model generation from proof checking: Lean
is the source of truth for a successful proof, never an LLM self-assessment.

## Goals

1. Curate a transparent benchmark of elementary theorems.
2. Record every formalization and proof attempt.
3. Feed compiler diagnostics back into a bounded repair loop.
4. Report formalization and proof success separately.

## Quick start

```powershell
python -m unittest discover -s tests -v
python -m proof_repair.cli --help
```

To check real Lean files, install Lean 4 with Mathlib and pass its executable
path via `--lean-command` (or set `LEAN_COMMAND`).

## Status

The initial release contains a local JSONL benchmark, a provider-neutral model
interface, a Lean subprocess verifier, an iterative repair engine, and
evaluation/reporting tools. It does not claim model results without a configured
model and Lean environment.
