from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TeamBasic(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None


class FixtureBasic(BaseModel):
    id: int
    date: datetime
    status: str
    home_team: TeamBasic
    away_team: TeamBasic
    league_name: str
    league_country: str
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None


class FormInfo(BaseModel):
    score: float = Field(..., description="Score de forme entre 0 et 1")
    last_5: List[str] = Field(default_factory=list)


class InjuryInfo(BaseModel):
    player_name: str
    player_id: Optional[int] = None
    type: Optional[str] = None
    reason: Optional[str] = None
    importance: str = "medium"


class MatchAnalysis(BaseModel):
    fixture: FixtureBasic
    home_form: FormInfo
    away_form: FormInfo
    injuries: List[InjuryInfo] = []
    h2h_summary: Optional[Dict[str, Any]] = None
    notes: List[str] = []


class PredictionResponse(BaseModel):
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
    recommended: List[str] = Field(default_factory=list)
