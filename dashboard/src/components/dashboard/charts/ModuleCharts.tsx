"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend,
} from "recharts";
import { ClientOnly } from "@/components/magic/ClientOnly";

export function ModuleBarChart({
  data,
  color = "#6366f1",
  valueLabel = "",
  height = 280,
  hideValue = false,
}: {
  data: { name: string; value: number }[];
  color?: string;
  valueLabel?: string;
  height?: number;
  hideValue?: boolean;
}) {
  return (
    <ClientOnly fallback={<div style={{ height }} className="w-full" />}>
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -8 }}>
          <defs>
            <linearGradient id={`bar-${color.replace("#", "")}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity={0.95} />
              <stop offset="100%" stopColor={color} stopOpacity={0.45} />
            </linearGradient>
          </defs>
          <CartesianGrid vertical={false} stroke="rgba(255,255,255,0.05)" />
          <XAxis
            dataKey="name"
            tickLine={false}
            axisLine={false}
            tick={{ fill: "#71717a", fontSize: 11 }}
            interval={0}
            tickFormatter={(v: string) => (v.length > 12 ? v.slice(0, 11) + "…" : v)}
          />
          <YAxis
            tickLine={false}
            axisLine={false}
            tick={{ fill: "#71717a", fontSize: 11 }}
            allowDecimals={false}
            width={52}
            tickFormatter={(v: number) => (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : String(v))}
          />
          <Tooltip
            cursor={{ fill: "rgba(255,255,255,0.04)" }}
            contentStyle={{
              background: "#161718",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: 10,
              fontSize: 12,
            }}
            formatter={(v) => [
              `${Number(v).toLocaleString("en-IN")} ${hideValue ? "" : valueLabel}`.trim(),
              hideValue ? "count" : valueLabel,
            ]}
            labelStyle={{ color: "#a1a1aa" }}
            itemStyle={{ color: "#f7f8f8" }}
          />
          <Bar
            dataKey="value"
            radius={[6, 6, 0, 0]}
            fill={`url(#bar-${color.replace("#", "")})`}
            animationDuration={900}
            maxBarSize={44}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
    </ClientOnly>
  );
}

export function ModulePriceChart({
  data,
  height = 280,
}: {
  data: { name: string; min: number; modal: number; max: number }[];
  height?: number;
}) {
  return (
    <ClientOnly fallback={<div style={{ height }} className="w-full" />}>
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -8 }}>
          <CartesianGrid vertical={false} stroke="rgba(255,255,255,0.05)" />
          <XAxis
            dataKey="name"
            tickLine={false}
            axisLine={false}
            tick={{ fill: "#71717a", fontSize: 11 }}
            interval={0}
          />
          <YAxis
            tickLine={false}
            axisLine={false}
            tick={{ fill: "#71717a", fontSize: 11 }}
            width={56}
            tickFormatter={(v: number) => (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : String(v))}
          />
          <Tooltip
            cursor={{ fill: "rgba(255,255,255,0.04)" }}
            contentStyle={{
              background: "#161718",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: 10,
              fontSize: 12,
            }}
            formatter={(v, n) => [`₹${Number(v).toLocaleString("en-IN")}/q`, String(n)]}
            labelStyle={{ color: "#a1a1aa" }}
            itemStyle={{ color: "#f7f8f8" }}
          />
          <Legend
            wrapperStyle={{ fontSize: 11, color: "#a1a1aa" }}
            iconType="circle"
            iconSize={8}
          />
          <Bar dataKey="min" name="Min" fill="#34d399" radius={[4, 4, 0, 0]} maxBarSize={18} animationDuration={900} />
          <Bar dataKey="modal" name="Modal" fill="#fbbf24" radius={[4, 4, 0, 0]} maxBarSize={18} animationDuration={900} />
          <Bar dataKey="max" name="Max" fill="#f87171" radius={[4, 4, 0, 0]} maxBarSize={18} animationDuration={900} />
        </BarChart>
      </ResponsiveContainer>
    </div>
    </ClientOnly>
  );
}
