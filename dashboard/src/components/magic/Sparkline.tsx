"use client";

import { AreaChart, Area, ResponsiveContainer } from "recharts";
import { ClientOnly } from "./ClientOnly";

export function Sparkline({
  data,
  color = "#6366f1",
  id,
  className,
  height = 44,
}: {
  data: { t: string; v: number }[];
  color?: string;
  id: string;
  className?: string;
  height?: number;
}) {
  return (
    <ClientOnly
      fallback={
        <div style={{ height }} className={className} />
      }
    >
      <div className={className} style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 4, right: 0, bottom: 0, left: 0 }}>
            <defs>
              <linearGradient id={`spark-${id}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={color} stopOpacity={0.35} />
                <stop offset="100%" stopColor={color} stopOpacity={0} />
              </linearGradient>
            </defs>
            <Area
              type="monotone"
              dataKey="v"
              stroke={color}
              strokeWidth={2}
              fill={`url(#spark-${id})`}
              isAnimationActive={true}
              animationDuration={900}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </ClientOnly>
  );
}
