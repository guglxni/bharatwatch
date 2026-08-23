"use client";

import Link from "next/link";
import { FadeIn } from "@/components/magic/Reveal";

export function FinalCTA() {
  return (
    <section className="py-24">
      <div className="max-w-4xl mx-auto px-6">
        <FadeIn>
          <div className="border-beam rounded-2xl border border-white/10 bg-gradient-to-b from-white/[0.04] to-transparent p-10 md:p-14 text-center glow-card">
            <h2 className="text-[32px] md:text-[40px] font-semibold tracking-[-0.03em] leading-[1.1]">
              See Bharat watching itself.
            </h2>
            <p className="text-[15px] text-muted-foreground mt-4 max-w-xl mx-auto">
              Five collectors are running right now. Open the dashboard and watch the data move — live KPIs,
              7-day activity, and the self-heal trail.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 mt-8">
              <Link
                href="/dashboard"
                className="group rounded-xl bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-400 hover:to-violet-500 text-white text-[14px] font-medium px-7 py-3.5 shadow-lg shadow-indigo-500/30 transition-all hover:-translate-y-0.5"
              >
                Open the Live Dashboard
                <span className="inline-block transition-transform group-hover:translate-x-0.5 ml-1.5">→</span>
              </Link>
              <a
                href="https://github.com/guglxni/bharatwatch"
                target="_blank"
                className="rounded-xl bg-white/[0.04] hover:bg-white/[0.07] border border-white/10 text-[14px] font-medium px-7 py-3.5 transition-colors font-mono"
              >
                git clone bharatwatch
              </a>
            </div>
          </div>
        </FadeIn>
      </div>
    </section>
  );
}
