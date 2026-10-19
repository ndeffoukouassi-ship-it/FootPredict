"""Historical walk-forward evaluation using completed fixtures (JSON list).

Run from api/: python -m app.services.backtest --input fixtures.json --limit 1000
Each fixture is an API-Football fixture response object with fixture.date,
fixture.id, teams.home.id, teams.away.id, goals.home and goals.away.
Only earlier, completed fixtures are used for each prediction. This does not
reconstruct historical injuries, odds or known-at-kickoff lineups.
"""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from app.services.prediction_engine import PredictionEngine


def evaluate(fixtures, limit=1000, min_history=5):
    engine = PredictionEngine()
    history = defaultdict(list)
    scored = []
    skipped = defaultdict(int)
    ordered = sorted(fixtures, key=lambda f: (f.get("fixture", {}).get("date", ""), f.get("fixture", {}).get("id", 0)))
    for row in ordered:
        fixture = row.get("fixture") or {}
        teams = row.get("teams") or {}
        goals = row.get("goals") or {}
        home = (teams.get("home") or {}).get("id")
        away = (teams.get("away") or {}).get("id")
        hg, ag = goals.get("home"), goals.get("away")
        status = (fixture.get("status") or {}).get("short")
        if not (home and away and isinstance(hg, int) and isinstance(ag, int) and status in ("FT", "AET", "PEN")):
            skipped["invalid_or_incomplete"] += 1
            continue
        home_hist, away_hist = history[home][-20:][::-1], history[away][-20:][::-1]
        if len(home_hist) >= min_history and len(away_hist) >= min_history and len(scored) < limit:
            pred = engine.predict(fixture.get("id", 0), home, away, home_hist, away_hist)
            # Winner classification uses regulation goals, when available.
            score = (row.get("score") or {}).get("fulltime") or {}
            fh, fa = score.get("home"), score.get("away")
            if not isinstance(fh, int) or not isinstance(fa, int):
                if status == "FT":
                    fh, fa = hg, ag
                else:
                    skipped["no_regulation_score"] += 1
                    fh = fa = None
            if fh is not None:
                outcome = 0 if fh > fa else 1 if fh == fa else 2
                probs = [pred.home_win, pred.draw, pred.away_win]
                scored.append({"fixture_id": fixture.get("id"), "actual": outcome,
                               "predicted": max(range(3), key=lambda i: probs[i]),
                               "probabilities": probs,
                               "brier": sum((p - (1 if i == outcome else 0)) ** 2 for i, p in enumerate(probs)),
                               "log_loss": -math.log(max(probs[outcome], 1e-12))})
        else:
            skipped["insufficient_history_or_limit"] += 1
        # Historical matches sharing a kickoff can leak if appended immediately;
        # group by timestamp in the next revision for strictly simultaneous games.
        history[home].append(row)
        history[away].append(row)
    n = len(scored)
    return {
        "evaluated": n, "target": limit, "available_fixtures": len(fixtures),
        "accuracy_1x2": sum(r["predicted"] == r["actual"] for r in scored) / n if n else None,
        "mean_brier_1x2": sum(r["brier"] for r in scored) / n if n else None,
        "mean_log_loss_1x2": sum(r["log_loss"] for r in scored) / n if n else None,
        "skipped": dict(skipped),
        "warning": "Historical lineups/injuries excluded; no profit or success guarantee.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    fixtures = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(fixtures, list):
        parser.error("Input must be a JSON list of fixture records")
    report = evaluate(fixtures, limit=args.limit)
    serialized = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
