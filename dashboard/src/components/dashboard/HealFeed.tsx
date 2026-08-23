"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";

interface Heal {
  id: number;
  module: string;
  module_label: string;
  icon: string;
  description: string;
  success: string;
  created_at: string;
}

function relTime(iso: string) {
  const then = new Date(iso + (iso.includes("Z") ? "" : "Z"));
  const mins = Math.max(1, Math.round((Date.now() - then.getTime()) / 60000));
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.round(hrs / 24)}d ago`;
}

export function HealFeed({ heals }: { heals: Heal[] }) {
  return (
    <Card className="glow-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-[15px] font-semibold tracking-tight">Self-Healing Engine</CardTitle>
            <CardDescription className="text-[12px]">
              Every time a target site changed layout, the scraper regenerated itself — automatically.
            </CardDescription>
          </div>
          <Link href="/heal-log">
            <Badge variant="outline" className="text-[11px] hover:bg-white/5">
              Full log →
            </Badge>
          </Link>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[220px] pr-3">
          <div className="relative space-y-0">
            {heals.map((h, i) => (
              <div key={h.id} className="flex gap-3 relative pb-5">
                {i < heals.length - 1 && (
                  <span className="absolute left-[15px] top-8 bottom-0 w-px bg-border" />
                )}
                <div className="size-8 rounded-lg bg-white/[0.04] border border-border grid place-items-center text-sm shrink-0 z-10">
                  {h.icon || "🩹"}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-[13px] font-medium">{h.module_label || h.module}</span>
                    <Badge
                      className={
                        h.success === "true"
                          ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/20 text-[10px]"
                          : "bg-red-500/10 text-red-300 border-red-500/20 text-[10px]"
                      }
                    >
                      {h.success === "true" ? "healed ✓" : "failed"}
                    </Badge>
                    <span className="text-[11px] text-muted-foreground ml-auto tabular">
                      {relTime(h.created_at)}
                    </span>
                  </div>
                  <p className="text-[12px] text-muted-foreground mt-1 leading-relaxed">{h.description}</p>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
