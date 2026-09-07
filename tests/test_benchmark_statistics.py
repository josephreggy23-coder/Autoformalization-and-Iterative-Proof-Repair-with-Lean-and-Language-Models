import unittest

from proof_repair.benchmark import benchmark_statistics, load_benchmark


class BenchmarkStatisticsTests(unittest.TestCase):
    def test_reports_split_and_tag_counts(self):
        result = benchmark_statistics(load_benchmark("data/benchmark.jsonl"))
        self.assertEqual(result["examples"], 4)
        self.assertEqual(result["splits"], {"dev": 2, "test": 2})
        self.assertEqual(result["tags"]["algebra"], 2)
