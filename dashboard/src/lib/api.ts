const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "https://bharatwatch-api.onrender.com";

export interface ModuleInfo {
  id: string;
  label: string;
  tagline: string;
  icon: string;
  accent: string;
  source_name: string;
  collector_id: string | null;
  health: string;
  item_count: number;
  changes_7d: number;
  last_run_at: string | null;
}

export interface ModuleStats {
  id: string;
  label: string;
  icon: string;
  accent: string;
  health: string;
  item_count: number;
  changes_7d: number;
  sparkline: { t: string; v: number }[];
  collector_id: string;
  last_run_at: string | null;
}

export interface Overview {
  sources: number;
  healthy: number;
  total_items: number;
  total_changes_7d: number;
  heal_events: number;
  heal_success: number;
  activity_series: { date: string; changes: number }[];
  modules: ModuleStats[];
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`API ${path} -> ${res.status}`);
  return res.json();
}

export const fetchHealth = () => get<{ status: string; sources: number; healthy: number }>("/api/v1/health");
export const fetchModules = () => get<{ modules: ModuleInfo[] }>("/api/v1/modules");
export const fetchOverview = () => get<Overview>("/api/v1/overview");
export const fetchSources = (module: string) =>
  get<{ id: number; name: string; url: string; health: string; collector_id: string; last_run_at: string | null }[]>(
    `/api/v1/${module}/sources`
  );
export const fetchChanges = (module: string) =>
  get<{ id: number; change_type: string; before: unknown; after: unknown; detected_at: string }[]>(
    `/api/v1/${module}/changes`
  );
export const fetchModuleData = (module: string) =>
  get<{
    module: string;
    meta: { label: string; tagline: string; icon: string; accent: string; source_name: string };
    source: { name: string; url: string; collector_id: string; health: string; last_run_at: string | null };
    items: Record<string, unknown>[];
    captured_at: string | null;
  }>(`/api/v1/${module}/data`);
export const fetchModuleHistory = (module: string) =>
  get<{
    history: { t: string; items: number; status: string }[];
    changes: { id: number; change_type: string; before: unknown; after: unknown; detected_at: string }[];
  }>(`/api/v1/${module}/history`);
export const fetchHealEvents = () =>
  get<{ id: number; source_id: number; module: string; module_label: string; icon: string; description: string; success: string; created_at: string }[]>(
    "/api/v1/heal-events"
  );
