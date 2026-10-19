"""Download historical league fixtures for an offline, leakage-safe backtest.

From api/: python -m app.services.collect_history --league 39 --season 2024 --league 140 --season 2024 --output history.json
API_FOOTBALL_KEY must be supplied via environment or api/.env. Never commit .env.
Each --league pairs with the matching --season by position.
"""
import argparse
import asyncio
import json
from pathlib import Path
import httpx
from app.core.config import settings

COMPLETED = {"FT"}  # Full-time only: avoid extra-time/penalty goal ambiguity.


async def fetch_history(leagues, seasons):
    fixtures = {}
    async with httpx.AsyncClient(timeout=60.0, headers={"x-apisports-key": settings.API_FOOTBALL_KEY}) as client:
        for league, season in zip(leagues, seasons):
            response = await client.get(
                f"{settings.API_FOOTBALL_BASE_URL}/fixtures",
                params={"league": league, "season": season, "status": "FT"},
            )
            response.raise_for_status()
            payload = response.json()
            if payload.get("errors"):
                raise RuntimeError(f"API-Football returned an error for league {league}, season {season}: {payload['errors']}")
            for fixture in payload.get("response", []):
                if (fixture.get("fixture", {}).get("status") or {}).get("short") != "FT":
                    continue
                fixture_id = fixture.get("fixture", {}).get("id")
                if fixture_id is not None:
                    fixtures[fixture_id] = fixture
            print(f"League {league}, season {season}: {len(payload.get('response', []))} fixtures returned")
    return sorted(fixtures.values(), key=lambda f: (f["fixture"].get("date", ""), f["fixture"].get("id", 0)))


def main():
    parser = argparse.ArgumentParser(description="Collect completed league fixtures from API-FOOTBALL")
    parser.add_argument("--league", action="append", type=int, required=True)
    parser.add_argument("--season", action="append", type=int, required=True)
    parser.add_argument("--output", type=Path, default=Path("history.json"))
    args = parser.parse_args()
    if len(args.league) != len(args.season):
        parser.error("Each --league must have one corresponding --season")
    if len(set(zip(args.league, args.season))) != len(args.league):
        parser.error("Duplicate league-season pairs are not allowed")
    records = asyncio.run(fetch_history(args.league, args.season))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(records)} unique completed fixtures to {args.output}")
    if len(records) < 1000:
        print("Note: 1000 evaluable predictions need more than 1000 raw fixtures because of warm-up history.")


if __name__ == "__main__":
    main()
