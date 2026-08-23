"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { ClientOnly } from "@/components/magic/ClientOnly";

const COLORS: Record<string, string> = {
  created: "#34d399",
  updated: "#fbbf24",
  deleted: "#f87171",
  new_notices: "#38bdf8",
};

const LABELS: Record<string, string> = {
  created: "Created",
  updated: "Updated",
  deleted: "Deleted",
  new_notices: "New notices",
};

export function ChangeTypeDonut({
  data,
  total,
}: {
  data: { type: string; count: number }[];
  total: number;
}) {
  return (
    <Card className="glow-card h-full">
      <CardHeader>
        <CardTitle className="text-[15px] font-semibold tracking-tight">Change Composition</CardTitle>
        <CardDescription className="text-[12px]">What kind of diffs the diff engine caught</CardDescription>
      </CardHeader>
      <CardContent>
        <ClientOnly fallback={<div className="h-[190px]" />}>
        <div className="h-[190px] relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey="count"
                nameKey="type"
                innerRadius={58}
                outerRadius={80}
                paddingAngle={3}
                strokeWidth={0}
                animationDuration={1000}
              >
                {data.map((entry, i) => (
                  <Cell key={i} fill={COLORS[entry.type] || "#818cf8"} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "#161718",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: 10,
                  fontSize: 12,
                }}
                formatter={(v, n) => [`${v} changes`, LABELS[String(n)] || String(n)]}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="absolute inset-0 grid place-items-center pointer-events-none">
            <div className="text-center">
              <div className="text-[26px] font-semibold tabular leading-none">{total}</div>
              <div className="text-[11px] text-muted-foreground mt-1">total changes</div>
            </div>
          </div>
        </div>
        </ClientOnly>
        <div className="flex flex-wrap gap-x-4 gap-y-1.5 mt-2 justify-center">
          {data.map((d) => (
            <div key={d.type} className="flex items-center gap-1.5 text-[12px] text-muted-foreground">
              <span className="size-2 rounded-full" style={{ background: COLORS[d.type] || "#818cf8" }} />
              {LABELS[d.type] || d.type}
              <span className="tabular text-foreground/80">{d.count}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
