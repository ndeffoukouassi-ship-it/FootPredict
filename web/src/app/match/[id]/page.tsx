"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { getMatchAnalysis, getPrediction } from "@/lib/api";
import PredictionCard from "@/components/match/PredictionCard";

export default function MatchPage() {
  const params = useParams();
  const id = Number(params.id);

  const { data: analysis, isLoading: loadingAnalysis } = useQuery({
    queryKey: ["analysis", id],
    queryFn: () => getMatchAnalysis(id),
    enabled: !!id,
  });

  const { data: prediction, isLoading: loadingPrediction } = useQuery({
    queryKey: ["prediction", id],
    queryFn: () => getPrediction(id),
    enabled: !!id,
  });

  if (loadingAnalysis || loadingPrediction) {
    return (
      <div className="space-y-6">
        <div className="h-12 w-64 bg-slate-700 rounded animate-pulse" />
        <div className="h-64 w-full rounded-xl bg-slate-700 animate-pulse" />
      </div>
    );
  }

  if (!analysis || !prediction) {
    return <div className="text-red-400">Match introuvable ou erreur API</div>;
  }

  const { fixture } = analysis;

  return (
    <div className="space-y-8 max-w-4xl">
      {/* Header match */}
      <div className="bg-slate-700 border border-slate-500 rounded-2xl p-6">
        <div className="text-sm text-slate-300 mb-2">
          {fixture.league_name} • {fixture.league_country}
        </div>
        <div className="flex items-center justify-center gap-8 text-2xl font-bold">
          <span className="text-right flex-1">{fixture.home_team.name}</span>
          <span className="text-slate-300 text-lg">vs</span>
          <span className="flex-1">{fixture.away_team.name}</span>
        </div>
      </div>

      {/* Forme */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-700 border border-slate-500 rounded-xl p-4">
          <div className="text-sm text-slate-200 mb-1">Forme domicile</div>
          <div className="text-2xl font-bold text-emerald-400">
            {(analysis.home_form.score * 100).toFixed(0)}%
          </div>
        </div>
        <div className="bg-slate-700 border border-slate-500 rounded-xl p-4">
          <div className="text-sm text-slate-200 mb-1">Forme extérieur</div>
          <div className="text-2xl font-bold text-emerald-400">
            {(analysis.away_form.score * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Pronostics */}
      <PredictionCard prediction={prediction} />

      {/* Blessures */}
      {analysis.injuries.length > 0 && (
        <div className="bg-slate-700 border border-slate-500 rounded-xl p-5">
          <h3 className="font-semibold mb-3">Blessures & absences</h3>
          <div className="space-y-2">
            {analysis.injuries.map((inj, i) => (
              <div key={i} className="flex items-center justify-between text-sm">
                <span>{inj.player_name}</span>
                <span className="text-xs bg-slate-600 text-slate-200 px-2 py-0.5 rounded">
                  {inj.importance}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
