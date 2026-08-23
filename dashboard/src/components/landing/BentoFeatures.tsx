"use client";

import { FadeIn } from "@/components/magic/Reveal";
import { cn } from "@/lib/utils";

function FeatureCard({
  icon,
  title,
  desc,
  span,
  children,
}: {
  icon: string;
  title: string;
  desc: string;
  span?: boolean;
  children?: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        "group rounded-2xl border border-white/[0.07] bg-white/[0.02] p-6 glow-card transition-all duration-200 hover:border-white/15 hover:bg-white/[0.035]",
        span && "md:col-span-2"
      )}
    >
      <div className="size-10 rounded-xl bg-white/5 border border-white/10 grid place-items-center text-lg mb-4">
        {icon}
      </div>
      <h3 className="text-[17px] font-semibold tracking-tight">{title}</h3>
      <p className="text-[13.5px] text-muted-foreground mt-1.5 leading-relaxed">{desc}</p>
      {children}
    </div>
  );
}

export function BentoFeatures() {
  return (
    <section id="features" className="py-24">
      <div className="max-w-6xl mx-auto px-6">
        <FadeIn>
          <div className="max-w-2xl mb-12">
            <div className="text-[12px] uppercase tracking-[0.12em] text-indigo-400 font-semibold mb-3">
              Why BharatWatch
            </div>
            <h2 className="text-[34px] md:text-[42px] font-semibold tracking-[-0.03em] leading-[1.1]">
              Scraping that never breaks.
              <br />
              <span className="text-muted-foreground">Intelligence that never sleeps.</span>
            </h2>
          </div>
        </FadeIn>

        <div className="grid md:grid-cols-3 gap-4">
          <FadeIn delay={0}>
            <FeatureCard
              span
              icon="🧬"
              title="Self-Healing Scrapers"
              desc="When a target portal redesigns its HTML, Bright Data's AI re-derives the extraction logic and ships a fixed scraper — no humans, no downtime, no broken pipelines."
            >
              <div className="mt-5 rounded-xl border border-white/[0.06] bg-[#0f1011] p-4 font-mono text-[12px] leading-relaxed overflow-hidden">
                <div className="text-muted-foreground"># layout change detected on ssc.nic.in</div>
                <div className="text-amber-300/90 mt-1">⚠ table#notices columns reordered</div>
                <div className="text-sky-300/90 mt-1">↻ regenerating extraction code…</div>
                <div className="text-emerald-300 mt-1">✓ healed in 42s — 0 records lost</div>
              </div>
            </FeatureCard>
          </FadeIn>

          <FadeIn delay={0.08}>
            <FeatureCard
              icon="🎯"
              title="100% Custom Collectors"
              desc="Every one of the 5 collectors is generated with Bright Data Scraper Studio from a natural-language prompt — not a single pre-built library scraper."
            />
          </FadeIn>

          <FadeIn delay={0.12}>
            <FeatureCard
              icon="📡"
              title="Live Diff Engine"
              desc="Every snapshot is hashed and diffed against the last. New records, updated fields, and deletions are caught field-by-field."
            />
          </FadeIn>

          <FadeIn delay={0.16}>
            <FeatureCard
              icon="🇮🇳"
              title="Built for Bharat"
              desc="Five verticals Indians actually care about — Sarkari Naukri alerts, govt tenders, mandi prices, JoSAA cutoffs, and startup schemes."
            />
          </FadeIn>

          <FadeIn delay={0.2}>
            <FeatureCard
              icon="📊"
              title="Mission-Control Dashboard"
              desc="A dark-native Next.js dashboard with live KPIs, 7-day activity charts, per-module visualisations, and a full self-heal audit trail."
            />
          </FadeIn>
        </div>
      </div>
    </section>
  );
}
