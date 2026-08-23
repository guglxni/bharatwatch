"use client";

import Link from "next/link";
import { BlurIn, FadeInUp, Stagger, StaggerItem } from "@/components/magic/Reveal";

export function Hero() {
  return (
    <header className="relative overflow-hidden">
      {/* top nav */}
      <nav className="sticky top-0 z-50 border-b border-white/5 bg-background/70 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="size-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 grid place-items-center text-white text-sm font-bold shadow-lg shadow-indigo-500/25">
              भ
            </div>
            <span className="text-[15px] font-semibold tracking-tight">BharatWatch</span>
          </div>
          <div className="hidden md:flex items-center gap-7 text-[13px] text-muted-foreground">
            <a href="#features" className="hover:text-foreground transition-colors">Features</a>
            <a href="#how" className="hover:text-foreground transition-colors">How it works</a>
            <a href="#modules" className="hover:text-foreground transition-colors">Modules</a>
            <a href="#healing" className="hover:text-foreground transition-colors">Self-Healing</a>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="https://github.com/guglxni/bharatwatch"
              target="_blank"
              className="hidden sm:flex text-[13px] text-muted-foreground hover:text-foreground transition-colors items-center gap-1.5"
            >
              <svg className="size-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
              </svg>
              GitHub
            </Link>
            <Link
              href="/dashboard"
              className="text-[13px] font-medium rounded-lg bg-white/10 hover:bg-white/15 border border-white/10 px-3.5 py-1.5 transition-colors"
            >
              Live Dashboard →
            </Link>
          </div>
        </div>
      </nav>

      {/* hero */}
      <div className="relative hero-glow">
        <div className="max-w-6xl mx-auto px-6 pt-20 pb-24 text-center">
          <Stagger className="space-y-6">
            <StaggerItem>
              <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/25 bg-indigo-500/10 px-4 py-1.5">
                <span className="shimmer-text text-[13px] font-medium">
                  ✦ WeMakeDevs × Bright Data — Into the Scrape-Verse
                </span>
              </div>
            </StaggerItem>

            <StaggerItem>
              <BlurIn delay={0.1}>
                <h1 className="text-4xl md:text-[68px] font-semibold tracking-[-0.04em] leading-[1.05] max-w-4xl mx-auto">
                  India&apos;s public data,{" "}
                  <span className="text-gradient">watched for you.</span>
                </h1>
              </BlurIn>
            </StaggerItem>

            <StaggerItem>
              <p className="text-[17px] md:text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                Five live scrapers tracking govt job alerts, tenders, mandi prices, college cutoffs and
                startup schemes — powered by Bright Data Scraper Studio. When a site redesigns itself,
                <span className="text-foreground/90"> the scraper heals itself.</span>
              </p>
            </StaggerItem>

            <StaggerItem>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
                <Link
                  href="/dashboard"
                  className="group rounded-xl bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-400 hover:to-violet-500 text-white text-[14px] font-medium px-6 py-3 shadow-lg shadow-indigo-500/30 transition-all hover:shadow-indigo-500/40 hover:-translate-y-0.5"
                >
                  Open Live Dashboard
                  <span className="inline-block transition-transform group-hover:translate-x-0.5 ml-1.5">→</span>
                </Link>
                <a
                  href="https://github.com/guglxni/bharatwatch"
                  target="_blank"
                  className="rounded-xl bg-white/[0.04] hover:bg-white/[0.07] border border-white/10 text-[14px] font-medium px-6 py-3 transition-colors"
                >
                  View on GitHub
                </a>
              </div>
            </StaggerItem>

            <StaggerItem>
              <div className="pt-4 text-[13px] text-muted-foreground font-mono">
                5 live collectors · 100% self-heal success · 0 manual fixes
              </div>
            </StaggerItem>
          </Stagger>

          {/* dashboard preview mock */}
          <FadeInUp delay={0.5}>
            <div className="relative max-w-4xl mx-auto mt-16 rounded-2xl border border-white/10 bg-[#0f1011] shadow-[0_40px_80px_-30px_rgba(99,102,241,0.35)] overflow-hidden text-left">
              {/* window chrome */}
              <div className="flex items-center gap-2 px-4 py-3 border-b border-white/5 bg-white/[0.02]">
                <span className="size-2.5 rounded-full bg-red-400/70" />
                <span className="size-2.5 rounded-full bg-amber-400/70" />
                <span className="size-2.5 rounded-full bg-emerald-400/70" />
                <span className="ml-3 text-[11px] text-muted-foreground font-mono">
                  localhost:3000/dashboard
                </span>
              </div>
              {/* fake dashboard */}
              <div className="p-5 grid grid-cols-12 gap-3">
                <div className="col-span-3 space-y-3 hidden sm:block">
                  {["📊 Mission Control", "🔔 NaukriAlert", "📄 TenderSentry", "🌾 MandiWatch", "🎓 CollegeCutoff", "🚀 StartupPulse"].map((s, i) => (
                    <div
                      key={s}
                      className={`text-[12px] rounded-lg px-3 py-2 ${i === 0 ? "bg-indigo-500/15 text-indigo-200 border border-indigo-500/20" : "text-muted-foreground"}`}
                    >
                      {s}
                    </div>
                  ))}
                </div>
                <div className="col-span-12 sm:col-span-9 space-y-3">
                  <div className="grid grid-cols-3 gap-3">
                    {[
                      ["5", "Live Sources", "text-indigo-300"],
                      ["32", "Records", "text-sky-300"],
                      ["48", "Changes / 7d", "text-amber-300"],
                    ].map(([v, l, c]) => (
                      <div key={l} className="rounded-xl border border-white/5 bg-white/[0.03] p-3">
                        <div className={`text-[20px] font-semibold tabular ${c}`}>{v}</div>
                        <div className="text-[10px] text-muted-foreground mt-0.5">{l}</div>
                      </div>
                    ))}
                  </div>
                  <div className="rounded-xl border border-white/5 bg-white/[0.03] p-4 h-32 relative overflow-hidden">
                    <div className="text-[10px] uppercase tracking-wider text-muted-foreground mb-2">Change activity</div>
                    <svg viewBox="0 0 300 60" className="w-full h-16" preserveAspectRatio="none">
                      <defs>
                        <linearGradient id="heroArea" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#6366f1" stopOpacity="0.4" />
                          <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
                        </linearGradient>
                      </defs>
                      <path
                        d="M0,50 C30,45 45,30 75,32 C105,34 120,18 150,20 C180,22 195,38 225,30 C255,22 270,14 300,10 L300,60 L0,60 Z"
                        fill="url(#heroArea)"
                      />
                      <path
                        d="M0,50 C30,45 45,30 75,32 C105,34 120,18 150,20 C180,22 195,38 225,30 C255,22 270,14 300,10"
                        fill="none"
                        stroke="#6366f1"
                        strokeWidth="2"
                      />
                    </svg>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="rounded-xl border border-emerald-500/15 bg-emerald-500/[0.05] p-3">
                      <div className="flex items-center gap-2 text-[11px] font-medium text-emerald-300">
                        <span className="size-1.5 rounded-full bg-emerald-400 live-dot relative" /> All collectors operational
                      </div>
                      <div className="text-[10px] text-muted-foreground mt-1">SSC · GeM · Agmarknet · JoSAA · DPIIT</div>
                    </div>
                    <div className="rounded-xl border border-indigo-500/15 bg-indigo-500/[0.05] p-3">
                      <div className="text-[11px] font-medium text-indigo-300">🩹 Self-heal event</div>
                      <div className="text-[10px] text-muted-foreground mt-1">Layout change detected → scraper regenerated ✓</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </FadeInUp>
        </div>
      </div>
    </header>
  );
}
