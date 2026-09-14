"use client";

import { useQuery } from "@tanstack/react-query";
import { getTodayMatches } from "@/lib/api";
import MatchCard from "@/components/match/MatchCard";

export default function HomePage() {
  const { data: matches, isLoading, error } = useQuery({
    queryKey: ["matches", "today"],
    queryFn: getTodayMatches,
  });

  const matchesByLeague = matches?.reduce((acc, match) => {
    const key = match.league_name;
    if (!acc[key]) acc[key] = [];
    acc[key].push(match);
    return acc;
  }, {} as Record<string, NonNullable<typeof matches>>);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Matchs du jour</h1>
        <p className="text-zinc-400 mt-1">
          Analyses, forme, blessures et pronostics
        </p>
      </div>

      {isLoading && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-44 rounded-xl bg-zinc-900 animate-pulse" />
          ))}
        </div>
      )}

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-red-400">
          Impossible de charger les matchs. Vérifie que l’API est bien démarrée et que ta clé API-Football est valide.
        </div>
      )}

      {matchesByLeague && Object.keys(matchesByLeague).length > 0 ? (
        <div className="space-y-10">
          {Object.entries(matchesByLeague).map(([leagueName, leagueMatches]) => (
            <section key={leagueName}>
              <div className="flex items-center gap-3 mb-4">
                <h2 className="text-lg font-semibold">{leagueName}</h2>
                <span className="text-xs bg-zinc-800 text-zinc-400 px-2.5 py-1 rounded-full">
                  {leagueMatches.length} match{leagueMatches.length > 1 ? "s" : ""}
                </span>
              </div>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {leagueMatches.map((match) => (
                  <MatchCard key={match.id} match={match} />
                ))}
              </div>
            </section>
          ))}
        </div>
      ) : (
        !isLoading && (
          <div className="text-center py-20 text-zinc-500">
            Aucun match prévu aujourd’hui (ou clé API manquante / quota atteint)
          </div>
        )
      )}
    </div>
  );
}
