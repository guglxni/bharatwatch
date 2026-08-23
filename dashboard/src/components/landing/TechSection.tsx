"use client";

import { FadeIn } from "@/components/magic/Reveal";

const STACK = [
  { icon: "🕷️", name: "Bright Data Scraper Studio", desc: "AI-generated custom collectors + self-healing via bdata CLI" },
  { icon: "🐍", name: "FastAPI + SQLite", desc: "Orchestrator, diff engine, snapshot storage & REST API" },
  { icon: "⚛️", name: "Next.js 16 + shadcn/ui", desc: "Dark-native dashboard with recharts visualisation" },
  { icon: "🧪", name: "Pydantic Schemas", desc: "Every record validated against per-module typed schemas" },
  { icon: "🚀", name: "GitHub Actions", desc: "Scheduled scrapes, heal monitors & CI validation" },
  { icon: "📦", name: "Public Data Only", desc: "No logins, no paywalls, no personal data — ever" },
];

export function TechSection() {
  return (
    <section className="py-24">
      <div className="max-w-6xl mx-auto px-6">
        <FadeIn>
          <div className="max-w-2xl mb-12">
            <div className="text-[12px] uppercase tracking-[0.12em] text-indigo-400 font-semibold mb-3">
              Under the hood
            </div>
            <h2 className="text-[34px] md:text-[42px] font-semibold tracking-[-0.03em] leading-[1.1]">
              Small stack, sharp edges.
            </h2>
          </div>
        </FadeIn>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {STACK.map((t, i) => (
            <FadeIn key={t.name} delay={i * 0.05}>
              <div className="flex items-start gap-3.5 rounded-xl border border-white/[0.07] bg-white/[0.02] p-5 glow-card hover:border-white/15 transition-colors">
                <div className="text-xl">{t.icon}</div>
                <div>
                  <div className="text-[14px] font-semibold tracking-tight">{t.name}</div>
                  <div className="text-[12.5px] text-muted-foreground mt-1 leading-relaxed">{t.desc}</div>
                </div>
              </div>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}
