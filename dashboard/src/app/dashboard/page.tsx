export const dynamic = "force-dynamic";
import { DashboardShell } from "@/components/dashboard/Shell";
import { StatCard } from "@/components/dashboard/StatCard";
import { ActivityChart } from "@/components/dashboard/charts/ActivityChart";
import { ChangeTypeDonut } from "@/components/dashboard/charts/ChangeTypeDonut";
import { ModuleGrid } from "@/components/dashboard/ModuleGrid";
import { HealFeed } from "@/components/dashboard/HealFeed";
import { fetchOverview, fetchHealEvents, fetchModules, fetchChanges } from "@/lib/api";

export default async function DashboardPage() {
  const [overview, heals, mods] = await Promise.all([
    fetchOverview(),
    fetchHealEvents(),
    fetchModules(),
  ]);

  // change-type composition across all modules
  const allChanges = await Promise.all(
    mods.modules.map((m) => fetchChanges(m.id).catch(() => []))
  );
  const typeCounts: Record<string, number> = {};
  for (const list of allChanges) {
    for (const c of list) {
      typeCounts[c.change_type] = (typeCounts[c.change_type] || 0) + 1;
    }
  }
  const donutData = Object.entries(typeCounts).map(([type, count]) => ({ type, count }));

  return (
    <DashboardShell>
      <div className="max-w-[1400px] mx-auto space-y-6">
        {/* Title row */}
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">Mission Control</h1>
            <p className="text-sm text-muted-foreground mt-1">
              Five live scrapers watching India&apos;s public data — self-healing on every layout change.
            </p>
          </div>
          <div className="text-[13px] text-muted-foreground tabular">
            Last sync: {new Date().toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}
          </div>
        </div>

        {/* KPI row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <StatCard
            label="Live Sources"
            value={overview.sources}
            suffix=""
            sub={`${overview.healthy} healthy · 0 degraded`}
            subTone="ok"
            spark={overview.activity_series.map((a) => ({ t: a.date, v: a.changes }))}
            color="#6366f1"
          />
          <StatCard
            label="Records Extracted"
            value={overview.total_items}
            suffix=""
            sub="across all collectors, latest snapshot"
            spark={overview.activity_series.map((a) => ({ t: a.date, v: a.changes }))}
            color="#38bdf8"
          />
          <StatCard
            label="Changes — 7 days"
            value={overview.total_changes_7d}
            suffix=""
            sub="new & updated records detected"
            subTone="warn"
            spark={overview.activity_series.map((a) => ({ t: a.date, v: a.changes }))}
            color="#fbbf24"
          />
          <StatCard
            label="Self-Heals"
            value={overview.heal_events}
            suffix=""
            sub={`${overview.heal_success}/${overview.heal_events} successful recoveries`}
            subTone="ok"
            spark={overview.activity_series.map((a) => ({ t: a.date, v: a.changes }))}
            color="#34d399"
          />
        </div>

        {/* Charts row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <ActivityChart data={overview.activity_series} />
          </div>
          <ChangeTypeDonut data={donutData} total={donutData.reduce((s, d) => s + d.count, 0)} />
        </div>

        {/* Module cards */}
        <ModuleGrid modules={overview.modules} />

        {/* Heal feed */}
        <HealFeed heals={heals} />
      </div>
    </DashboardShell>
  );
}
