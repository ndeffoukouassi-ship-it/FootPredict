"""Tests de non-regression pour le moteur FootPredict V11."""
import unittest

from app.services.prediction_engine import PredictionEngine


def match(team, opponent, gf, ga, at_home=True):
    return {
        "teams": {"home": {"id": team if at_home else opponent},
                  "away": {"id": opponent if at_home else team}},
        "goals": {"home": gf if at_home else ga,
                  "away": ga if at_home else gf},
    }


class PredictionEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = PredictionEngine()

    def test_uses_up_to_twenty_matches(self):
        fixtures = [match(1, 3, 2, 1) for _ in range(25)]
        stats = self.engine._team_stats(fixtures, 1)
        self.assertEqual(stats["matches"], 20)

    def test_market_probabilities_are_normalized(self):
        home = [match(1, 3, 2, 1) for _ in range(20)]
        away = [match(2, 4, 1, 1) for _ in range(20)]
        p = self.engine.predict(123, 1, 2, home, away)
        self.assertAlmostEqual(p.home_win + p.draw + p.away_win, 1, delta=0.002)
        self.assertAlmostEqual(p.first_half_home + p.first_half_draw + p.first_half_away, 1, delta=0.002)
        self.assertAlmostEqual(p.btts_yes + p.btts_no, 1, delta=0.002)
        self.assertEqual(len(p.likely_scores), 5)

    def test_empty_history_reports_low_sample(self):
        p = self.engine.predict(123, 1, 2, [], [])
        self.assertEqual(p.analysis["sample_size"], 0)
        self.assertTrue(any("Peu de matchs" in n for n in p.analysis["notes"]))


if __name__ == "__main__":
    unittest.main()
