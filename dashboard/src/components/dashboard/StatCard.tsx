"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { NumberTicker } from "@/components/magic/NumberTicker";
import { Sparkline } from "@/components/magic/Sparkline";
import { cn } from "@/lib/utils";

export function StatCard({
  label,
  value,
  suffix = "",
  prefix = "",
  sub,
  subTone = "muted",
  spark,
  color = "#6366f1",
}: {
  label: string;
  value: number;
  suffix?: string;
  prefix?: string;
  sub?: string;
  subTone?: "ok" | "warn" | "muted";
  spark?: { t: string; v: number }[];
  color?: string;
}) {
  return (
    <Card className="glow-card overflow-hidden relative group transition-colors hover:border-white/15">
      <CardHeader className="pb-1 pt-4 px-4">
        <CardTitle className="text-[12px] font-medium uppercase tracking-wider text-muted-foreground">
          {label}
        </CardTitle>
      </CardHeader>
      <CardContent className="px-4 pb-3">
        <div className="text-[30px] font-semibold tracking-tight leading-none">
          <NumberTicker value={value} suffix={suffix} prefix={prefix} />
        </div>
        {sub && (
          <div
            className={cn(
              "text-[12px] mt-2",
              subTone === "ok" && "text-emerald-400/80",
              subTone === "warn" && "text-amber-400/80",
              subTone === "muted" && "text-muted-foreground"
            )}
          >
            {sub}
          </div>
        )}
      </CardContent>
      {spark && (
        <div className="px-2 pb-1 opacity-90 group-hover:opacity-100 transition-opacity">
          <Sparkline data={spark} color={color} id={label.replace(/\s+/g, "-").toLowerCase()} height={40} />
        </div>
      )}
    </Card>
  );
}
