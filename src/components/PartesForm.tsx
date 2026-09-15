import { useState } from "react";
import { insurers } from "../data/insurers";
import { serviceOptions } from "../data/services";
import { buildWhatsappUrl } from "../data/contact";

const STEP_LABELS = ["Aseguradora", "Servicio", "Vehículo"];

export function PartesForm() {
  const [step, setStep] = useState(1);
  const [aseguradora, setAseguradora] = useState<string | null>(null);
  const [servicio, setServicio] = useState<string | null>(null);
  const [vehiculo, setVehiculo] = useState("");
  const [contactoInfo, setContactoInfo] = useState("");

  const canGoStep2 = Boolean(aseguradora);
  const canGoStep3 = Boolean(servicio);
  const canSubmit = vehiculo.trim().length > 1 || contactoInfo.trim().length > 1;

  const vehiculoTexto = [vehiculo, contactoInfo].filter(Boolean).join(" · Contacto: ");

  const whatsappUrl = buildWhatsappUrl({
    aseguradora: aseguradora ?? undefined,
    servicio: servicio ?? undefined,
    vehiculo: vehiculoTexto || undefined,
  });

  return (
    <section id="parte" className="relative bg-titanium-900 px-6 py-28 sm:px-10">
      <div className="mx-auto max-w-3xl">
        <p className="font-kinetic text-center text-xs uppercase tracking-[0.35em] text-cyan-400">
          Gestión de partes y citas
        </p>
        <h2 className="font-kinetic mt-2 text-center text-3xl font-bold uppercase text-white sm:text-5xl">
          Tramita tu parte en 3 pasos
        </h2>

        <div className="mt-10 flex items-center justify-center gap-2 sm:gap-4">
          {STEP_LABELS.map((label, i) => {
            const n = i + 1;
            const active = step === n;
            const done = step > n;
            return (
              <div key={label} className="flex items-center gap-2 sm:gap-4">
                <div className="flex flex-col items-center gap-1">
                  <span
                    className={`flex h-9 w-9 items-center justify-center rounded-full font-kinetic text-sm font-bold transition ${
                      done
                        ? "bg-cyan-500 text-titanium-950"
                        : active
                          ? "border-2 border-cyan-400 text-cyan-400"
                          : "border border-white/20 text-white/40"
                    }`}
                  >
                    {done ? "✓" : n}
                  </span>
                  <span className="font-kinetic hidden text-[11px] uppercase tracking-widest text-white/50 sm:block">
                    {label}
                  </span>
                </div>
                {n < STEP_LABELS.length && <span className="h-px w-8 bg-white/15 sm:w-16" />}
              </div>
            );
          })}
        </div>

        <div className="mt-12 rounded-2xl border border-white/10 bg-titanium-800/60 p-6 shadow-[0_0_60px_-25px_rgba(0,180,216,0.5)] sm:p-10">
          {step === 1 && (
            <div>
              <h3 className="font-kinetic text-xl font-bold uppercase text-white">
                Selecciona tu compañía de seguros
              </h3>
              <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
                {insurers.map((insurer) => (
                  <button
                    key={insurer.id}
                    type="button"
                    onClick={() => setAseguradora(insurer.name)}
                    className={`rounded-xl border px-4 py-5 font-kinetic text-sm font-semibold uppercase tracking-wide transition ${
                      aseguradora === insurer.name
                        ? "border-cyan-400 bg-cyan-500/15 text-cyan-300"
                        : "border-white/10 bg-titanium-900/60 text-white/80 hover:border-cyan-500/40"
                    }`}
                  >
                    {insurer.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 2 && (
            <div>
              <h3 className="font-kinetic text-xl font-bold uppercase text-white">
                Tipo de daño o servicio
              </h3>
              <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
                {serviceOptions.map((service) => (
                  <button
                    key={service.id}
                    type="button"
                    onClick={() => setServicio(service.name)}
                    className={`rounded-xl border px-5 py-4 text-left transition ${
                      servicio === service.name
                        ? "border-cyan-400 bg-cyan-500/15"
                        : "border-white/10 bg-titanium-900/60 hover:border-cyan-500/40"
                    }`}
                  >
                    <span className="font-kinetic block text-sm font-semibold uppercase tracking-wide text-white">
                      {service.name}
                    </span>
                    <span className="mt-1 block text-xs text-white/50">{service.description}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <h3 className="font-kinetic text-xl font-bold uppercase text-white">Datos del vehículo</h3>
              <div className="mt-6 flex flex-col gap-4">
                <label className="flex flex-col gap-2">
                  <span className="font-kinetic text-xs uppercase tracking-widest text-white/50">
                    Marca / Modelo y Matrícula
                  </span>
                  <input
                    value={vehiculo}
                    onChange={(e) => setVehiculo(e.target.value)}
                    placeholder="Ej: Seat León 1234-ABC"
                    className="rounded-lg border border-white/15 bg-titanium-900/70 px-4 py-3 text-white placeholder:text-white/30 outline-none focus:border-cyan-400"
                  />
                </label>
                <label className="flex flex-col gap-2">
                  <span className="font-kinetic text-xs uppercase tracking-widest text-white/50">
                    Teléfono de contacto (opcional)
                  </span>
                  <input
                    value={contactoInfo}
                    onChange={(e) => setContactoInfo(e.target.value)}
                    placeholder="Ej: 600 000 000"
                    className="rounded-lg border border-white/15 bg-titanium-900/70 px-4 py-3 text-white placeholder:text-white/30 outline-none focus:border-cyan-400"
                  />
                </label>
              </div>
            </div>
          )}

          <div className="mt-8 flex items-center justify-between gap-4">
            <button
              type="button"
              onClick={() => setStep((s) => Math.max(1, s - 1))}
              className={`font-kinetic text-sm uppercase tracking-widest text-white/50 transition hover:text-white ${
                step === 1 ? "pointer-events-none opacity-0" : ""
              }`}
            >
              ← Atrás
            </button>

            {step < 3 ? (
              <button
                type="button"
                disabled={step === 1 ? !canGoStep2 : !canGoStep3}
                onClick={() => setStep((s) => s + 1)}
                className="rounded-full bg-cyan-500 px-8 py-3 font-kinetic text-sm font-bold uppercase tracking-wide text-titanium-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:bg-white/10 disabled:text-white/30"
              >
                Siguiente →
              </button>
            ) : (
              <a
                href={canSubmit ? whatsappUrl : undefined}
                target="_blank"
                rel="noreferrer"
                aria-disabled={!canSubmit}
                onClick={(e) => {
                  if (!canSubmit) e.preventDefault();
                }}
                className={`animate-neon-pulse flex items-center gap-2 rounded-full px-8 py-3 font-kinetic text-sm font-bold uppercase tracking-wide transition ${
                  canSubmit
                    ? "bg-cyan-500 text-titanium-950 hover:bg-cyan-400"
                    : "cursor-not-allowed bg-white/10 text-white/30"
                }`}
              >
                Tramitar Parte por WhatsApp
              </a>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
