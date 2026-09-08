import { useAppStore } from "../store/AppStore";
import { RoomIconGlyph } from "../lib/roomIcon";
import { relativeTime } from "../lib/format";
import { ShieldIcon, WifiIcon, WifiOffIcon, BatteryIcon } from "../components/icons";
import { Link } from "react-router-dom";

export function HomePage() {
  const { state } = useAppStore();
  const { rooms, sensors, members, houseName, familyName } = state;

  const offlineSensors = sensors.filter((s) => s.status === "offline");
  const allOk = offlineSensors.length === 0;

  return (
    <div>
      <div className="px-5 pt-6 pb-2 flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">{familyName}</p>
          <h1 className="text-2xl font-semibold text-slate-900">{houseName}</h1>
        </div>
        <div className="flex -space-x-2">
          {members.slice(0, 4).map((m) => (
            <div
              key={m.id}
              title={m.name}
              className="w-9 h-9 rounded-full ring-2 ring-white flex items-center justify-center text-white text-xs font-semibold"
              style={{ backgroundColor: m.avatarColor }}
            >
              {m.name
                .split(" ")
                .map((p) => p[0])
                .slice(0, 2)
                .join("")
                .toUpperCase()}
            </div>
          ))}
        </div>
      </div>

      <div className="px-5 mt-4">
        <div
          className={`rounded-3xl p-5 flex items-center gap-4 ${
            allOk ? "bg-safe-600" : "bg-warn-500"
          }`}
        >
          <div className="w-14 h-14 rounded-full bg-white/20 flex items-center justify-center shrink-0">
            <ShieldIcon className="w-7 h-7 text-white" />
          </div>
          <div className="min-w-0">
            <p className="text-white font-semibold text-lg leading-tight">
              {allOk ? "Todo en orden" : "Revisa los sensores"}
            </p>
            <p className="text-white/85 text-sm mt-0.5">
              {allOk
                ? "Todos los sensores están activos y monitoreando"
                : `${offlineSensors.length} sensor${offlineSensors.length > 1 ? "es" : ""} sin conexión`}
            </p>
          </div>
        </div>
      </div>

      <div className="px-5 mt-6 flex items-center justify-between">
        <h2 className="text-base font-semibold text-slate-900">Habitaciones</h2>
        <Link to="/sensores" className="text-sm font-medium text-brand-600">
          Gestionar
        </Link>
      </div>

      <ul className="px-5 mt-3 space-y-3">
        {rooms.map((room) => {
          const sensor = sensors.find((s) => s.roomId === room.id);
          const isOnline = sensor?.status === "online";
          return (
            <li
              key={room.id}
              className="bg-white rounded-2xl p-4 flex items-center gap-4 shadow-sm border border-slate-100"
            >
              <div
                className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 ${
                  isOnline ? "bg-brand-50 text-brand-600" : "bg-slate-100 text-slate-400"
                }`}
              >
                <RoomIconGlyph icon={room.icon} className="w-6 h-6" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="font-medium text-slate-900">{room.name}</p>
                <p className="text-xs text-slate-500 mt-0.5">
                  {sensor
                    ? isOnline
                      ? `Activo · actualizado ${relativeTime(sensor.lastSeen)}`
                      : `Sin conexión · desde ${relativeTime(sensor.lastSeen)}`
                    : "Sin sensor asignado"}
                </p>
              </div>
              <div className="flex flex-col items-end gap-1 shrink-0">
                {isOnline ? (
                  <WifiIcon className="w-4 h-4 text-safe-600" />
                ) : (
                  <WifiOffIcon className="w-4 h-4 text-warn-500" />
                )}
                {sensor?.battery != null && (
                  <span className="flex items-center gap-0.5 text-[11px] text-slate-400">
                    <BatteryIcon className="w-3.5 h-3.5" />
                    {sensor.battery}%
                  </span>
                )}
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
