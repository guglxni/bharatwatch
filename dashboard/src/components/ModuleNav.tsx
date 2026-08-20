"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const modules = [
  { id: "nauktrialert", label: "NaukriAlert", icon: "🔔" },
  { id: "tendersentry", label: "TenderSentry", icon: "📄" },
  { id: "collegecutoff", label: "CollegeCutoff", icon: "🎓" },
  { id: "startuppulse", label: "StartupPulse", icon: "🚀" },
  { id: "mandiwatch", label: "MandiWatch", icon: "🌾" },
];

export default function ModuleNav() {
  const pathname = usePathname();
  return (
    <nav className="space-y-1">
      <Link href="/" className={cn(
        "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium",
        pathname === "/" ? "bg-slate-900 text-white" : "text-slate-600 hover:bg-slate-100"
      )}>
        <span>🏠</span> Overview
      </Link>
      {modules.map((m) => (
        <Link key={m.id} href={`/modules/${m.id}`} className={cn(
          "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium",
          pathname.startsWith(`/modules/${m.id}`) ? "bg-slate-900 text-white" : "text-slate-600 hover:bg-slate-100"
        )}>
          <span>{m.icon}</span> {m.label}
        </Link>
      ))}
      <Link href="/heal-log" className={cn(
        "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium",
        pathname === "/heal-log" ? "bg-slate-900 text-white" : "text-slate-600 hover:bg-slate-100"
      )}>
        <span>🩹</span> Heal Log
      </Link>
    </nav>
  );
}
