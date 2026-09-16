import { useEffect, useRef } from "react"
import { SERVICES } from "../lib/content"
import { getGsapCore } from "../lib/gsap"

export default function ServicesShowcase() {
  const containerRef = useRef<HTMLElement | null>(null)
  const trackRef = useRef<HTMLDivElement | null>(null)
  const doorLeftRef = useRef<HTMLDivElement | null>(null)
  const doorRightRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const { gsap } = getGsapCore()
    const container = containerRef.current
    const track = trackRef.current
    if (!container || !track) return

    const ctx = gsap.context(() => {
      const getScrollAmount = () => track.scrollWidth - window.innerWidth

      const tween = gsap.to(track, {
        x: () => -getScrollAmount(),
        ease: "none",
        scrollTrigger: {
          trigger: container,
          start: "top top",
          end: () => `+=${getScrollAmount()}`,
          scrub: 1,
          pin: true,
          invalidateOnRefresh: true,
          anticipatePin: 1,
          onUpdate: (self) => {
            // Card 0 ("Armarios") occupies roughly the first quarter of the scroll — open its
            // sliding doors in sync so the reveal lands while the card is centered on screen.
            const doorProgress = gsap.utils.clamp(0, 1, gsap.utils.mapRange(0, 0.32, 0, 1, self.progress))
            if (doorLeftRef.current) doorLeftRef.current.style.transform = `translateX(${-doorProgress * 100}%)`
            if (doorRightRef.current) doorRightRef.current.style.transform = `translateX(${doorProgress * 100}%)`
          },
        },
      })

      return () => {
        tween.scrollTrigger?.kill()
        tween.kill()
      }
    }, container)

    return () => ctx.revert()
  }, [])

  return (
    <section id="servicios" ref={containerRef} className="relative h-screen overflow-hidden bg-carbon">
      <div className="absolute left-1/2 top-20 z-20 -translate-x-1/2 text-center md:top-10">
        <p className="font-body text-xs uppercase tracking-[0.3em] text-gold">Showcase de Servicios</p>
        <h2 className="font-display mt-2 text-4xl text-white md:text-5xl">Lo que fabricamos</h2>
      </div>

      <div ref={trackRef} className="flex h-full w-max items-center gap-8 px-[8vw] pt-16 will-change-transform">
        {SERVICES.map((service) => (
          <article
            key={service.id}
            className="group relative h-[65vh] w-[80vw] shrink-0 overflow-hidden rounded-3xl border border-line bg-carbon-card shadow-[0_30px_80px_rgba(0,0,0,0.5)] sm:w-[60vw] lg:w-[42vw]"
            style={{ perspective: "1200px" }}
          >
            <div
              className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-105"
              style={{ backgroundImage: `url(${service.image})` }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-carbon via-carbon/40 to-transparent" />

            {service.accent === "door" && (
              <>
                <div
                  ref={doorLeftRef}
                  className="absolute inset-y-0 left-0 w-1/2 border-r border-gold/30 bg-carbon-soft/95 backdrop-blur-sm"
                  style={{ transform: "translateX(0%)" }}
                />
                <div
                  ref={doorRightRef}
                  className="absolute inset-y-0 right-0 w-1/2 border-l border-gold/30 bg-carbon-soft/95 backdrop-blur-sm"
                  style={{ transform: "translateX(0%)" }}
                />
              </>
            )}

            {service.accent === "slats" && (
              <div className="pointer-events-none absolute inset-0 flex">
                {Array.from({ length: 14 }, (_, i) => (
                  <div key={i} className="h-full flex-1 border-r border-carbon/70" />
                ))}
              </div>
            )}

            <div className="relative z-10 flex h-full flex-col justify-end p-8 md:p-10">
              <span className="font-display text-6xl text-gold/40 md:text-7xl">{service.index}</span>
              <h3 className="font-heading mt-4 max-w-md text-2xl font-semibold text-white md:text-3xl">
                {service.title}
              </h3>
              <p className="mt-3 max-w-md font-body text-sm text-white/70 md:text-base">{service.description}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
