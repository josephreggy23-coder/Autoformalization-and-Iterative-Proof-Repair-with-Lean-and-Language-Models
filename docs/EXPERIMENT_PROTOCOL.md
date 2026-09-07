# Experiment reporting protocol

Use this checklist before reporting a model result from this repository.

## 1. Freeze the inputs

- Commit the benchmark JSONL and record its path and selected split.
- Record the exact model identifier, prompt version, repair budget, and seed in
  an `ExperimentManifest`.
- Record the Lean/Mathlib command used by the verifier.

## 2. Preserve every attempt

Write the complete `Attempt` sequence with `write_attempts`. Do not retain only
accepted proofs: rejected sources and Lean diagnostics are required to explain
what repair did or did not improve.

## 3. Report example-level metrics

Always state all of the following:

| Metric | Meaning |
| --- | --- |
| Examples | Unique theorem IDs evaluated |
| Initial success rate | Accepted before any repair |
| Eventual success rate | Accepted within the fixed repair budget |
| Repaired successes | Examples rescued after an initial rejection |
| Repair budget | Maximum extra generations allowed |
| Verifier environment | Lean and Mathlib command/version |

Do not label a manual proof, reference theorem, or controlled negative example
as a model result.

## 4. Include a compact result table

```text
configuration: <model + prompt + verifier>
split: <dev or test>; examples: <n>; repair budget: <k>
initial: <x/n>; eventual: <y/n>; repaired: <y-x>
artifact: artifacts/<experiment-id>/attempts.jsonl
manifest: artifacts/<experiment-id>/manifest.json
```

This template makes the result traceable without exposing API keys or private
provider configuration.
