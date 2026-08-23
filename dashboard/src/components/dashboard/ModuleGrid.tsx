"use client";

import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sparkline } from "@/components/magic/Sparkline";
import { FadeIn } from "@/components/magic/Reveal";
import { cn } from "@/lib/utils";

interface Mod {
  id: string;
  label: string;
  icon: string;
  accent: string;
  health: string;
  item_count: number;
  changes_7d: number;
  sparkline: { t: string; v: number }[];
  collector_id: string;
}

export function ModuleGrid({ modules }: { modules: Mod[] }) {
  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-[15px] font-semibold tracking-tight">Live Collectors</h2>
        <span className="text-[12px] text-muted-foreground">{modules.length} modules · all Bright Data custom scrapers</span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {modules.map((m, i) => (
          <FadeIn key={m.id} delay={i * 0.06}>
            <Link href={`/dashboard/${m.id}`}>
              <Card className="glow-card group hover:border-white/15 transition-all duration-200 hover:-translate-y-0.5 overflow-hidden h-full">
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div
                        className={cn(
                          "size-10 rounded-xl grid place-items-center text-lg bg-gradient-to-br text-white shadow-lg",
                          m.accent
                        )}
                      >
                        {m.icon}
                      </div>
                      <div>
                        <div className="text-[14px] font-semibold tracking-tight">{m.label}</div>
                        <div className="text-[11px] text-muted-foreground font-mono truncate max-w-[130px]">
                          {m.collector_id}
                        </div>
                      </div>
                    </div>
                    <Badge
                      className={cn(
                        "border text-[11px] gap-1",
                        m.health === "healthy"
                          ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"
                          : "bg-red-500/10 text-red-300 border-red-500/20"
                      )}
                    >
                      <span className={cn("size-1.5 rounded-full", m.health === "healthy" ? "bg-emerald-400 live-dot" : "bg-red-400")} />
                      {m.health === "healthy" ? "Live" : "Down"}
                    </Badge>
                  </div>

                  <div className="mt-4 grid grid-cols-2 gap-3">
                    <div>
                      <div className="text-[20px] font-semibold tabular leading-none">{m.item_count}</div>
                      <div className="text-[11px] text-muted-foreground mt-1">records live</div>
                    </div>
                    <div>
                      <div className="text-[20px] font-semibold tabular leading-none text-amber-300/90">{m.changes_7d}</div>
                      <div className="text-[11px] text-muted-foreground mt-1">changes · 7d</div>
                    </div>
                  </div>

                  <Sparkline
                    data={m.sparkline}
                    id={m.id}
                    className="mt-3 -mx-1"
                    color={m.accent.includes("orange") ? "#fb923c" : m.accent.includes("blue") ? "#38bdf8" : m.accent.includes("green") ? "#34d399" : m.accent.includes("violet") ? "#a78bfa" : "#f472b6"}
                    height={44}
                  />
                </CardContent>
              </Card>
            </Link>
          </FadeIn>
        ))}
      </div>
    </div>
  );
}
