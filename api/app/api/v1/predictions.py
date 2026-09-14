from fastapi import APIRouter, HTTPException
from app.services.football_api import football_api
from app.services.prediction_engine import prediction_engine
from app.models.schemas import PredictionResponse

router = APIRouter()


@router.get("/{fixture_id}", response_model=PredictionResponse)
async def get_prediction(fixture_id: int):
    try:
        raw = await football_api.get_fixture_by_id(fixture_id)
        if not raw:
            raise HTTPException(status_code=404, detail="Match non trouvé")

        home_id = raw["teams"]["home"]["id"]
        away_id = raw["teams"]["away"]["id"]

        home_last = await football_api.get_last_fixtures(home_id, last=10)
        away_last = await football_api.get_last_fixtures(away_id, last=10)
        h2h = await football_api.get_head_to_head(home_id, away_id, last=8)
        injuries = await football_api.get_injuries(fixture_id)

        prediction = prediction_engine.predict(
            fixture_id=fixture_id,
            home_team_id=home_id,
            away_team_id=away_id,
            home_last_fixtures=home_last,
            away_last_fixtures=away_last,
            h2h_fixtures=h2h,
            injuries=injuries
        )

        recommended = []
        if prediction.btts_yes >= 0.58:
            recommended.append("BTTS Oui")
        if prediction.home_win >= 0.48:
            recommended.append("1 (Victoire domicile)")
        elif prediction.away_win >= 0.42:
            recommended.append("2 (Victoire extérieur)")
        elif prediction.draw >= 0.30:
            recommended.append("X (Nul)")
        
        if prediction.over_25 >= 0.55:
            recommended.append("Over 2.5")
        elif prediction.under_25 >= 0.60:
            recommended.append("Under 2.5")

        double_chances = {
            "1X (Domicile ou nul)": prediction.double_chance_1x,
            "X2 (Extérieur ou nul)": prediction.double_chance_x2,
            "12 (Une équipe gagne)": prediction.double_chance_12,
        }
        best_dc, best_dc_value = max(double_chances.items(), key=lambda item: item[1])
        if best_dc_value >= 0.70:
            recommended.append(best_dc)

        return PredictionResponse(
            fixture_id=prediction.fixture_id,
            home_win=prediction.home_win,
            draw=prediction.draw,
            away_win=prediction.away_win,
            double_chance_1x=prediction.double_chance_1x,
            double_chance_x2=prediction.double_chance_x2,
            double_chance_12=prediction.double_chance_12,
            btts_yes=prediction.btts_yes,
            btts_no=prediction.btts_no,
            over_15=prediction.over_15,
            under_15=prediction.under_15,
            over_25=prediction.over_25,
            under_25=prediction.under_25,
            over_35=prediction.over_35,
            under_35=prediction.under_35,
            first_half_home=prediction.first_half_home,
            first_half_draw=prediction.first_half_draw,
            first_half_away=prediction.first_half_away,
            expected_home_goals=prediction.expected_home_goals,
            expected_away_goals=prediction.expected_away_goals,
            likely_scores=prediction.likely_scores,
            confidence=prediction.confidence,
            chance_factor=prediction.chance_factor,
            analysis=prediction.analysis,
            recommended=recommended
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
