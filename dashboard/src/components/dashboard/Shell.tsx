import Link from "next/link";
import { ShellNav } from "./ShellNav";
import { LivePill } from "./LivePill";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-sidebar hidden md:flex flex-col fixed inset-y-0 z-40">
        <div className="px-5 h-16 flex items-center gap-2.5 border-b border-border">
          <div className="size-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 grid place-items-center text-white text-sm font-bold shadow-lg shadow-indigo-500/25">
            भ
          </div>
          <div>
            <div className="text-[15px] font-semibold tracking-tight leading-none">BharatWatch</div>
            <div className="text-[11px] text-muted-foreground mt-0.5">Local Intelligence</div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto py-4 px-3">
          <ShellNav />
        </div>

        {/* footer card */}
        <div className="p-3 border-t border-border">
          <div className="rounded-xl bg-white/[0.03] border border-border p-3.5 glow-card">
            <div className="flex items-center gap-2 text-[12px] font-medium text-foreground/90">
              <span className="relative size-1.5 rounded-full bg-emerald-400 live-dot" />
              All collectors operational
            </div>
            <div className="text-[11px] text-muted-foreground mt-1.5 leading-relaxed">
              Powered by Bright Data Scraper Studio · WeMakeDevs hackathon
            </div>
          </div>
        </div>
      </aside>

      {/* Main column */}
      <div className="flex-1 md:ml-64 flex flex-col min-h-screen">
        {/* Header */}
        <header className="h-16 border-b border-border bg-background/80 backdrop-blur-xl sticky top-0 z-30 flex items-center justify-between px-6">
          <div className="flex items-center gap-3">
            <Link href="/" className="md:hidden">
              <div className="size-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 grid place-items-center text-white text-sm font-bold">
                भ
              </div>
            </Link>
            <div className="text-sm text-muted-foreground">
              BharatWatch <span className="mx-1.5 text-border">/</span>
              <span className="text-foreground">Mission Control</span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <LivePill />
            <Link
              href="https://github.com/guglxni/bharatwatch"
              target="_blank"
              className="text-[13px] text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1.5"
            >
              <svg className="size-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
              </svg>
              GitHub
            </Link>
          </div>
        </header>

        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
