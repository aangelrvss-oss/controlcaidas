import type { EventStatus } from "../types";

export const eventStatusMeta: Record<
  EventStatus,
  { label: string; badgeClass: string; dotClass: string }
> = {
  active: {
    label: "Alerta activa",
    badgeClass: "bg-danger-50 text-danger-700",
    dotClass: "bg-danger-600",
  },
  escalated: {
    label: "Escalada",
    badgeClass: "bg-danger-50 text-danger-700",
    dotClass: "bg-danger-600",
  },
  confirmed_fall: {
    label: "Caída confirmada",
    badgeClass: "bg-danger-50 text-danger-700",
    dotClass: "bg-danger-600",
  },
  confirmed_ok: {
    label: "Confirmado: está bien",
    badgeClass: "bg-safe-100 text-safe-700",
    dotClass: "bg-safe-600",
  },
  false_alarm: {
    label: "Falsa alarma",
    badgeClass: "bg-slate-100 text-slate-600",
    dotClass: "bg-slate-400",
  },
};
