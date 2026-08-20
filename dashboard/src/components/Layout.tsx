import ModuleNav from "./ModuleNav";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50 flex">
      <aside className="w-64 bg-white border-r border-slate-200 p-6 hidden md:block">
        <div className="mb-6">
          <h1 className="text-xl font-bold text-slate-900">BharatWatch</h1>
          <p className="text-xs text-slate-500">Self-Healing Local Intelligence</p>
        </div>
        <ModuleNav />
      </aside>
      <main className="flex-1 p-6 overflow-auto">{children}</main>
    </div>
  );
}
