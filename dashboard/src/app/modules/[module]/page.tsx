export const dynamic = "force-dynamic";
import Layout from "@/components/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { fetchSources, fetchChanges } from "@/lib/api";

export default async function ModulePage({ params }: { params: { module: string } }) {
  const { module } = params;
  const sources = await fetchSources(module);
  const changes = await fetchChanges(module);

  return (
    <Layout>
      <div className="max-w-6xl mx-auto space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 capitalize">{module.replace(/-/g, " ")}</h2>
          <p className="text-slate-500">Live sources and detected changes.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sources.map((s: any) => (
            <Card key={s.id}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base">{s.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 text-sm">
                  <Badge variant={s.health === "healthy" ? "default" : "destructive"}>{s.health}</Badge>
                  <span className="text-slate-500">{s.last_run_at ? new Date(s.last_run_at).toLocaleString() : "Never"}</span>
                </div>
              </CardContent>
            </Card>
          ))}
          {sources.length === 0 && <p className="text-slate-500 text-sm">No sources configured.</p>}
        </div>

        <Card>
          <CardHeader><CardTitle>Latest Data</CardTitle></CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Title</TableHead>
                  <TableHead>Department</TableHead>
                  <TableHead>Last Date</TableHead>
                  <TableHead>Vacancies</TableHead>
                  <TableHead>Qualification</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {changes.slice(0, 20).map((c: any) => {
                  const item = c.after || c.before;
                  return (
                    <TableRow key={c.id}>
                      <TableCell className="font-medium">{item?.title}</TableCell>
                      <TableCell>{item?.department}</TableCell>
                      <TableCell>{item?.last_application_date}</TableCell>
                      <TableCell>{item?.number_of_vacancies}</TableCell>
                      <TableCell>{item?.qualification_required}</TableCell>
                    </TableRow>
                  );
                })}
                {changes.length === 0 && <TableRow><TableCell colSpan={5} className="text-slate-500">No data yet.</TableCell></TableRow>}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
