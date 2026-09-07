import tempfile
import unittest
from pathlib import Path

from proof_repair.benchmark import load_benchmark


class BenchmarkTests(unittest.TestCase):
    def test_loads_curated_examples(self):
        items = load_benchmark("data/benchmark.jsonl")
        self.assertEqual([item.id for item in items], ["nat_add_zero", "even_square", "zero_mul", "subset_refl"])

    def test_rejects_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_text(
                '{"id":"x","split":"dev","natural_language":"a","reference_statement":"b"}\n'
                '{"id":"x","split":"test","natural_language":"a","reference_statement":"b"}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate"):
                load_benchmark(path)
