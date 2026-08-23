export const dynamic = "force-dynamic";
import { notFound } from "next/navigation";
import { DashboardShell } from "@/components/dashboard/Shell";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ModuleBarChart, ModulePriceChart } from "@/components/dashboard/charts/ModuleCharts";
import { fetchModuleData, fetchModuleHistory, fetchSources } from "@/lib/api";
import { cn } from "@/lib/utils";

const MODULE_IDS = ["nauktrialert", "tendersentry", "mandiwatch", "collegecutoff", "startuppulse"];

// per-module table column definitions: [key, label, align]
const COLUMNS: Record<string, [string, string, "left" | "right"][]> = {
  nauktrialert: [
    ["title", "Notification", "left"],
    ["department", "Department", "left"],
    ["notification_date", "Notified", "left"],
    ["last_application_date", "Apply by", "left"],
    ["exam_date", "Exam date", "left"],
    ["number_of_vacancies", "Vacancies", "right"],
    ["qualification_required", "Qualification", "left"],
  ],
  tendersentry: [
    ["tender_id", "Tender ID", "left"],
    ["title", "Title", "left"],
    ["department", "Department", "left"],
    ["estimated_value", "Value (₹)", "right"],
    ["closing_date", "Closes", "left"],
  ],
  mandiwatch: [
    ["state", "State", "left"],
    ["mandi", "Mandi", "left"],
    ["crop", "Crop", "left"],
    ["variety", "Variety", "left"],
    ["min_price", "Min ₹/q", "right"],
    ["modal_price", "Modal ₹/q", "right"],
    ["max_price", "Max ₹/q", "right"],
    ["date", "Date", "left"],
  ],
  collegecutoff: [
    ["institute", "Institute", "left"],
    ["branch", "Branch", "left"],
    ["round", "Round", "left"],
    ["opening_rank", "Opening rank", "right"],
    ["closing_rank", "Closing rank", "right"],
    ["status", "Status", "left"],
  ],
  startuppulse: [
    ["title", "Scheme", "left"],
    ["ministry", "Ministry", "left"],
    ["scheme_type", "Type", "left"],
    ["deadline", "Deadline", "left"],
    ["summary", "Summary", "left"],
  ],
};

function fmtCell(key: string, value: unknown): React.ReactNode {
  if (value === null || value === undefined) return "—";
  if (typeof value === "number") return value.toLocaleString("en-IN");
  if (key === "estimated_value" && typeof value === "number") return value.toLocaleString("en-IN");
  if (key === "status") {
    return (
      <Badge
        className={cn(
          "text-[10px]",
          String(value).toLowerCase() === "open" || String(value).toLowerCase() === "closed"
            ? String(value).toLowerCase() === "open"
              ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"
              : "bg-zinc-500/10 text-zinc-300 border-zinc-500/20"
            : "bg-zinc-500/10 text-zinc-300 border-zinc-500/20"
        )}
      >
        {String(value)}
      </Badge>
    );
  }
  return String(value);
}

export default async function ModulePage({ params }: { params: Promise<{ module: string }> }) {
  const { module } = await params;
  if (!MODULE_IDS.includes(module)) notFound();

  const [data, hist, sources] = await Promise.all([
    fetchModuleData(module),
    fetchModuleHistory(module),
    fetchSources(module),
  ]);

  const cols = COLUMNS[module];
  const items = data.items;

  // ---- chart data per module ----
  let chartTitle = "";
  let chartDesc = "";
  let chart = null as React.ReactNode;

  if (module === "nauktrialert") {
    chartTitle = "Vacancies by notification";
    chartDesc = "Total open posts per exam — from the latest scrape";
    chart = (
      <ModuleBarChart
        data={items.map((i) => ({
          name: String(i.title || "").replace(/\s+\d{4}$/, ""),
          value: Number(i.number_of_vacancies) || 0,
        }))}
        color="#fb923c"
        valueLabel="vacancies"
      />
    );
  } else if (module === "tendersentry") {
    chartTitle = "Tender value pipeline";
    chartDesc = "Estimated value (₹ lakh) of tracked live tenders";
    chart = (
      <ModuleBarChart
        data={items.map((i) => ({
          name: String(i.tender_id || "").split("/").slice(-1)[0],
          value: Math.round((Number(i.estimated_value) || 0) / 100000) / 10,
        }))}
        color="#38bdf8"
        valueLabel="₹ lakh"
      />
    );
  } else if (module === "mandiwatch") {
    chartTitle = "Mandi price range";
    chartDesc = "Min / modal / max price per crop (₹ per quintal)";
    chart = (
      <ModulePriceChart
        data={items.map((i) => ({
          name: String(i.crop || ""),
          min: Number(i.min_price) || 0,
          modal: Number(i.modal_price) || 0,
          max: Number(i.max_price) || 0,
        }))}
      />
    );
  } else if (module === "collegecutoff") {
    chartTitle = "Closing ranks";
    chartDesc = "Round-wise closing rank — lower is tougher";
    chart = (
      <ModuleBarChart
        data={items.slice(0, 8).map((i) => ({
          name: `${String(i.institute || "").replace("IIT ", "").replace("NIT ", "NIT-")}`,
          value: Number(i.closing_rank) || 0,
        }))}
        color="#a78bfa"
        valueLabel="rank"
      />
    );
  } else if (module === "startuppulse") {
    chartTitle = "Active schemes";
    chartDesc = "By scheme type — funding, grants, incentives & more";
    chart = (
      <ModuleBarChart
        data={items.map((i) => ({
          name: String(i.title || "").split(" ").slice(0, 2).join(" "),
          value: 1,
        }))}
        color="#f472b6"
        valueLabel="scheme"
        hideValue
      />
    );
  }

  return (
    <DashboardShell>
      <div className="max-w-[1400px] mx-auto space-y-6">
        {/* Module hero header */}
        <div
          className={cn(
            "rounded-2xl border border-border p-6 md:p-8 relative overflow-hidden glow-card"
          )}
        >
          <div className="absolute inset-0 hero-glow opacity-60 pointer-events-none" />
          <div className="relative flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div
                className={cn(
                  "size-14 rounded-2xl grid place-items-center text-2xl bg-gradient-to-br text-white shadow-xl",
                  data.meta.accent
                )}
              >
                {data.meta.icon}
              </div>
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-2xl font-semibold tracking-tight">{data.meta.label}</h1>
                  <Badge
                    className={cn(
                      "gap-1.5 border",
                      data.source.health === "healthy"
                        ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"
                        : "bg-red-500/10 text-red-300 border-red-500/20"
                    )}
                  >
                    <span
                      className={cn(
                        "size-1.5 rounded-full",
                        data.source.health === "healthy" ? "bg-emerald-400 live-dot" : "bg-red-400"
                      )}
                    />
                    {data.source.health === "healthy" ? "Live" : "Down"}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground mt-1">{data.meta.tagline}</p>
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              <div className="rounded-lg border border-border bg-white/[0.03] px-3 py-2">
                <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Collector</div>
                <div className="text-[12px] font-mono mt-0.5">{data.source.collector_id}</div>
              </div>
              <div className="rounded-lg border border-border bg-white/[0.03] px-3 py-2">
                <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Records</div>
                <div className="text-[15px] font-semibold tabular mt-0.5">{items.length}</div>
              </div>
              <div className="rounded-lg border border-border bg-white/[0.03] px-3 py-2">
                <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Snapshots</div>
                <div className="text-[15px] font-semibold tabular mt-0.5">{hist.history.length}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Charts row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <Card className="glow-card lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-[15px] font-semibold tracking-tight">{chartTitle}</CardTitle>
              <CardDescription className="text-[12px]">{chartDesc}</CardDescription>
            </CardHeader>
            <CardContent>{chart}</CardContent>
          </Card>

          <Card className="glow-card">
            <CardHeader>
              <CardTitle className="text-[15px] font-semibold tracking-tight">Snapshot History</CardTitle>
              <CardDescription className="text-[12px]">Records per scrape — 7 days</CardDescription>
            </CardHeader>
            <CardContent>
              <ModuleBarChart
                data={hist.history.map((h) => ({ name: h.t.slice(5, 10), value: h.items }))}
                color="#6366f1"
                valueLabel="records"
                height={240}
              />
            </CardContent>
          </Card>
        </div>

        {/* Live data table */}
        <Card className="glow-card overflow-hidden">
          <CardHeader>
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div>
                <CardTitle className="text-[15px] font-semibold tracking-tight">Live Extracted Data</CardTitle>
                <CardDescription className="text-[12px]">
                  Latest snapshot from {data.source.name}
                  {data.captured_at && ` · captured ${new Date(data.captured_at).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}`}
                </CardDescription>
              </div>
              <Badge variant="outline" className="text-[11px] font-mono">
                {items.length} rows
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="px-0 pb-0">
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="hover:bg-transparent border-b">
                    {cols.map(([key, label, align]) => (
                      <TableHead
                        key={key}
                        className={cn(
                          "text-[11px] uppercase tracking-wider text-muted-foreground font-semibold h-10",
                          align === "right" && "text-right"
                        )}
                      >
                        {label}
                      </TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {items.map((item, idx) => (
                    <TableRow key={idx} className="border-b border-border/50 hover:bg-white/[0.02]">
                      {cols.map(([key, , align]) => (
                        <TableCell
                          key={key}
                          className={cn(
                            "text-[13px] py-3 max-w-[260px] truncate",
                            align === "right" && "text-right tabular",
                            key === "title" && "font-medium"
                          )}
                          title={String(item[key] ?? "")}
                        >
                          {fmtCell(key, item[key])}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>

        {/* Change log */}
        <Card className="glow-card">
          <CardHeader>
            <CardTitle className="text-[15px] font-semibold tracking-tight">Detected Changes</CardTitle>
            <CardDescription className="text-[12px]">
              Diff engine output — new records and field-level updates between snapshots
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {hist.changes.slice(0, 8).map((c) => {
                const item = (c.after || c.before) as Record<string, unknown>;
                const label =
                  String(item?.title || item?.tender_id || item?.crop || item?.institute || "record");
                return (
                  <div
                    key={c.id}
                    className="flex items-center gap-3 p-3 rounded-lg border border-border/60 bg-white/[0.02]"
                  >
                    <Badge
                      className={cn(
                        "text-[10px] w-[74px] justify-center",
                        c.change_type === "created" && "bg-emerald-500/10 text-emerald-300 border-emerald-500/20",
                        c.change_type === "updated" && "bg-amber-500/10 text-amber-300 border-amber-500/20",
                        c.change_type === "deleted" && "bg-red-500/10 text-red-300 border-red-500/20",
                        c.change_type === "new_notices" && "bg-sky-500/10 text-sky-300 border-sky-500/20"
                      )}
                    >
                      {c.change_type}
                    </Badge>
                    <span className="text-[13px] font-medium truncate">{label}</span>
                    <span className="text-[11px] text-muted-foreground ml-auto tabular shrink-0">
                      {new Date(c.detected_at).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}
                    </span>
                  </div>
                );
              })}
              {hist.changes.length === 0 && (
                <p className="text-sm text-muted-foreground py-6 text-center">
                  No changes detected yet — the diff engine fires when a snapshot differs from the previous one.
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  );
}
