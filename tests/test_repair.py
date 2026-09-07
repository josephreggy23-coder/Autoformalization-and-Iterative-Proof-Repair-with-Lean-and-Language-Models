import unittest

from proof_repair.models import BenchmarkItem, CheckResult
from proof_repair.repair import RepairEngine


class ScriptedGenerator:
    def __init__(self, replies):
        self.replies = iter(replies)

    def complete(self, prompt):
        return next(self.replies)


class SourceChecker:
    def check(self, source):
        if "valid" in source:
            return CheckResult(True)
        return CheckResult(False, "unknown tactic")


class RepairTests(unittest.TestCase):
    item = BenchmarkItem("example", "dev", "A fact.", "theorem target : True := by trivial")

    def test_retries_until_checker_accepts(self):
        engine = RepairEngine(ScriptedGenerator(["bad", "```lean\nvalid\n```"]), SourceChecker(), 2)
        attempts = engine.run(self.item)
        self.assertEqual([a.phase for a in attempts], ["formalize", "repair"])
        self.assertTrue(attempts[-1].check.accepted)
        self.assertEqual(attempts[-1].source, "valid")

    def test_stops_after_budget(self):
        engine = RepairEngine(ScriptedGenerator(["bad", "still bad"]), SourceChecker(), 1)
        self.assertEqual(len(engine.run(self.item)), 2)
