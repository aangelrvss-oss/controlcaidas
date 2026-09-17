import { useState } from "react"
import type { FormEvent } from "react"
import { BRAND, FURNITURE_TYPES } from "../lib/content"
import { withSafeEnye } from "../lib/text"

const MAPS_QUERY = encodeURIComponent(BRAND.address)
const MAPS_SEARCH_URL = `https://www.google.com/maps/search/?api=1&query=${MAPS_QUERY}`

export default function Contact() {
  const [furnitureType, setFurnitureType] = useState<string>(FURNITURE_TYPES[0])
  const [name, setName] = useState("")
  const [measurements, setMeasurements] = useState("")
  const [message, setMessage] = useState("")

  const buildWhatsappUrl = () => {
    const lines = [
      `Hola CAYBA, soy ${name || "___"}.`,
      `Quiero presupuesto para: ${furnitureType}.`,
      measurements ? `Medidas aproximadas: ${measurements}.` : null,
      message ? `Detalles: ${message}` : null,
    ].filter(Boolean)
    return `${BRAND.whatsappHref}?text=${encodeURIComponent(lines.join("\n"))}`
  }

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    window.open(buildWhatsappUrl(), "_blank", "noopener,noreferrer")
  }

  return (
    <section id="contacto" className="relative bg-carbon py-28 md:py-40">
      <div className="grid-fresadora absolute inset-0 opacity-40" />
      <div className="absolute inset-0 bg-gradient-to-b from-carbon via-transparent to-carbon" />

      <div className="relative mx-auto max-w-6xl px-6 lg:px-10">
        <div className="mb-16 text-center">
          <p className="font-body text-xs uppercase tracking-[0.3em] text-brand">Presupuesto Express</p>
          <h2 className="font-display mt-2 text-4xl text-white md:text-6xl">
            {withSafeEnye("Diseña tu espacio")}
          </h2>
          <p className="mx-auto mt-4 max-w-xl font-body text-white/60">
            Cuéntanos qué necesitas y te respondemos por WhatsApp o teléfono en el mismo día.
          </p>
        </div>

        <div className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr]">
          <form
            onSubmit={onSubmit}
            className="rounded-3xl border border-line bg-carbon-card/80 p-8 shadow-[0_30px_80px_rgba(0,0,0,0.5)] backdrop-blur-sm md:p-10"
          >
            <div className="grid gap-6 sm:grid-cols-2">
              <label className="flex flex-col gap-2 sm:col-span-2">
                <span className="font-body text-xs uppercase tracking-wider text-white/50">Tipo de mueble</span>
                <select
                  value={furnitureType}
                  onChange={(e) => setFurnitureType(e.target.value)}
                  className="rounded-xl border border-line bg-carbon px-4 py-3 font-body text-white outline-none focus:border-brand"
                >
                  {FURNITURE_TYPES.map((type) => (
                    <option key={type} value={type}>
                      {type}
                    </option>
                  ))}
                </select>
              </label>

              <label className="flex flex-col gap-2">
                <span className="font-body text-xs uppercase tracking-wider text-white/50">Tu nombre</span>
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  type="text"
                  placeholder="Nombre y apellidos"
                  className="rounded-xl border border-line bg-carbon px-4 py-3 font-body text-white outline-none placeholder:text-white/30 focus:border-brand"
                />
              </label>

              <label className="flex flex-col gap-2">
                <span className="font-body text-xs uppercase tracking-wider text-white/50">Medidas aproximadas</span>
                <input
                  value={measurements}
                  onChange={(e) => setMeasurements(e.target.value)}
                  type="text"
                  placeholder='Ej. 2,40m x 2,60m x 0,60m'
                  className="rounded-xl border border-line bg-carbon px-4 py-3 font-body text-white outline-none placeholder:text-white/30 focus:border-brand"
                />
              </label>

              <label className="flex flex-col gap-2 sm:col-span-2">
                <span className="font-body text-xs uppercase tracking-wider text-white/50">Cuéntanos tu proyecto</span>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={4}
                  placeholder="Estilo, acabados, plazos..."
                  className="resize-none rounded-xl border border-line bg-carbon px-4 py-3 font-body text-white outline-none placeholder:text-white/30 focus:border-brand"
                />
              </label>
            </div>

            <div className="mt-8 flex flex-col gap-4 sm:flex-row">
              <button
                type="submit"
                className="flex-1 rounded-full bg-brand px-8 py-4 font-body text-sm font-semibold uppercase tracking-widest text-carbon transition-shadow hover:shadow-[0_0_40px_rgba(232,69,47,0.5)]"
              >
                Enviar por WhatsApp
              </button>
              <a
                href={BRAND.phoneHref}
                className="flex-1 rounded-full border border-brand/50 px-8 py-4 text-center font-body text-sm font-semibold uppercase tracking-widest text-brand transition-colors hover:bg-brand hover:text-carbon"
              >
                Llamar: {BRAND.phone}
              </a>
            </div>
          </form>

          <div className="flex flex-col gap-6">
            <a
              href={MAPS_SEARCH_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="group relative block h-64 overflow-hidden rounded-3xl border border-line bg-carbon-card"
            >
              <div className="grid-fresadora absolute inset-0" />
              <div className="absolute inset-0 bg-gradient-to-t from-carbon via-carbon/20 to-transparent" />
              <div className="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2 flex-col items-center gap-2 text-center transition-transform duration-300 group-hover:-translate-y-[60%]">
                <span className="flex h-12 w-12 items-center justify-center rounded-full border border-brand text-brand">
                  ●
                </span>
                <p className="font-body text-sm text-white">{BRAND.address}</p>
                <span className="brand-underline font-body text-xs uppercase tracking-wider text-brand">
                  Abrir en Google Maps
                </span>
              </div>
            </a>

            <div className="rounded-3xl border border-line bg-carbon-card/80 p-8 font-body text-white/70">
              <p className="text-xs uppercase tracking-[0.3em] text-brand">Contacto directo</p>
              <p className="mt-4 text-lg text-white">{BRAND.phone}</p>
              <p className="mt-1">{BRAND.email}</p>
              <p className="mt-4 text-sm">{BRAND.address}</p>
              <p className="mt-6 text-sm text-brand">{BRAND.rating.toFixed(1)} ★ en Google Maps</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
