"use client";

import Link from "next/link";
import { FadeIn } from "@/components/magic/Reveal";
import { NumberTicker } from "@/components/magic/NumberTicker";
import type { Overview } from "@/lib/api";
import { cn } from "@/lib/utils";

const COPY: Record<string, { tagline: string; examples: string }> = {
  nauktrialert: {
    tagline: "The moment a new govt job drops on SarkariResult, it's on your radar — with vacancies, deadlines and exam dates.",
    examples: "SBI Clerk Backlog 2026 · JSSC 10+2 Level · RVUNL Various Post",
  },
  tendersentry: {
    tagline: "Every government tender tracked with value, department and closing date. Miss nothing worth bidding on.",
    examples: "Computer Hardware · ₹25L · Ministry of Electronics & IT",
  },
  mandiwatch: {
    tagline: "Min, modal and max prices from mandis across India — refreshed daily via BD Discover + Web Unlocker.",
    examples: "Tomato @ Yeshwanthpur · ₹1,500/q modal · ▲4.2% this week",
  },
  collegecutoff: {
    tagline: "JoSAA opening and closing ranks, round by round. Watch the cutoff move before you lock your choices.",
    examples: "IIT Bombay CSE · closing rank 60 · Round 1 closed",
  },
  startuppulse: {
    tagline: "Funding schemes, grants and awards from DPIIT, MSME and MeitY — with deadlines before they slip past.",
    examples: "Seed Fund · up to ₹50L · deadline 31 Dec",
  },
};

export function ModuleShowcase({ overview }: { overview: Overview | null }) {
  const mods = overview?.modules ?? [];
  return (
    <section id="modules" className="py-24">
      <div className="max-w-6xl mx-auto px-6">
        <FadeIn>
          <div className="max-w-2xl mb-12">
            <div className="text-[12px] uppercase tracking-[0.12em] text-indigo-400 font-semibold mb-3">
              Five live verticals
            </div>
            <h2 className="text-[34px] md:text-[42px] font-semibold tracking-[-0.03em] leading-[1.1]">
              One watcher. Five fronts.
            </h2>
            <p className="text-[15px] text-muted-foreground mt-3">
              Each vertical runs its own Bright Data custom collector with its own schema, diff history and
              dedicated dashboard view.
            </p>
          </div>
        </FadeIn>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {(mods.length ? mods : Array.from({ length: 5 })).map((m: any, i: number) => {
            const id = m?.id ?? Object.keys(COPY)[i];
            const copy = COPY[id] ?? { tagline: "", examples: "" };
            return (
              <FadeIn key={id} delay={i * 0.06}>
                <Link href={`/dashboard/${id}`}>
                  <div className="group rounded-2xl border border-white/[0.07] bg-white/[0.02] p-6 h-full glow-card hover:border-white/15 hover:-translate-y-0.5 transition-all duration-200">
                    <div className="flex items-center justify-between mb-4">
                      <div
                        className={cn(
                          "size-11 rounded-xl grid place-items-center text-xl bg-gradient-to-br text-white shadow-lg",
                          m?.accent ?? "from-indigo-500 to-violet-600"
                        )}
                      >
                        {m?.icon ?? ["🔔", "📄", "🌾", "🎓", "🚀"][i]}
                      </div>
                      {m && (
                        <div className="flex items-center gap-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1">
                          <span className="size-1.5 rounded-full bg-emerald-400 live-dot relative" />
                          <span className="text-[11px] font-medium text-emerald-300">Live</span>
                        </div>
                      )}
                    </div>
                    <h3 className="text-[17px] font-semibold tracking-tight">
                      {m?.label ?? ["NaukriAlert", "TenderSentry", "MandiWatch", "CollegeCutoff", "StartupPulse"][i]}
                    </h3>
                    <p className="text-[13px] text-muted-foreground mt-2 leading-relaxed">{copy.tagline}</p>
                    <div className="mt-4 rounded-lg border border-white/[0.06] bg-[#0c0d0e] px-3 py-2 font-mono text-[11px] text-muted-foreground truncate">
                      {copy.examples}
                    </div>
                    {m && (
                      <div className="mt-4 flex items-center gap-4 text-[12px] text-muted-foreground">
                        <span>
                          <NumberTicker value={m.item_count} className="text-foreground font-semibold" /> records
                        </span>
                        <span>
                          <NumberTicker value={m.changes_7d} className="text-amber-300 font-semibold" /> changes · 7d
                        </span>
                        <span className="ml-auto text-indigo-300 opacity-0 group-hover:opacity-100 transition-opacity">
                          Open →
                        </span>
                      </div>
                    )}
                  </div>
                </Link>
              </FadeIn>
            );
          })}
        </div>
      </div>
    </section>
  );
}
