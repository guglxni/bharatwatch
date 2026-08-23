"use client";

import { FadeIn } from "@/components/magic/Reveal";

const SOURCES = [
  "SSC", "UPSC", "IBPS", "GeM e-Procurement", "Agmarknet", "JoSAA", "DPIIT",
  "Startup India", "RBI", "NIC", "CPWD", "MNRE",
];

export function SourceMarquee() {
  return (
    <section className="py-14 border-y border-white/5 bg-white/[0.01]">
      <FadeIn>
        <p className="text-center text-[12px] uppercase tracking-[0.12em] text-muted-foreground mb-7">
          Watching public data across
        </p>
        <div className="relative overflow-hidden marquee-mask">
          <div className="flex w-max animate-marquee gap-14 px-7 hover:[animation-play-state:paused]">
            {[...SOURCES, ...SOURCES].map((s, i) => (
              <div
                key={i}
                className="text-[15px] font-medium text-muted-foreground/60 hover:text-foreground/80 transition-colors whitespace-nowrap tracking-tight"
              >
                {s}
              </div>
            ))}
          </div>
        </div>
      </FadeIn>
    </section>
  );
}
