export const dynamic = "force-dynamic";
import { DashboardShell } from "@/components/dashboard/Shell";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { fetchHealEvents } from "@/lib/api";
import { FadeIn } from "@/components/magic/Reveal";
import { cn } from "@/lib/utils";

function relTime(iso: string) {
  const then = new Date(iso + (iso.includes("Z") ? "" : "Z"));
  const mins = Math.max(1, Math.round((Date.now() - then.getTime()) / 60000));
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.round(hrs / 24)}d ago`;
}

export default async function HealLogPage() {
  const heals = await fetchHealEvents();
  const successes = heals.filter((h) => h.success === "true").length;

  return (
    <DashboardShell>
      <div className="max-w-[900px] mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Self-Heal Log</h1>
          <p className="text-sm text-muted-foreground mt-1">
            When a target site changes its layout, the Bright Data AI regenerates the scraper&apos;s extraction
            code — no human intervention. This is the full audit trail.
          </p>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <Card className="glow-card">
            <CardContent className="p-4">
              <div className="text-[24px] font-semibold tabular">{heals.length}</div>
              <div className="text-[12px] text-muted-foreground">heal attempts</div>
            </CardContent>
          </Card>
          <Card className="glow-card">
            <CardContent className="p-4">
              <div className="text-[24px] font-semibold tabular text-emerald-300">{successes}</div>
              <div className="text-[12px] text-muted-foreground">successful</div>
            </CardContent>
          </Card>
          <Card className="glow-card">
            <CardContent className="p-4">
              <div className="text-[24px] font-semibold tabular text-emerald-300">
                {heals.length ? Math.round((successes / heals.length) * 100) : 0}%
              </div>
              <div className="text-[12px] text-muted-foreground">recovery rate</div>
            </CardContent>
          </Card>
        </div>

        <Card className="glow-card">
          <CardHeader>
            <CardTitle className="text-[15px] font-semibold tracking-tight">Audit Trail</CardTitle>
            <CardDescription className="text-[12px]">Most recent first</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative">
              {heals.map((h, i) => (
                <FadeIn key={h.id} delay={i * 0.05}>
                  <div className="flex gap-4 relative pb-6">
                    {i < heals.length - 1 && (
                      <span className="absolute left-[19px] top-10 bottom-0 w-px bg-border" />
                    )}
                    <div className="size-10 rounded-xl bg-white/[0.04] border border-border grid place-items-center text-lg shrink-0 z-10">
                      {h.icon || "🩹"}
                    </div>
                    <div className="min-w-0 flex-1 rounded-xl border border-border/70 bg-white/[0.02] p-4">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-[13px] font-semibold">{h.module_label || h.module}</span>
                        <Badge
                          className={cn(
                            "text-[10px]",
                            h.success === "true"
                              ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"
                              : "bg-red-500/10 text-red-300 border-red-500/20"
                          )}
                        >
                          {h.success === "true" ? "✓ healed" : "✗ failed"}
                        </Badge>
                        <span className="text-[11px] text-muted-foreground ml-auto tabular">
                          {relTime(h.created_at)}
                        </span>
                      </div>
                      <p className="text-[13px] text-muted-foreground mt-2 leading-relaxed">{h.description}</p>
                    </div>
                  </div>
                </FadeIn>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  );
}
