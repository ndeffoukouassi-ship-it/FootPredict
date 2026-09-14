from dataclasses import dataclass
from math import exp, factorial
from typing import Any, Dict, List, Optional


@dataclass
class MatchPrediction:
    fixture_id: int
    home_win: float
    draw: float
    away_win: float
    double_chance_1x: float
    double_chance_x2: float
    double_chance_12: float
    btts_yes: float
    btts_no: float
    over_15: float
    under_15: float
    over_25: float
    under_25: float
    over_35: float
    under_35: float
    first_half_home: float
    first_half_draw: float
    first_half_away: float
    expected_home_goals: float
    expected_away_goals: float
    likely_scores: List[Dict[str, Any]]
    confidence: float
    chance_factor: float
    analysis: Dict[str, Any]


class PredictionEngine:
    """Moteur V2 : forme pondérée, buts attendus et matrice de Poisson."""

    @staticmethod
    def _team_stats(fixtures: List[Dict], team_id: int) -> Dict[str, float]:
        rows = []
        weights = [1.00, 0.92, 0.84, 0.76, 0.68, 0.60, 0.55, 0.55, 0.55, 0.55]
        for i, fix in enumerate(fixtures[:10]):
            teams, goals = fix.get("teams", {}), fix.get("goals", {})
            home_id = teams.get("home", {}).get("id")
            away_id = teams.get("away", {}).get("id")
            hg, ag = goals.get("home"), goals.get("away")
            if hg is None or ag is None or team_id not in (home_id, away_id):
                continue
            gf, ga = (hg, ag) if team_id == home_id else (ag, hg)
            points = 3 if gf > ga else 1 if gf == ga else 0
            rows.append((weights[min(i, len(weights) - 1)], gf, ga, points))

        if not rows:
            return {"matches": 0, "gf": 1.2, "ga": 1.2, "form": 0.5}
        weight_sum = sum(r[0] for r in rows)
        return {
            "matches": len(rows),
            "gf": sum(w * gf for w, gf, _, _ in rows) / weight_sum,
            "ga": sum(w * ga for w, _, ga, _ in rows) / weight_sum,
            "form": sum(w * pts for w, _, _, pts in rows) / (weight_sum * 3),
        }

    @staticmethod
    def _poisson(k: int, rate: float) -> float:
        return exp(-rate) * (rate ** k) / factorial(k)

    @staticmethod
    def _clamp(value: float, low: float, high: float) -> float:
        return max(low, min(high, value))

    def predict(self, fixture_id: int, home_team_id: int, away_team_id: int,
                home_last_fixtures: List[Dict], away_last_fixtures: List[Dict],
                h2h_fixtures: Optional[List[Dict]] = None,
                injuries: Optional[List[Dict]] = None) -> MatchPrediction:
        home = self._team_stats(home_last_fixtures, home_team_id)
        away = self._team_stats(away_last_fixtures, away_team_id)
        lambda_home = self._clamp(((home["gf"] + away["ga"]) / 2) * 1.08, 0.25, 3.5)
        lambda_away = self._clamp((away["gf"] + home["ga"]) / 2, 0.25, 3.5)

        matrix = [(hg, ag, self._poisson(hg, lambda_home) * self._poisson(ag, lambda_away))
                  for hg in range(8) for ag in range(8)]
        mass = sum(p for _, _, p in matrix)
        matrix = [(hg, ag, p / mass) for hg, ag, p in matrix]
        home_win = sum(p for hg, ag, p in matrix if hg > ag)
        draw = sum(p for hg, ag, p in matrix if hg == ag)
        away_win = sum(p for hg, ag, p in matrix if hg < ag)
        btts_yes = sum(p for hg, ag, p in matrix if hg > 0 and ag > 0)

        def over(line: float) -> float:
            return sum(p for hg, ag, p in matrix if hg + ag > line)

        likely_scores = [{"score": f"{hg}-{ag}", "probability": round(p, 3)}
                         for hg, ag, p in sorted(matrix, key=lambda x: x[2], reverse=True)[:3]]
        first_half_home, first_half_away = home_win * 0.62, away_win * 0.62
        first_half_draw = 1 - first_half_home - first_half_away
        sample_reliability = min(home["matches"], away["matches"]) / 10
        balance = 1 - abs(home_win - away_win)
        chance_factor = self._clamp(balance * 55 + (1 - sample_reliability) * 45, 5, 95)
        confidence = self._clamp(88 - chance_factor * 0.43, 45, 85)

        if home["form"] > away["form"] + 0.15:
            notes = ["La forme récente favorise l'équipe à domicile"]
        elif away["form"] > home["form"] + 0.15:
            notes = ["La forme récente favorise l'équipe à l'extérieur"]
        else:
            notes = ["Les formes récentes sont proches : match potentiellement équilibré"]
        if min(home["matches"], away["matches"]) < 5:
            notes.append("Peu de matchs exploitables : prudence recommandée")

        analysis = {
            "home_form": round(home["form"], 3), "away_form": round(away["form"], 3),
            "home_goals_for": round(home["gf"], 2), "home_goals_against": round(home["ga"], 2),
            "away_goals_for": round(away["gf"], 2), "away_goals_against": round(away["ga"], 2),
            "sample_size": min(home["matches"], away["matches"]),
            "h2h_count": len(h2h_fixtures or []), "injuries_count": len(injuries or []),
            "notes": notes,
        }
        return MatchPrediction(
            fixture_id=fixture_id, home_win=round(home_win, 3), draw=round(draw, 3),
            away_win=round(away_win, 3), double_chance_1x=round(home_win + draw, 3),
            double_chance_x2=round(draw + away_win, 3), double_chance_12=round(home_win + away_win, 3),
            btts_yes=round(btts_yes, 3), btts_no=round(1 - btts_yes, 3),
            over_15=round(over(1.5), 3), under_15=round(1 - over(1.5), 3),
            over_25=round(over(2.5), 3), under_25=round(1 - over(2.5), 3),
            over_35=round(over(3.5), 3), under_35=round(1 - over(3.5), 3),
            first_half_home=round(first_half_home, 3), first_half_draw=round(first_half_draw, 3),
            first_half_away=round(first_half_away, 3), expected_home_goals=round(lambda_home, 2),
            expected_away_goals=round(lambda_away, 2), likely_scores=likely_scores,
            confidence=round(confidence, 1), chance_factor=round(chance_factor, 1), analysis=analysis)


prediction_engine = PredictionEngine()
