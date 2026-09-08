import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import {
  FamilyIcon,
  HistoryIcon,
  HomeIcon,
  SensorIcon,
  SettingsIcon,
} from "./icons";

const navItems = [
  { to: "/", label: "Inicio", icon: HomeIcon, end: true },
  { to: "/historial", label: "Historial", icon: HistoryIcon, end: false },
  { to: "/sensores", label: "Sensores", icon: SensorIcon, end: false },
  { to: "/familia", label: "Familia", icon: FamilyIcon, end: false },
  { to: "/ajustes", label: "Ajustes", icon: SettingsIcon, end: false },
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-[#f4f6fb] flex justify-center">
      <div className="w-full max-w-md min-h-screen bg-[#f4f6fb] flex flex-col relative shadow-xl">
        <main className="flex-1 overflow-y-auto pb-24">{children}</main>
        <nav className="fixed bottom-0 w-full max-w-md bg-white border-t border-slate-200 pb-[env(safe-area-inset-bottom)]">
          <ul className="flex items-stretch justify-between px-2">
            {navItems.map(({ to, label, icon: Icon, end }) => (
              <li key={to} className="flex-1">
                <NavLink
                  to={to}
                  end={end}
                  className={({ isActive }) =>
                    `flex flex-col items-center gap-1 py-2.5 text-xs font-medium transition-colors ${
                      isActive ? "text-brand-600" : "text-slate-400"
                    }`
                  }
                >
                  {({ isActive }) => (
                    <>
                      <Icon
                        className="w-6 h-6"
                        strokeWidth={isActive ? 2.4 : 2}
                      />
                      <span>{label}</span>
                    </>
                  )}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </div>
  );
}

export function ScreenHeader({
  title,
  subtitle,
  right,
}: {
  title: string;
  subtitle?: string;
  right?: ReactNode;
}) {
  return (
    <header className="px-5 pt-6 pb-4 flex items-start justify-between gap-3">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">{title}</h1>
        {subtitle && <p className="text-sm text-slate-500 mt-0.5">{subtitle}</p>}
      </div>
      {right}
    </header>
  );
}
