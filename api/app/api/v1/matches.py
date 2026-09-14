from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.football_api import football_api
from app.models.schemas import FixtureBasic, MatchAnalysis, FormInfo, InjuryInfo, TeamBasic
from datetime import datetime
from app.services.prediction_engine import prediction_engine

router = APIRouter()


def _parse_fixture(raw: dict) -> FixtureBasic:
    fixture = raw["fixture"]
    teams = raw["teams"]
    league = raw["league"]
    goals = raw["goals"]

    return FixtureBasic(
        id=fixture["id"],
        date=datetime.fromisoformat(fixture["date"].replace("Z", "+00:00")),
        status=fixture["status"]["short"],
        home_team=TeamBasic(
            id=teams["home"]["id"],
            name=teams["home"]["name"],
            logo=teams["home"].get("logo")
        ),
        away_team=TeamBasic(
            id=teams["away"]["id"],
            name=teams["away"]["name"],
            logo=teams["away"].get("logo")
        ),
        league_name=league["name"],
        league_country=league["country"],
        home_goals=goals["home"],
        away_goals=goals["away"]
    )


@router.get("/today", response_model=List[FixtureBasic])
async def get_today_matches(
    league: Optional[int] = Query(None, description="ID de ligue (ex: 61 = Ligue 1)")
):
    try:
        raw_fixtures = await football_api.get_fixtures_today()
        
        fixtures = []
        for raw in raw_fixtures:
            if league and raw["league"]["id"] != league:
                continue
            fixtures.append(_parse_fixture(raw))
        
        return fixtures
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{fixture_id}", response_model=FixtureBasic)
async def get_fixture(fixture_id: int):
    try:
        raw = await football_api.get_fixture_by_id(fixture_id)
        if not raw:
            raise HTTPException(status_code=404, detail="Match non trouvé")
        return _parse_fixture(raw)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{fixture_id}/analysis", response_model=MatchAnalysis)
async def get_match_analysis(fixture_id: int):
    try:
        raw = await football_api.get_fixture_by_id(fixture_id)
        if not raw:
            raise HTTPException(status_code=404, detail="Match non trouvé")

        fixture = _parse_fixture(raw)
        home_id = fixture.home_team.id
        away_id = fixture.away_team.id

        home_last = await football_api.get_last_fixtures(home_id, last=8)
        away_last = await football_api.get_last_fixtures(away_id, last=8)

        raw_injuries = await football_api.get_injuries(fixture_id)
        injuries = []
        for inj in raw_injuries:
            player = inj.get("player", {})
            injuries.append(InjuryInfo(
                player_name=player.get("name", "Inconnu"),
                player_id=player.get("id"),
                type=inj.get("type"),
                reason=inj.get("reason"),
                importance="high" if "important" in str(inj.get("reason", "")).lower() else "medium"
            ))

        home_form_score = prediction_engine._team_stats(home_last, home_id)["form"]
        away_form_score = prediction_engine._team_stats(away_last, away_id)["form"]

        return MatchAnalysis(
            fixture=fixture,
            home_form=FormInfo(score=round(home_form_score, 3)),
            away_form=FormInfo(score=round(away_form_score, 3)),
            injuries=injuries,
            notes=[]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
