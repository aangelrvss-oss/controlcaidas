import { useMemo, useState } from "react";
import { useAppStore } from "../store/AppStore";
import { ScreenHeader } from "../components/AppShell";
import { RoomIconGlyph } from "../lib/roomIcon";
import { formatDateTime } from "../lib/format";
import { eventStatusMeta } from "../lib/eventStatus";

export function HistoryPage() {
  const { state } = useAppStore();
  const [roomFilter, setRoomFilter] = useState<string>("all");

  const sorted = useMemo(
    () =>
      [...state.events]
        .filter((e) => roomFilter === "all" || e.roomId === roomFilter)
        .sort((a, b) => new Date(b.detectedAt).getTime() - new Date(a.detectedAt).getTime()),
    [state.events, roomFilter]
  );

  return (
    <div>
      <ScreenHeader title="Historial" subtitle="Todos los eventos detectados en la casa" />

      <div className="px-5 mb-3">
        <select
          value={roomFilter}
          onChange={(e) => setRoomFilter(e.target.value)}
          className="w-full bg-white border border-slate-200 rounded-xl px-3 py-2.5 text-sm text-slate-700"
        >
          <option value="all">Todas las habitaciones</option>
          {state.rooms.map((r) => (
            <option key={r.id} value={r.id}>
              {r.name}
            </option>
          ))}
        </select>
      </div>

      {sorted.length === 0 ? (
        <p className="px-5 text-sm text-slate-500">No hay eventos para mostrar.</p>
      ) : (
        <ul className="px-5 space-y-3">
          {sorted.map((event) => {
            const room = state.rooms.find((r) => r.id === event.roomId);
            const meta = eventStatusMeta[event.status];
            const resolvedBy = event.resolvedBy
              ? state.members.find((m) => m.id === event.resolvedBy)
              : null;
            return (
              <li
                key={event.id}
                className="bg-white rounded-2xl p-4 shadow-sm border border-slate-100"
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-500 shrink-0">
                    {room && <RoomIconGlyph icon={room.icon} className="w-5 h-5" />}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-2">
                      <p className="font-medium text-slate-900">{room?.name ?? "Habitación"}</p>
                      <span
                        className={`text-[11px] font-semibold px-2 py-0.5 rounded-full shrink-0 ${meta.badgeClass}`}
                      >
                        {meta.label}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-1">{formatDateTime(event.detectedAt)}</p>
                    {resolvedBy && (
                      <p className="text-xs text-slate-400 mt-1">Resuelto por {resolvedBy.name}</p>
                    )}
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
