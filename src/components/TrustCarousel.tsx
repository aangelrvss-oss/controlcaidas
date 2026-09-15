import { insurers } from "../data/insurers";

export function TrustCarousel() {
  const track = [...insurers, ...insurers];

  return (
    <section className="relative border-y border-white/5 bg-titanium-950 py-14">
      <div className="mx-auto max-w-4xl px-6 text-center">
        <p className="font-kinetic text-xs uppercase tracking-[0.35em] text-cyan-400">
          Confianza total
        </p>
        <h2 className="font-kinetic mt-2 text-2xl font-bold uppercase text-white sm:text-3xl">
          Concertado con todas las aseguradoras
        </h2>
        <p className="mt-3 text-sm text-white/60 sm:text-base">
          Gestionamos el 100% de los trámites de tu seguro sin papeleos ni complicaciones para ti.
        </p>
      </div>

      <div className="relative mt-10 overflow-hidden">
        <div className="pointer-events-none absolute inset-y-0 left-0 z-10 w-24 bg-gradient-to-r from-titanium-950 to-transparent" />
        <div className="pointer-events-none absolute inset-y-0 right-0 z-10 w-24 bg-gradient-to-l from-titanium-950 to-transparent" />

        <div className="animate-marquee flex w-max gap-6">
          {track.map((insurer, i) => (
            <div
              key={`${insurer.id}-${i}`}
              className="flex min-w-[220px] flex-col items-center justify-center gap-1 rounded-xl border border-white/10 bg-gradient-to-b from-titanium-800 to-titanium-900 px-8 py-6 shadow-[0_0_25px_-10px_rgba(0,180,216,0.4)]"
            >
              <span className="font-kinetic text-xl font-bold uppercase tracking-wide text-white">
                {insurer.name}
              </span>
              {insurer.tag && (
                <span className="font-kinetic text-[11px] uppercase tracking-widest text-cyan-400">
                  {insurer.tag}
                </span>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
