export const dynamic = "force-dynamic";
import Layout from "@/components/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { fetchHealEvents } from "@/lib/api";

export default async function HealLog() {
  const heals = await fetchHealEvents();
  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Self-Healing Log</h2>
          <p className="text-slate-500">Every time a scraper was repaired after a layout change.</p>
        </div>
        <div className="space-y-3">
          {heals.map((h: any) => (
            <Card key={h.id}>
              <CardHeader className="pb-2 flex flex-row items-center gap-3">
                <Badge variant={h.success === "true" ? "default" : "destructive"}>{h.success === "true" ? "Success" : "Failed"}</Badge>
                <CardTitle className="text-base">Source #{h.source_id}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600">{h.description}</p>
                <p className="text-xs text-slate-400 mt-2">{new Date(h.created_at).toLocaleString()}</p>
              </CardContent>
            </Card>
          ))}
          {heals.length === 0 && <p className="text-slate-500">No heal events recorded yet.</p>}
        </div>
      </div>
    </Layout>
  );
}
