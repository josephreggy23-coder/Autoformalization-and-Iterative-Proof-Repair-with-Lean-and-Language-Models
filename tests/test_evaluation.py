import tempfile
import unittest
from pathlib import Path

from proof_repair.evaluation import read_attempts, summarize, write_attempts
from proof_repair.models import Attempt, CheckResult


class EvaluationTests(unittest.TestCase):
    def test_distinguishes_initial_and_repaired_success(self):
        attempts = [
            Attempt("a", "formalize", "a", CheckResult(True)),
            Attempt("b", "formalize", "b", CheckResult(False)),
            Attempt("b", "repair", "b'", CheckResult(True), 1),
        ]
        result = summarize(attempts)
        self.assertEqual(result["examples"], 2)
        self.assertEqual(result["initial_successes"], 1)
        self.assertEqual(result["repaired_successes"], 1)
        self.assertEqual(result["eventual_success_rate"], 1.0)

    def test_round_order_and_artifact_round_trip(self):
        attempts = [
            Attempt("a", "repair", "fixed", CheckResult(True), 1),
            Attempt("a", "formalize", "broken", CheckResult(False), 0),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "attempts.jsonl"
            write_attempts(path, attempts)
            restored = read_attempts(path)
        self.assertEqual(summarize(restored)["initial_successes"], 0)
