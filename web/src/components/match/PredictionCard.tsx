import { Prediction } from "@/lib/types";

function ProbBar({
  label,
  value,
  color = "bg-emerald-500",
}: {
  label: string;
  value: number;
  color?: string;
}) {
  return (
    <div className="space-y-1.5">
      <div className="flex justify-between text-sm">
        <span className="text-slate-200">{label}</span>
        <span className="font-medium tabular-nums">{(value * 100).toFixed(1)}%</span>
      </div>
      <div className="h-2 bg-slate-600 rounded-full overflow-hidden">
        <div
          className={`h-full ${color} rounded-full transition-all duration-500`}
          style={{ width: `${Math.min(value * 100, 100)}%` }}
        />
      </div>
    </div>
  );
}

export default function PredictionCard({ prediction }: { prediction: Prediction }) {
  return (
    <div className="bg-slate-700 border border-slate-500 rounded-xl">
      <div className="p-5 pb-4 flex items-center justify-between border-b border-slate-500">
        <h3 className="text-lg font-semibold">Pronostics</h3>
        <span className="text-sm bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 rounded-full">
          Confiance {prediction.confidence}%
        </span>
      </div>

      <div className="p-5 space-y-8">
        {/* 1X2 */}
        <section className="space-y-3">
          <h4 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
            Résultat final (1X2)
          </h4>
          <ProbBar label="1 — Domicile" value={prediction.home_win} />
          <ProbBar label="N — Nul" value={prediction.draw} color="bg-amber-500" />
          <ProbBar label="2 — Extérieur" value={prediction.away_win} color="bg-sky-500" />
        </section>

        <section className="space-y-3">
          <h4 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">Double chance</h4>
          <div className="grid grid-cols-3 gap-3">
            {[["1X", prediction.double_chance_1x], ["X2", prediction.double_chance_x2], ["12", prediction.double_chance_12]].map(([label, value]) => (
              <div key={String(label)} className="bg-slate-600/60 rounded-lg p-3 text-center">
                <div className="text-xs text-slate-300">{label}</div>
                <div className="text-lg font-bold text-emerald-400">{(Number(value) * 100).toFixed(0)}%</div>
              </div>
            ))}
          </div>
        </section>

        {/* BTTS + Over/Under */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
          <section className="space-y-3">
            <h4 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
              Les deux équipes marquent
            </h4>
            <ProbBar label="Oui" value={prediction.btts_yes} />
            <ProbBar label="Non" value={prediction.btts_no} color="bg-zinc-600" />
          </section>

          <section className="space-y-3">
            <h4 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
              Nombre de buts
            </h4>
            <ProbBar label="Over 2.5" value={prediction.over_25} />
            <ProbBar label="Under 2.5" value={prediction.under_25} color="bg-zinc-600" />
            <ProbBar label="Over 1.5" value={prediction.over_15} color="bg-sky-500" />
            <ProbBar label="Over 3.5" value={prediction.over_35} color="bg-violet-500" />
          </section>
        </div>

        <section>
          <h4 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3">Scores les plus probables</h4>
          <div className="grid grid-cols-3 gap-3">
            {prediction.likely_scores.map((item) => (
              <div key={item.score} className="bg-slate-600/60 rounded-lg p-3 text-center">
                <div className="text-xl font-bold">{item.score}</div>
                <div className="text-xs text-slate-200">{(item.probability * 100).toFixed(1)}%</div>
              </div>
            ))}
          </div>
          <div className="mt-3 text-sm text-slate-200 flex justify-between gap-4">
            <span>Buts attendus : {prediction.expected_home_goals} - {prediction.expected_away_goals}</span>
            <span>Facteur chance : {prediction.chance_factor}%</span>
          </div>
        </section>

        {/* 1ère mi-temps */}
        <section className="space-y-3">
          <h4 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
            Première mi-temps
          </h4>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-slate-600/60 rounded-lg p-3 text-center">
              <div className="text-xs text-slate-300 mb-1">1</div>
              <div className="text-lg font-bold text-emerald-400">
                {(prediction.first_half_home * 100).toFixed(0)}%
              </div>
            </div>
            <div className="bg-slate-600/60 rounded-lg p-3 text-center">
              <div className="text-xs text-slate-300 mb-1">N</div>
              <div className="text-lg font-bold text-amber-400">
                {(prediction.first_half_draw * 100).toFixed(0)}%
              </div>
            </div>
            <div className="bg-slate-600/60 rounded-lg p-3 text-center">
              <div className="text-xs text-slate-300 mb-1">2</div>
              <div className="text-lg font-bold text-sky-400">
                {(prediction.first_half_away * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        </section>

        {/* Recommandations */}
        {prediction.recommended.length > 0 && (
          <section>
            <h4 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3">
              Recommandations
            </h4>
            <div className="flex flex-wrap gap-2">
              {prediction.recommended.map((rec) => (
                <span
                  key={rec}
                  className="bg-emerald-600/90 text-white text-sm px-3 py-1 rounded-full"
                >
                  {rec}
                </span>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
