import type { ReactNode } from "react";
import { useAppStore } from "../store/AppStore";
import { ScreenHeader } from "../components/AppShell";
import { MoonIcon } from "../components/icons";
import type { FamilySettings } from "../types";

function Toggle({ checked, onChange }: { checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <button
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={`w-11 h-6 rounded-full relative transition-colors shrink-0 ${
        checked ? "bg-brand-600" : "bg-slate-200"
      }`}
    >
      <span
        className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform ${
          checked ? "translate-x-5" : "translate-x-0.5"
        }`}
      />
    </button>
  );
}

function SectionTitle({ children }: { children: string }) {
  return (
    <h2 className="px-5 mt-6 mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
      {children}
    </h2>
  );
}

function Row({
  title,
  subtitle,
  right,
}: {
  title: string;
  subtitle?: string;
  right: ReactNode;
}) {
  return (
    <div className="bg-white px-4 py-3.5 flex items-center gap-3 border-b border-slate-100 last:border-0 last:rounded-b-2xl first:rounded-t-2xl">
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-slate-900">{title}</p>
        {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
      </div>
      {right}
    </div>
  );
}

const sensitivityOptions: { value: FamilySettings["sensitivity"]; label: string }[] = [
  { value: "baja", label: "Baja" },
  { value: "media", label: "Media" },
  { value: "alta", label: "Alta" },
];

export function SettingsPage() {
  const { state, updateSettings } = useAppStore();
  const { settings } = state;

  return (
    <div>
      <ScreenHeader title="Ajustes" subtitle="Notificaciones, sensibilidad y cuenta" />

      <SectionTitle>Sensibilidad de detección</SectionTitle>
      <div className="px-5">
        <div className="bg-white rounded-2xl border border-slate-100 p-1.5 flex gap-1">
          {sensitivityOptions.map((opt) => (
            <button
              key={opt.value}
              onClick={() => updateSettings({ sensitivity: opt.value })}
              className={`flex-1 py-2 rounded-xl text-sm font-medium transition-colors ${
                settings.sensitivity === opt.value
                  ? "bg-brand-600 text-white"
                  : "text-slate-500"
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
        <p className="text-xs text-slate-400 mt-2 px-1">
          Más alta detecta más rápido, pero puede dar más falsas alarmas.
        </p>
      </div>

      <SectionTitle>Notificaciones de alerta</SectionTitle>
      <div className="px-5">
        <div className="rounded-2xl overflow-hidden">
          <Row
            title="Notificación push"
            subtitle="Aviso inmediato en el móvil"
            right={
              <Toggle
                checked={settings.notifyPush}
                onChange={(v) => updateSettings({ notifyPush: v })}
              />
            }
          />
          <Row
            title="SMS"
            subtitle="Por si no hay internet"
            right={
              <Toggle
                checked={settings.notifySms}
                onChange={(v) => updateSettings({ notifySms: v })}
              />
            }
          />
          <Row
            title="Llamada automática"
            subtitle="Si nadie confirma a tiempo"
            right={
              <Toggle
                checked={settings.notifyCall}
                onChange={(v) => updateSettings({ notifyCall: v })}
              />
            }
          />
        </div>
      </div>

      <SectionTitle>Tiempo antes de escalar</SectionTitle>
      <div className="px-5">
        <div className="bg-white rounded-2xl border border-slate-100 p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-slate-600">Esperar respuesta</span>
            <span className="text-sm font-semibold text-brand-600">
              {settings.escalationTimeoutSeconds}s
            </span>
          </div>
          <input
            type="range"
            min={20}
            max={120}
            step={10}
            value={settings.escalationTimeoutSeconds}
            onChange={(e) =>
              updateSettings({ escalationTimeoutSeconds: Number(e.target.value) })
            }
            className="w-full accent-brand-600"
          />
        </div>
      </div>

      <SectionTitle>General</SectionTitle>
      <div className="px-5 pb-4">
        <div className="rounded-2xl overflow-hidden">
          <Row
            title="No molestar"
            subtitle={
              settings.doNotDisturbUntil
                ? "Activado temporalmente"
                : "Las alertas siempre se notifican"
            }
            right={
              <div className="flex items-center gap-2">
                <MoonIcon className="w-4 h-4 text-slate-400" />
                <Toggle
                  checked={!!settings.doNotDisturbUntil}
                  onChange={(v) =>
                    updateSettings({
                      doNotDisturbUntil: v ? new Date(Date.now() + 3600_000).toISOString() : null,
                    })
                  }
                />
              </div>
            }
          />
          <Row title="Familia" subtitle={state.familyName} right={null} />
          <Row title="Casa" subtitle={state.houseName} right={null} />
        </div>
      </div>
    </div>
  );
}
