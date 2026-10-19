"""Tests for historical evaluation without future-data leakage."""
import unittest
from app.services.backtest import evaluate


def fixture(i, kickoff, home, away, hg, ag):
    return {
        "fixture": {"id": i, "date": kickoff, "status": {"short": "FT"}},
        "teams": {"home": {"id": home}, "away": {"id": away}},
        "goals": {"home": hg, "away": ag},
        "score": {"fulltime": {"home": hg, "away": ag}},
    }


class BacktestTests(unittest.TestCase):
    def test_backtest_uses_prior_matches_only(self):
        fixtures = [
            fixture(i, f"2026-01-{i:02d}T15:00:00+00:00", 1, 2, 1, 0)
            for i in range(1, 9)
        ]
        result = evaluate(fixtures, limit=1000, min_history=5)
        self.assertEqual(result["evaluated"], 3)
        self.assertTrue(0 <= result["accuracy_1x2"] <= 1)
        self.assertGreaterEqual(result["mean_brier_1x2"], 0)

    def test_no_fixtures_returns_no_accuracy(self):
        result = evaluate([])
        self.assertEqual(result["evaluated"], 0)
        self.assertIsNone(result["accuracy_1x2"])

    def test_same_kickoff_not_used_as_history(self):
        rows = [fixture(i, "2026-01-01T15:00:00+00:00", 1, 2, 1, 0) for i in range(1, 10)]
        result = evaluate(rows, min_history=5)
        self.assertEqual(result["evaluated"], 0)


if __name__ == "__main__":
    unittest.main()
