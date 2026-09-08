import { useState } from "react";
import { useAppStore } from "../store/AppStore";
import { AlertTriangleIcon, XIcon } from "./icons";

export function DevSimulateButton() {
  const { state, simulateFall, activeAlert } = useAppStore();
  const [open, setOpen] = useState(false);

  if (activeAlert) return null;

  return (
    <div className="fixed bottom-24 right-4 z-40">
      {open && (
        <div className="mb-2 bg-white rounded-2xl shadow-lg border border-slate-200 p-3 w-56">
          <p className="text-xs font-semibold text-slate-500 mb-2 px-1">
            Modo demo · simular caída
          </p>
          <ul className="space-y-1">
            {state.rooms.map((room) => (
              <li key={room.id}>
                <button
                  onClick={() => {
                    simulateFall(room.id);
                    setOpen(false);
                  }}
                  className="w-full text-left text-sm px-2 py-1.5 rounded-lg hover:bg-slate-50 text-slate-700"
                >
                  {room.name}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
      <button
        onClick={() => setOpen((o) => !o)}
        aria-label="Simular caída (solo demo)"
        className="w-12 h-12 rounded-full bg-slate-900 text-white shadow-lg flex items-center justify-center active:scale-95 transition-transform"
      >
        {open ? <XIcon className="w-5 h-5" /> : <AlertTriangleIcon className="w-5 h-5" />}
      </button>
    </div>
  );
}
