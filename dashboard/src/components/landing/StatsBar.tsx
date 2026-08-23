"use client";

import { FadeIn } from "@/components/magic/Reveal";
import { NumberTicker } from "@/components/magic/NumberTicker";
import type { Overview } from "@/lib/api";

export function StatsBar({ overview }: { overview: Overview | null }) {
  const stats = [
    { v: overview?.sources ?? 5, label: "Live custom scrapers", suffix: "" },
    { v: overview?.total_items ?? 32, label: "Records in latest sync", suffix: "" },
    { v: overview?.total_changes_7d ?? 48, label: "Changes caught this week", suffix: "" },
    { v: overview ? Math.round((overview.heal_success / Math.max(1, overview.heal_events)) * 100) : 100, label: "Self-heal success rate", suffix: "%" },
  ];
  return (
    <section className="py-20">
      <FadeIn>
        <div className="max-w-6xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-4">
          {stats.map((s, i) => (
            <div
              key={s.label}
              className="text-center relative"
            >
              {i > 0 && (
                <div className="hidden md:block absolute left-0 top-1/2 -translate-y-1/2 w-px h-12 bg-white/5" />
              )}
              <div className="text-[40px] md:text-[46px] font-semibold tracking-[-0.03em] tabular">
                <NumberTicker value={s.v} suffix={s.suffix} />
              </div>
              <div className="text-[13px] text-muted-foreground mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </FadeIn>
    </section>
  );
}
