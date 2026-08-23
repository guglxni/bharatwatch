"use client";

import Link from "next/link";
import { FadeIn } from "@/components/magic/Reveal";
import { Badge } from "@/components/ui/badge";

interface Heal {
  id: number;
  module_label: string;
  icon: string;
  description: string;
  success: string;
  created_at: string;
}

export function SelfHealSection({ heals }: { heals: Heal[] }) {
  const list = heals.slice(0, 4);
  return (
    <section id="healing" className="py-24 border-t border-white/5 bg-white/[0.01]">
      <div className="max-w-6xl mx-auto px-6 grid lg:grid-cols-2 gap-12 items-center">
        <FadeIn>
          <div>
            <div className="text-[12px] uppercase tracking-[0.12em] text-emerald-400 font-semibold mb-3">
              Spider-Sense
            </div>
            <h2 className="text-[34px] md:text-[42px] font-semibold tracking-[-0.03em] leading-[1.1]">
              Sites change.
              <br />
              <span className="text-gradient">Scrapers adapt.</span>
            </h2>
            <p className="text-[15px] text-muted-foreground mt-4 leading-relaxed max-w-md">
              Government portals redesign without warning. Traditional scrapers die silently. BharatWatch&apos;s
              healing loop detects selector drift, regenerates extraction code via{" "}
              <span className="text-foreground/90">bdata scraper heal</span>, and resumes — usually in under a
              minute.
            </p>
            <div className="mt-6 flex items-center gap-3">
              <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/[0.07] px-4 py-3">
                <div className="text-[22px] font-semibold text-emerald-300 tabular">5/5</div>
                <div className="text-[11px] text-muted-foreground">heals successful</div>
              </div>
              <div className="rounded-xl border border-white/[0.08] bg-white/[0.02] px-4 py-3">
                <div className="text-[22px] font-semibold tabular">0</div>
                <div className="text-[11px] text-muted-foreground">manual fixes needed</div>
              </div>
            </div>
            <Link
              href="/heal-log"
              className="inline-flex items-center gap-2 mt-6 text-[14px] font-medium text-indigo-300 hover:text-indigo-200 transition-colors"
            >
              Read the full heal log →
            </Link>
          </div>
        </FadeIn>

        <FadeIn delay={0.12}>
          <div className="space-y-3">
            {list.map((h) => (
              <div
                key={h.id}
                className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-4 glow-card"
              >
                <div className="flex items-center gap-2.5">
                  <span className="text-base">{h.icon || "🩹"}</span>
                  <span className="text-[13px] font-semibold">{h.module_label}</span>
                  <Badge
                    className={
                      h.success === "true"
                        ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/20 text-[10px] ml-auto"
                        : "bg-red-500/10 text-red-300 border-red-500/20 text-[10px] ml-auto"
                    }
                  >
                    {h.success === "true" ? "healed ✓" : "failed"}
                  </Badge>
                </div>
                <p className="text-[12.5px] text-muted-foreground mt-2 leading-relaxed">{h.description}</p>
              </div>
            ))}
          </div>
        </FadeIn>
      </div>
    </section>
  );
}
