import { useState } from "react";
import { useAppStore } from "../store/AppStore";
import { ScreenHeader } from "../components/AppShell";
import { Modal } from "../components/Modal";
import { PhoneIcon, PlusIcon, XIcon } from "../components/icons";

function initials(name: string) {
  return name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

export function FamilyPage() {
  const { state, addMember, removeMember } = useAppStore();
  const [showAdd, setShowAdd] = useState(false);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");

  const escalation = [...state.members]
    .filter((m) => m.isEmergencyContact && m.escalationOrder)
    .sort((a, b) => (a.escalationOrder ?? 99) - (b.escalationOrder ?? 99));

  const submit = () => {
    if (!name.trim() || !phone.trim()) return;
    addMember(name.trim(), phone.trim());
    setShowAdd(false);
    setName("");
    setPhone("");
  };

  return (
    <div>
      <ScreenHeader
        title="Familia"
        subtitle="Quién cuida, y en qué orden se avisa"
        right={
          <button
            onClick={() => setShowAdd(true)}
            className="w-10 h-10 rounded-full bg-brand-600 text-white flex items-center justify-center shrink-0"
            aria-label="Invitar miembro"
          >
            <PlusIcon className="w-5 h-5" />
          </button>
        }
      />

      <ul className="px-5 space-y-3">
        {state.members.map((m) => (
          <li
            key={m.id}
            className="bg-white rounded-2xl p-4 shadow-sm border border-slate-100 flex items-center gap-3"
          >
            <div
              className="w-11 h-11 rounded-full flex items-center justify-center text-white font-semibold shrink-0"
              style={{ backgroundColor: m.avatarColor }}
            >
              {initials(m.name)}
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2">
                <p className="font-medium text-slate-900">{m.name}</p>
                {m.role === "admin" && (
                  <span className="text-[10px] font-semibold bg-brand-50 text-brand-600 px-1.5 py-0.5 rounded-full">
                    ADMIN
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                <PhoneIcon className="w-3 h-3" />
                {m.phone}
              </p>
            </div>
            {!m.isYou && (
              <button
                onClick={() => removeMember(m.id)}
                className="w-8 h-8 rounded-full text-slate-300 hover:text-slate-500 flex items-center justify-center shrink-0"
                aria-label={`Quitar a ${m.name}`}
              >
                <XIcon className="w-4 h-4" />
              </button>
            )}
          </li>
        ))}
      </ul>

      <h2 className="px-5 mt-6 mb-3 text-base font-semibold text-slate-900">
        Orden de aviso en una alerta
      </h2>
      <ol className="px-5 space-y-2">
        {escalation.map((m, i) => (
          <li
            key={m.id}
            className="bg-white rounded-xl px-4 py-3 flex items-center gap-3 border border-slate-100"
          >
            <span className="w-6 h-6 rounded-full bg-brand-600 text-white text-xs font-bold flex items-center justify-center shrink-0">
              {i + 1}
            </span>
            <span className="text-sm text-slate-700">{m.name}</span>
          </li>
        ))}
      </ol>

      {showAdd && (
        <Modal title="Invitar a la familia" onClose={() => setShowAdd(false)}>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-slate-700">Nombre</label>
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Ej. Pedro Rivas"
                className="w-full mt-1 border border-slate-200 rounded-xl px-3 py-2.5 text-sm"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700">Teléfono</label>
              <input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+34 600 000 000"
                className="w-full mt-1 border border-slate-200 rounded-xl px-3 py-2.5 text-sm"
              />
            </div>
            <p className="text-xs text-slate-400">
              Se enviará una invitación por SMS para que descargue la app y se una al círculo
              familiar.
            </p>
            <button
              onClick={submit}
              disabled={!name.trim() || !phone.trim()}
              className="w-full bg-brand-600 disabled:bg-slate-200 disabled:text-slate-400 text-white font-semibold rounded-xl py-3"
            >
              Enviar invitación
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}
