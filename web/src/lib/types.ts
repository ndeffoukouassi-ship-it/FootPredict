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
  btts_yes: number;
  btts_no: number;
  over_25: number;
  under_25: number;
  first_half_home: number;
  first_half_draw: number;
  first_half_away: number;
  confidence: number;
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
