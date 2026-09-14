import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import QueryProvider from "@/providers/query-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FootPredict – Analyses & Pronostics",
  description: "Analyses de matchs, forme, blessures et pronostics football",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <QueryProvider>
          <div className="min-h-screen bg-zinc-950 text-zinc-100">
            <header className="border-b border-zinc-800 bg-zinc-900/80 backdrop-blur sticky top-0 z-50">
              <div className="container mx-auto px-4 h-14 flex items-center justify-between">
                <div className="font-bold text-xl tracking-tight">
                  Foot<span className="text-emerald-400">Predict</span>
                </div>
                <nav className="text-sm text-zinc-400">Analyses • Pronostics • Forme</nav>
              </div>
            </header>
            <main className="container mx-auto px-4 py-8">{children}</main>
          </div>
        </QueryProvider>
      </body>
    </html>
  );
}
