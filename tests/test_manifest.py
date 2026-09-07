import json
import tempfile
import unittest
from pathlib import Path

from proof_repair.manifest import ExperimentManifest, write_manifest


class ManifestTests(unittest.TestCase):
    def test_writes_non_secret_reproducibility_record(self):
        manifest = ExperimentManifest(
            "baseline-001", "data/benchmark.jsonl", "test", "example-model",
            "formalize-v1", 3, "lake env lean", seed=7,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            write_manifest(path, manifest)
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["model_id"], "example-model")
        self.assertNotIn("api_key", payload)
