export interface Team {
  id: number;
  name: string;
  logo?: string;
}

export interface Fixture {
  id: number;
  date: string;
  status: string;
  home_team: Team;
  away_team: Team;
  league_name: string;
  league_country: string;
  home_goals?: number | null;
  away_goals?: number | null;
}

export interface Prediction {
  fixture_id: number;
  home_win: number;
  draw: number;
  away_win: number;
  double_chance_1x: number;
  double_chance_x2: number;
  double_chance_12: number;
  btts_yes: number;
  btts_no: number;
  over_15: number;
  under_15: number;
  over_25: number;
  under_25: number;
  over_35: number;
  under_35: number;
  first_half_home: number;
  first_half_draw: number;
  first_half_away: number;
  expected_home_goals: number;
  expected_away_goals: number;
  likely_scores: { score: string; probability: number }[];
  confidence: number;
  chance_factor: number;
  analysis: {
    home_form: number;
    away_form: number;
    notes: string[];
  };
  recommended: string[];
}

export interface MatchAnalysis {
  fixture: Fixture;
  home_form: { score: number };
  away_form: { score: number };
  injuries: {
    player_name: string;
    type?: string;
    reason?: string;
    importance: string;
  }[];
  notes: string[];
}
