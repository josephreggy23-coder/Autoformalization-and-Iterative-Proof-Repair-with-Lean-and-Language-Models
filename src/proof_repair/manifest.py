"""Versioned provenance records for reproducible proof-repair experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class ExperimentManifest:
    """The non-secret settings needed to interpret an attempt artifact."""

    experiment_id: str
    benchmark_path: str
    benchmark_split: str
    model_id: str
    prompt_version: str
    max_repairs: int
    verifier_command: str
    seed: int | None = None

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must not be empty")
        if self.max_repairs < 0:
            raise ValueError("max_repairs must be non-negative")


def write_manifest(path: str | Path, manifest: ExperimentManifest) -> None:
    """Write stable, reviewable JSON without storing API keys or prompts secrets."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(asdict(manifest), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
