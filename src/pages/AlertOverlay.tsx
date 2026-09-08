import { useEffect, useState } from "react";
import { useAppStore } from "../store/AppStore";
import { RoomIconGlyph } from "../lib/roomIcon";
import { AlertTriangleIcon, CheckIcon, PhoneIcon } from "../components/icons";
import type { FallEvent } from "../types";

export function AlertOverlay({ event }: { event: FallEvent }) {
  const { state, resolveEvent, escalateEvent } = useAppStore();
  const room = state.rooms.find((r) => r.id === event.roomId);
  const you = state.members.find((m) => m.isYou) ?? state.members[0];
  const nextContact = state.members
    .filter((m) => m.isEmergencyContact && m.escalationOrder && !m.isYou)
    .sort((a, b) => (a.escalationOrder ?? 99) - (b.escalationOrder ?? 99))[0];

  const [remaining, setRemaining] = useState(() => {
    const elapsed = (Date.now() - new Date(event.detectedAt).getTime()) / 1000;
    return Math.max(0, Math.round(state.settings.escalationTimeoutSeconds - elapsed));
  });

  useEffect(() => {
    if (event.status !== "active") return;
    const id = setInterval(() => {
      setRemaining((r) => {
        if (r <= 1) {
          escalateEvent(event.id);
          return 0;
        }
        return r - 1;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [event.id, event.status, escalateEvent]);

  const resolve = (status: FallEvent["status"]) => resolveEvent(event.id, status, you.id);

  return (
    <div className="fixed inset-0 z-50 bg-danger-600 flex flex-col text-white">
      <div className="flex-1 flex flex-col items-center justify-center px-6 text-center">
        <div className="relative mb-6">
          <span className="absolute inset-0 rounded-full bg-white/30 animate-pulse-ring" />
          <div className="relative w-24 h-24 rounded-full bg-white/15 flex items-center justify-center">
            <AlertTriangleIcon className="w-12 h-12 text-white" />
          </div>
        </div>

        <p className="uppercase tracking-wide text-white/80 text-xs font-semibold mb-2">
          {event.confidence === "alta" ? "Confianza alta" : "Confianza media"}
        </p>
        <h1 className="text-2xl font-bold leading-tight">Posible caída detectada</h1>
        <p className="text-white/90 mt-2 flex items-center gap-1.5 justify-center">
          {room && <RoomIconGlyph icon={room.icon} className="w-4 h-4" />}
          {room?.name ?? "Habitación desconocida"}
        </p>

        <div className="mt-6 bg-white/10 rounded-2xl px-5 py-3">
          {event.status === "active" ? (
            <p className="text-sm text-white/90">
              Si nadie responde en <span className="font-bold">{remaining}s</span>, llamaremos a{" "}
              <span className="font-semibold">{nextContact?.name ?? "el siguiente contacto"}</span>
            </p>
          ) : (
            <p className="text-sm text-white/90 font-medium">
              Sin respuesta a tiempo. Llamando a{" "}
              <span className="font-semibold">{nextContact?.name ?? "el siguiente contacto"}</span>…
            </p>
          )}
        </div>
      </div>

      <div className="px-5 pb-8 pt-4 space-y-3">
        <button
          onClick={() => resolve("confirmed_fall")}
          className="w-full bg-white text-danger-700 font-semibold rounded-2xl py-4 flex items-center justify-center gap-2 text-base active:scale-[0.98] transition-transform"
        >
          <PhoneIcon className="w-5 h-5" />
          Es una caída, pedir ayuda
        </button>
        <button
          onClick={() => resolve("confirmed_ok")}
          className="w-full bg-white/15 text-white font-semibold rounded-2xl py-4 flex items-center justify-center gap-2 text-base active:scale-[0.98] transition-transform"
        >
          <CheckIcon className="w-5 h-5" />
          Está bien, confirmar
        </button>
        <button
          onClick={() => resolve("false_alarm")}
          className="w-full text-white/70 font-medium py-2 text-sm"
        >
          Descartar como falsa alarma
        </button>
      </div>
    </div>
  );
}
