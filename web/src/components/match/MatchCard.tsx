import Link from "next/link";
import { Fixture } from "@/lib/types";
import { format } from "date-fns";
import { fr } from "date-fns/locale";

export default function MatchCard({ match }: { match: Fixture }) {
  return (
    <Link href={`/match/${match.id}`}>
      <div className="h-full cursor-pointer rounded-xl border border-cyan-300 bg-gradient-to-br from-blue-600 via-sky-500 to-cyan-400 p-5 text-white shadow-lg transition-all hover:-translate-y-1 hover:shadow-xl">
        <div className="mb-3 flex justify-between text-xs font-medium text-blue-50">
          <span>{match.league_name}</span>
          <span>{format(new Date(match.date), "HH:mm", { locale: fr })}</span>
        </div>

        <div className="flex items-center justify-between gap-3">
          <div className="flex-1 text-right">
            <div className="truncate font-bold">
              {match.home_team.name}
            </div>
          </div>

          <div className="rounded-full bg-white/25 px-3 py-1 text-sm font-bold">
            VS
          </div>

          <div className="flex-1">
            <div className="truncate font-bold">
              {match.away_team.name}
            </div>
          </div>
        </div>

        <div className="mt-4 text-center">
          <span className="inline-block rounded-full bg-white px-3 py-1 text-xs font-semibold text-blue-700 shadow">
            Voir l’analyse →
          </span>
        </div>
      </div>
    </Link>
  );
}
