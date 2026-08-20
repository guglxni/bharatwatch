const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/api/v1/health`);
  return res.json();
}

export async function fetchModules() {
  const res = await fetch(`${API_BASE}/api/v1/modules`);
  return res.json();
}

export async function fetchSources(module: string) {
  const res = await fetch(`${API_BASE}/api/v1/${module}/sources`);
  return res.json();
}

export async function fetchChanges(module: string) {
  const res = await fetch(`${API_BASE}/api/v1/${module}/changes`);
  return res.json();
}

export async function fetchHealEvents() {
  const res = await fetch(`${API_BASE}/api/v1/heal-events`);
  return res.json();
}
