"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const MODULES = [
  { id: "nauktrialert", label: "NaukriAlert", icon: "🔔" },
  { id: "tendersentry", label: "TenderSentry", icon: "📄" },
  { id: "mandiwatch", label: "MandiWatch", icon: "🌾" },
  { id: "collegecutoff", label: "CollegeCutoff", icon: "🎓" },
  { id: "startuppulse", label: "StartupPulse", icon: "🚀" },
];

function NavItem({
  href,
  active,
  icon,
  label,
}: {
  href: string;
  active: boolean;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <Link
      href={href}
      className={cn(
        "group flex items-center gap-3 px-3 py-2 rounded-lg text-[13px] font-medium transition-all duration-150 relative",
        active
          ? "bg-white/[0.06] text-white"
          : "text-muted-foreground hover:text-foreground hover:bg-white/[0.03]"
      )}
    >
      {active && (
        <span className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-4 rounded-full bg-indigo-400" />
      )}
      <span className="text-[15px]">{icon}</span>
      {label}
    </Link>
  );
}

export function ShellNav() {
  const pathname = usePathname();
  return (
    <nav className="space-y-6">
      <div>
        <div className="px-3 mb-2 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground/70">
          Overview
        </div>
        <div className="space-y-0.5">
          <NavItem href="/dashboard" active={pathname === "/dashboard"} icon="📊" label="Mission Control" />
          <NavItem href="/heal-log" active={pathname === "/heal-log"} icon="🩹" label="Self-Heal Log" />
        </div>
      </div>
      <div>
        <div className="px-3 mb-2 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground/70">
          Live Collectors
        </div>
        <div className="space-y-0.5">
          {MODULES.map((m) => (
            <NavItem
              key={m.id}
              href={`/dashboard/${m.id}`}
              active={pathname === `/dashboard/${m.id}`}
              icon={m.icon}
              label={m.label}
            />
          ))}
        </div>
      </div>
      <div>
        <div className="px-3 mb-2 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground/70">
          Project
        </div>
        <div className="space-y-0.5">
          <NavItem href="/" active={pathname === "/"} icon="🏠" label="Landing Page" />
        </div>
      </div>
    </nav>
  );
}
