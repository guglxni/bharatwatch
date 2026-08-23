"use client";

export function LivePill() {
  return (
    <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1">
      <span className="relative size-1.5 rounded-full bg-emerald-400 live-dot" />
      <span className="text-[12px] font-medium text-emerald-300">Live</span>
      <span className="text-[11px] text-emerald-300/60 hidden sm:inline">5/5 collectors</span>
    </div>
  );
}
