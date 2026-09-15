import { CONTACT, buildWhatsappUrl } from "../data/contact";

export function ContactMap() {
  return (
    <section id="contacto" className="relative bg-titanium-950 px-6 py-28 sm:px-10">
      <div className="mx-auto grid max-w-6xl gap-10 lg:grid-cols-2">
        <div>
          <p className="font-kinetic text-xs uppercase tracking-[0.35em] text-cyan-400">
            Visítanos
          </p>
          <h2 className="font-kinetic mt-2 text-3xl font-bold uppercase text-white sm:text-5xl">
            Estamos en Rivas
          </h2>
          <p className="mt-4 max-w-md text-sm text-white/60 sm:text-base">
            {CONTACT.address} · Línea Interurbana 322
          </p>

          <div className="mt-8 flex flex-col gap-4 rounded-2xl border border-white/10 bg-titanium-800/60 p-6">
            <div>
              <span className="font-kinetic text-xs uppercase tracking-widest text-white/40">
                Teléfono taller
              </span>
              <p className="mt-1 font-kinetic text-lg font-semibold text-white">
                {CONTACT.phones.join(" · ")}
              </p>
            </div>
            <div>
              <span className="font-kinetic text-xs uppercase tracking-widest text-white/40">
                WhatsApp directo
              </span>
              <p className="mt-1 font-kinetic text-lg font-semibold text-cyan-400">
                {CONTACT.whatsapp}
              </p>
            </div>
            <div>
              <span className="font-kinetic text-xs uppercase tracking-widest text-white/40">
                {CONTACT.jefeTaller.role}
              </span>
              <p className="mt-1 font-kinetic text-lg font-semibold text-white">
                {CONTACT.jefeTaller.name} · {CONTACT.jefeTaller.phone}
              </p>
            </div>
          </div>

          <a
            href={buildWhatsappUrl({})}
            target="_blank"
            rel="noreferrer"
            className="animate-neon-pulse mt-8 inline-flex rounded-full bg-cyan-500 px-8 py-4 font-kinetic text-sm font-bold uppercase tracking-wide text-titanium-950 transition hover:bg-cyan-400"
          >
            Hablar con el taller ahora
          </a>
        </div>

        <div className="relative h-80 overflow-hidden rounded-2xl border border-white/10 lg:h-full">
          <div className="absolute inset-0 [filter:invert(92%)_hue-rotate(180deg)_contrast(0.9)_brightness(0.85)]">
            <iframe
              title="Carrocerías Pintauto en el mapa"
              src={CONTACT.mapEmbedUrl}
              className="h-full w-full border-0"
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
            />
          </div>
          <div className="pointer-events-none absolute inset-0 ring-1 ring-inset ring-cyan-500/20" />
        </div>
      </div>
    </section>
  );
}
