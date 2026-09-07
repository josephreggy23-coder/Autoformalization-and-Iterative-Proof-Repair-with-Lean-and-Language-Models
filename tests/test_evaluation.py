import unittest

from proof_repair.evaluation import summarize
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
