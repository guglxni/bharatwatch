export const dynamic = "force-dynamic";
import Layout from "@/components/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { fetchHealth, fetchChanges, fetchHealEvents } from "@/lib/api";

export default async function Home() {
  const health = await fetchHealth();
  const changes = await fetchChanges("nauktrialert");
  const heals = await fetchHealEvents();

  return (
    <Layout>
      <div className="max-w-5xl mx-auto space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Overview</h2>
          <p className="text-slate-500">Real-time intelligence from Indian public data.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card><CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-slate-500">Sources</CardTitle></CardHeader><CardContent><div className="text-3xl font-bold">{health.sources}</div></CardContent></Card>
          <Card><CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-slate-500">Healthy</CardTitle></CardHeader><CardContent><div className="text-3xl font-bold text-green-600">{health.healthy}</div></CardContent></Card>
          <Card><CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-slate-500">Recent Changes</CardTitle></CardHeader><CardContent><div className="text-3xl font-bold text-orange-600">{changes.length}</div></CardContent></Card>
        </div>

        <Card>
          <CardHeader><CardTitle>Latest Changes</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-2">
              {changes.slice(0, 10).map((c: any) => (
                <div key={c.id} className="flex items-start gap-3 p-3 rounded-lg border border-slate-100 bg-slate-50">
                  <Badge variant={c.change_type === "created" ? "default" : c.change_type === "updated" ? "secondary" : "destructive"}>{c.change_type}</Badge>
                  <div className="text-sm">
                    <div className="font-medium">{c.after?.title || c.before?.title}</div>
                    <div className="text-slate-500">{c.after?.department || c.before?.department}</div>
                  </div>
                </div>
              ))}
              {changes.length === 0 && <p className="text-slate-500 text-sm">No changes detected yet.</p>}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Heal Events</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-2">
              {heals.slice(0, 5).map((h: any) => (
                <div key={h.id} className="flex items-start gap-3 p-3 rounded-lg border border-slate-100 bg-slate-50">
                  <Badge variant={h.success === "true" ? "default" : "destructive"}>{h.success === "true" ? "Healed" : "Failed"}</Badge>
                  <div className="text-sm">
                    <div className="font-medium">Source #{h.source_id}</div>
                    <div className="text-slate-500 truncate max-w-md">{h.description}</div>
                  </div>
                </div>
              ))}
              {heals.length === 0 && <p className="text-slate-500 text-sm">No heal events yet.</p>}
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
