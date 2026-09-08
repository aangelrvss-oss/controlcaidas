import { useState } from "react";
import { useAppStore } from "../store/AppStore";
import { ScreenHeader } from "../components/AppShell";
import { Modal } from "../components/Modal";
import { RoomIconGlyph } from "../lib/roomIcon";
import { relativeTime } from "../lib/format";
import { BatteryIcon, PlusIcon, WifiIcon, WifiOffIcon } from "../components/icons";

export function SensorsPage() {
  const { state, toggleSensor, pairNewSensor } = useAppStore();
  const [showAdd, setShowAdd] = useState(false);
  const [step, setStep] = useState<"form" | "searching" | "found">("form");
  const [roomName, setRoomName] = useState("");

  const startPairing = () => {
    if (!roomName.trim()) return;
    setStep("searching");
    setTimeout(() => setStep("found"), 1800);
  };

  const finishPairing = () => {
    pairNewSensor(roomName.trim());
    setShowAdd(false);
    setStep("form");
    setRoomName("");
  };

  return (
    <div>
      <ScreenHeader
        title="Sensores"
        subtitle={`${state.sensors.length} dispositivos ESP32 + LD2450`}
        right={
          <button
            onClick={() => setShowAdd(true)}
            className="w-10 h-10 rounded-full bg-brand-600 text-white flex items-center justify-center shrink-0"
            aria-label="Añadir sensor"
          >
            <PlusIcon className="w-5 h-5" />
          </button>
        }
      />

      <ul className="px-5 space-y-3">
        {state.sensors.map((sensor) => {
          const room = state.rooms.find((r) => r.id === sensor.roomId);
          const isOnline = sensor.status === "online";
          return (
            <li
              key={sensor.id}
              className="bg-white rounded-2xl p-4 shadow-sm border border-slate-100"
            >
              <div className="flex items-start gap-3">
                <div
                  className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 ${
                    isOnline ? "bg-brand-50 text-brand-600" : "bg-slate-100 text-slate-400"
                  }`}
                >
                  {room && <RoomIconGlyph icon={room.icon} className="w-6 h-6" />}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <p className="font-medium text-slate-900 truncate">{sensor.name}</p>
                    <span
                      className={`text-[11px] font-semibold px-2 py-0.5 rounded-full shrink-0 flex items-center gap-1 ${
                        isOnline ? "bg-safe-100 text-safe-700" : "bg-warn-50 text-warn-600"
                      }`}
                    >
                      {isOnline ? <WifiIcon className="w-3 h-3" /> : <WifiOffIcon className="w-3 h-3" />}
                      {isOnline ? "En línea" : "Sin conexión"}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">{room?.name ?? "Sin habitación"}</p>
                  <div className="flex items-center gap-3 mt-2 text-[11px] text-slate-400">
                    <span>Firmware {sensor.firmware}</span>
                    <span>Visto {relativeTime(sensor.lastSeen)}</span>
                    {sensor.battery != null && (
                      <span className="flex items-center gap-0.5">
                        <BatteryIcon className="w-3.5 h-3.5" />
                        {sensor.battery}%
                      </span>
                    )}
                  </div>
                </div>
              </div>
              <button
                onClick={() => toggleSensor(sensor.id)}
                className="mt-3 text-xs font-medium text-slate-400 underline decoration-dotted"
              >
                Simular {isOnline ? "desconexión" : "reconexión"} (demo)
              </button>
            </li>
          );
        })}
      </ul>

      {showAdd && (
        <Modal
          title="Añadir sensor"
          onClose={() => {
            setShowAdd(false);
            setStep("form");
          }}
        >
          {step === "form" && (
            <div className="space-y-4">
              <p className="text-sm text-slate-500">
                Enciende el ESP32 con el sensor LD2450 cerca del router y ponlo en modo
                emparejamiento. Luego indica en qué habitación lo vas a instalar.
              </p>
              <div>
                <label className="text-sm font-medium text-slate-700">Habitación</label>
                <input
                  value={roomName}
                  onChange={(e) => setRoomName(e.target.value)}
                  placeholder="Ej. Estudio, Entrada..."
                  className="w-full mt-1 border border-slate-200 rounded-xl px-3 py-2.5 text-sm"
                />
              </div>
              <button
                onClick={startPairing}
                disabled={!roomName.trim()}
                className="w-full bg-brand-600 disabled:bg-slate-200 disabled:text-slate-400 text-white font-semibold rounded-xl py-3"
              >
                Buscar dispositivo
              </button>
            </div>
          )}

          {step === "searching" && (
            <div className="flex flex-col items-center py-6 text-center">
              <div className="w-12 h-12 rounded-full border-4 border-brand-100 border-t-brand-600 animate-spin mb-4" />
              <p className="text-sm text-slate-600">Buscando sensor ESP32 + LD2450…</p>
            </div>
          )}

          {step === "found" && (
            <div className="text-center py-2">
              <div className="w-14 h-14 mx-auto rounded-full bg-safe-100 text-safe-600 flex items-center justify-center mb-3">
                <WifiIcon className="w-7 h-7" />
              </div>
              <p className="font-medium text-slate-900">Sensor encontrado</p>
              <p className="text-sm text-slate-500 mt-1">
                Se asignará a la habitación “{roomName}”.
              </p>
              <button
                onClick={finishPairing}
                className="w-full mt-4 bg-brand-600 text-white font-semibold rounded-xl py-3"
              >
                Confirmar instalación
              </button>
            </div>
          )}
        </Modal>
      )}
    </div>
  );
}
