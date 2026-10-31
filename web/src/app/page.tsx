"use client";

import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getTodayMatches } from "@/lib/api";
import MatchCard from "@/components/match/MatchCard";

function normalizeTeamName(name: string) {
  return name.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("fr").replace(/\s+/g, " ").trim();
}

export default function HomePage() {
  const [selectedHour, setSelectedHour] = useState("");
  const [activeHour, setActiveHour] = useState("");
  const [teamInput, setTeamInput] = useState("");
  const [activeTeam, setActiveTeam] = useState("");
  const { data: matches, isLoading, error } = useQuery({
    queryKey: ["matches", "today"], queryFn: getTodayMatches,
  });

  const filteredMatches = useMemo(() => {
    if (!matches) return matches;
    const query = normalizeTeamName(activeTeam);
    return matches.filter((match) => {
      const hourMatches = !activeHour ||
        String(new Date(match.date).getHours()).padStart(2, "0") === activeHour;
      const teamMatches = !query ||
        [match.home_team.name, match.away_team.name]
          .some((teamName) => normalizeTeamName(teamName).includes(query));
      return hourMatches && teamMatches;
    });
  }, [matches, activeHour, activeTeam]);

  const matchesByLeague = filteredMatches?.reduce((acc, match) => {
    const key = `${match.league_name} — ${match.league_country}`;
    if (!acc[key]) acc[key] = [];
    acc[key].push(match);
    return acc;
  }, {} as Record<string, NonNullable<typeof filteredMatches>>);

  const resetHour = () => { setSelectedHour(""); setActiveHour(""); };
  const resetTeam = () => { setTeamInput(""); setActiveTeam(""); };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Matchs du jour</h1>
        <p className="text-slate-200 mt-1">Analyses, forme, blessures et pronostics</p>
      </div>

      <section className="rounded-xl border border-slate-500 bg-slate-700 p-4">
        <h2 className="font-semibold mb-3">Rechercher les matchs par heure</h2>
        <div className="flex flex-col sm:flex-row gap-3">
          <select value={selectedHour} onChange={(e) => setSelectedHour(e.target.value)}
            className="rounded-lg border border-slate-400 bg-slate-800 px-4 py-2 text-white">
            <option value="">Choisir une heure</option>
            {Array.from({ length: 24 }, (_, hour) => {
              const value = String(hour).padStart(2, "0");
              return <option key={value} value={value}>{value} h 00 à {value} h 59</option>;
            })}
          </select>
          <button type="button" onClick={() => setActiveHour(selectedHour)} disabled={!selectedHour}
            className="rounded-lg bg-emerald-500 px-5 py-2 font-semibold text-slate-950 disabled:opacity-50">Rechercher</button>
          {activeHour && <button type="button" onClick={resetHour}
            className="rounded-lg border border-slate-400 px-5 py-2">Afficher tous les matchs</button>}
        </div>
        {activeHour && <p className="mt-3 text-sm text-emerald-300">
          {filteredMatches?.length ?? 0} match(s) trouvé(s) entre {activeHour} h 00 et {activeHour} h 59
        </p>}
      </section>

      <section aria-labelledby="team-search-title" className="rounded-xl border border-slate-500 bg-slate-700 p-4">
        <h2 id="team-search-title" className="mb-1 font-semibold">🔎 Rechercher par équipe</h2>
        <p className="mb-3 text-sm text-slate-200">Trouve les matchs du jour d&apos;une équipe, à domicile ou à l&apos;extérieur.</p>
        <form className="flex flex-col gap-3 sm:flex-row"
          onSubmit={(event) => { event.preventDefault(); setActiveTeam(teamInput.trim()); }}>
          <label htmlFor="team-search" className="sr-only">Nom de l&apos;équipe</label>
          <input id="team-search" type="search" autoComplete="off" enterKeyHint="search"
            placeholder="Ex. : Real Madrid, ASEC, Arsenal…" value={teamInput}
            onChange={(event) => setTeamInput(event.target.value)}
            className="min-w-0 flex-1 rounded-lg border border-slate-400 bg-slate-800 px-4 py-3 text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-400" />
          <button type="submit" disabled={!teamInput.trim()}
            className="rounded-lg bg-emerald-500 px-5 py-3 font-semibold text-slate-950 disabled:cursor-not-allowed disabled:opacity-50">
            Rechercher
          </button>
          {activeTeam && <button type="button" onClick={resetTeam}
            className="rounded-lg border border-slate-400 px-5 py-3 font-semibold">Effacer</button>}
        </form>
        {activeTeam && <p role="status" className="mt-3 text-sm text-emerald-300">
          {filteredMatches?.length ?? 0} match(s) trouvé(s) pour « {activeTeam} » aujourd&apos;hui
          {activeHour ? ` (filtre horaire : ${activeHour} h)` : ""}.
        </p>}
      </section>

      {isLoading && <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[...Array(6)].map((_, i) => <div key={i} className="h-44 rounded-xl bg-slate-700 animate-pulse" />)}
      </div>}
      {error && <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-red-300">
        Impossible de charger les matchs. Vérifie que l’API est démarrée et que ta clé API-Football est valide.
      </div>}

      {matchesByLeague && Object.keys(matchesByLeague).length > 0 ? <div className="space-y-10">
        {Object.entries(matchesByLeague).map(([leagueName, leagueMatches]) => <section key={leagueName}>
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-lg font-semibold">{leagueName}</h2>
            <span className="text-xs bg-slate-600 text-slate-200 px-2.5 py-1 rounded-full">
              {leagueMatches.length} match{leagueMatches.length > 1 ? "s" : ""}
            </span>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {leagueMatches.map((match) => <MatchCard key={match.id} match={match} />)}
          </div>
        </section>)}
      </div> : !isLoading && <div className="text-center py-20 text-slate-200">
        {activeTeam
          ? `Aucun match trouvé aujourd’hui pour « ${activeTeam} »${activeHour ? ` entre ${activeHour} h 00 et ${activeHour} h 59` : ""}.`
          : activeHour
            ? `Aucun match programmé entre ${activeHour} h 00 et ${activeHour} h 59`
            : "Aucun match prévu aujourd’hui"}
      </div>}
    </div>
  );
}
