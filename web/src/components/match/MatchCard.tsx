import Link from "next/link";
import { Fixture } from "@/lib/types";
import { format } from "date-fns";
import { fr } from "date-fns/locale";

export default function MatchCard({ match }: { match: Fixture }) {
  return (
    <Link href={`/match/${match.id}`}>
      <div className="bg-slate-700 border border-slate-500 hover:border-emerald-500/50 transition-colors cursor-pointer h-full rounded-xl p-5">
        <div className="text-xs text-slate-300 mb-3 flex justify-between">
          <span>{match.league_name}</span>
          <span>{format(new Date(match.date), "HH:mm", { locale: fr })}</span>
        </div>

        <div className="flex items-center justify-between gap-3">
          <div className="flex-1 text-right">
            <div className="font-medium truncate">{match.home_team.name}</div>
          </div>

          <div className="text-slate-300 font-bold text-sm px-2">VS</div>

          <div className="flex-1">
            <div className="font-medium truncate">{match.away_team.name}</div>
          </div>
        </div>

        <div className="mt-4 text-center">
          <span className="text-xs bg-slate-600 text-slate-200 px-2.5 py-1 rounded-full">
            Voir l’analyse →
          </span>
        </div>
      </div>
    </Link>
  );
}
