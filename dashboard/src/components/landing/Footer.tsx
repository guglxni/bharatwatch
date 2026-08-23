"use client";

import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-white/5 py-12 mt-8">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
          <div>
            <div className="flex items-center gap-2.5">
              <div className="size-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 grid place-items-center text-white text-sm font-bold">
                भ
              </div>
              <span className="text-[15px] font-semibold tracking-tight">BharatWatch</span>
            </div>
            <p className="text-[13px] text-muted-foreground mt-3 max-w-xs leading-relaxed">
              Self-healing local intelligence for India. Public data only.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-x-16 gap-y-2 text-[13px]">
            <div className="space-y-2">
              <div className="text-[11px] uppercase tracking-wider text-muted-foreground/70 font-semibold mb-3">Product</div>
              <Link href="/dashboard" className="block text-muted-foreground hover:text-foreground transition-colors">Dashboard</Link>
              <Link href="/heal-log" className="block text-muted-foreground hover:text-foreground transition-colors">Heal Log</Link>
              <a href="#modules" className="block text-muted-foreground hover:text-foreground transition-colors">Modules</a>
            </div>
            <div className="space-y-2">
              <div className="text-[11px] uppercase tracking-wider text-muted-foreground/70 font-semibold mb-3">Project</div>
              <a href="https://github.com/guglxni/bharatwatch" target="_blank" className="block text-muted-foreground hover:text-foreground transition-colors">GitHub</a>
              <a href="https://brightdata.com" target="_blank" className="block text-muted-foreground hover:text-foreground transition-colors">Bright Data</a>
              <a href="https://wemakedevs.org" target="_blank" className="block text-muted-foreground hover:text-foreground transition-colors">WeMakeDevs</a>
            </div>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-3">
          <span className="text-[12px] text-muted-foreground">
            © 2026 BharatWatch · Built for Into the Scrape-Verse by Aaryan Guglani
          </span>
          <span className="flex items-center gap-2 text-[12px] text-muted-foreground">
            <span className="size-1.5 rounded-full bg-emerald-400" />
            All systems operational
          </span>
        </div>
      </div>
    </footer>
  );
}
