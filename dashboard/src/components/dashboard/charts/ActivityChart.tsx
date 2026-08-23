"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { AreaChart, Area, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";
import { ClientOnly } from "@/components/magic/ClientOnly";

export function ActivityChart({ data }: { data: { date: string; changes: number }[] }) {
  return (
    <Card className="glow-card h-full">
      <CardHeader>
        <CardTitle className="text-[15px] font-semibold tracking-tight">Change Activity</CardTitle>
        <CardDescription className="text-[12px]">
          Records created, updated or dropped — last 7 days
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ClientOnly fallback={<div className="h-[260px]" />}>
        <div className="h-[260px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -14 }}>
              <defs>
                <linearGradient id="fillChanges" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid vertical={false} stroke="rgba(255,255,255,0.05)" />
              <XAxis
                dataKey="date"
                tickLine={false}
                axisLine={false}
                tick={{ fill: "#71717a", fontSize: 12 }}
                tickFormatter={(d: string) => d.slice(5)}
                minTickGap={28}
              />
              <YAxis
                tickLine={false}
                axisLine={false}
                tick={{ fill: "#71717a", fontSize: 12 }}
                allowDecimals={false}
              />
              <Tooltip
                contentStyle={{
                  background: "#161718",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: 10,
                  fontSize: 12,
                }}
                formatter={(v) => [`${v} changes`, "Changes"]}
                labelFormatter={(l) => `Date ${l}`}
                labelStyle={{ color: "#a1a1aa" }}
                itemStyle={{ color: "#f7f8f8" }}
              />
              <Area
                type="monotone"
                dataKey="changes"
                name="Changes"
                stroke="#6366f1"
                strokeWidth={2.5}
                fill="url(#fillChanges)"
                dot={{ r: 3, fill: "#6366f1", strokeWidth: 0 }}
                activeDot={{ r: 5 }}
                animationDuration={1100}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        </ClientOnly>
      </CardContent>
    </Card>
  );
}
