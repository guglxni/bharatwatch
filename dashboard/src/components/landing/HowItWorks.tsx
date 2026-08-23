"use client";

import { FadeIn } from "@/components/magic/Reveal";

const STEPS = [
  {
    n: "01",
    title: "Describe what to scrape",
    desc: "One natural-language prompt to Bright Data Scraper Studio: point it at a public portal and name the fields you want. AI builds the collector autonomously.",
    code: "bdata scraper create <url> \\\n  \"Extract all rows from table#notices…\"",
  },
  {
    n: "02",
    title: "AI builds + discovers",
    desc: "Scraper Studio generates extraction code. SERP + Discover find data sources across the web. Web Unlocker fetches pages as clean markdown.",
    code: "bdata search \"ssc recruitment 2026\"\nbdata discover --intent \"govt jobs\"\nbdata scrape sarkariresult.com",
  },
  {
    n: "03",
    title: "Watch, diff, heal",
    desc: "The orchestrator runs collectors on schedule, hashes every snapshot, emits field-level diffs, and self-heals the moment a layout drifts — all closed-loop.",
    code: "snapshot ok · 50 records\nΔ created: SSC MTS 2026\n🩹 heal: selector drift → auto-approved → fixed",
  },
];

export function HowItWorks() {
  return (
    <section id="how" className="py-24 border-t border-white/5 bg-white/[0.01]">
      <div className="max-w-6xl mx-auto px-6">
        <FadeIn>
          <div className="max-w-2xl mb-14">
            <div className="text-[12px] uppercase tracking-[0.12em] text-indigo-400 font-semibold mb-3">
              How it works
            </div>
            <h2 className="text-[34px] md:text-[42px] font-semibold tracking-[-0.03em] leading-[1.1]">
              From prompt to pipeline in three steps.
            </h2>
          </div>
        </FadeIn>

        <div className="grid md:grid-cols-3 gap-4 relative">
          {/* connecting line */}
          <div className="hidden md:block absolute top-[22px] left-[16%] right-[16%] h-px bg-gradient-to-r from-transparent via-indigo-500/40 to-transparent" />
          {STEPS.map((s, i) => (
            <FadeIn key={s.n} delay={i * 0.1}>
              <div className="relative rounded-2xl border border-white/[0.07] bg-white/[0.02] p-6 h-full glow-card hover:border-white/15 transition-colors">
                <div className="flex items-center gap-3 mb-4">
                  <div className="size-11 rounded-xl bg-indigo-500/10 border border-indigo-500/25 grid place-items-center font-mono text-[13px] font-semibold text-indigo-300 relative z-10">
                    {s.n}
                  </div>
                  <h3 className="text-[16px] font-semibold tracking-tight">{s.title}</h3>
                </div>
                <p className="text-[13.5px] text-muted-foreground leading-relaxed">{s.desc}</p>
                <div className="mt-4 rounded-lg border border-white/[0.06] bg-[#0c0d0e] p-3 font-mono text-[11.5px] text-muted-foreground leading-relaxed whitespace-pre-wrap">
                  {s.code}
                </div>
              </div>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}
