import { useEffect, useRef } from "react"
import { BRAND } from "../lib/content"
import { useMagnetic } from "../lib/useMagnetic"
import { getGsapCore } from "../lib/gsap"
import { withSafeEnye } from "../lib/text"

const DUST_PARTICLES = Array.from({ length: 22 }, (_, i) => ({
  id: i,
  left: Math.round((i * 47) % 100),
  size: 2 + ((i * 7) % 5),
  duration: 10 + ((i * 13) % 14),
  delay: (i * 1.7) % 12,
}))

export default function Hero() {
  const sectionRef = useRef<HTMLElement | null>(null)
  const titleRef = useRef<HTMLHeadingElement | null>(null)
  const ctaRef = useMagnetic<HTMLAnchorElement>(0.4)

  useEffect(() => {
    const { gsap } = getGsapCore()
    const section = sectionRef.current
    const title = titleRef.current
    if (!section || !title) return

    const lines = title.querySelectorAll<HTMLElement>("[data-line]")

    const ctx = gsap.context(() => {
      gsap.set(lines, { letterSpacing: "0.35em", opacity: 0.35 })

      gsap.timeline({
        scrollTrigger: {
          trigger: section,
          start: "top top",
          end: "bottom top",
          scrub: 0.6,
        },
      })
        .to(lines, { letterSpacing: "0em", opacity: 1, stagger: 0.08, ease: "none" }, 0)
        .to(title, { scale: 1.08, ease: "none" }, 0)
        .to(section.querySelector("[data-hero-bg]"), { scale: 1.25, ease: "none" }, 0)
        .to(section, { opacity: 0.15, ease: "none" }, 0.7)
    }, section)

    return () => ctx.revert()
  }, [])

  return (
    <section
      id="top"
      ref={sectionRef}
      className="relative flex h-[100svh] min-h-[640px] w-full items-center justify-center overflow-hidden bg-carbon"
    >
      <div data-hero-bg className="absolute inset-0 h-full w-full">
        <video
          className="h-full w-full object-cover opacity-70 animate-kenburns"
          autoPlay
          muted
          loop
          playsInline
          poster="https://images.unsplash.com/photo-1553835973-dec43bfddbeb?w=1920&q=80&fit=crop"
        >
          <source src="/videos/hero-wood-carving-loop.mp4" type="video/mp4" />
        </video>
        <div className="absolute inset-0 bg-gradient-to-b from-carbon/70 via-carbon/40 to-carbon" />
        <div className="absolute inset-0 bg-gradient-to-r from-carbon/60 via-transparent to-carbon/60" />
      </div>

      <div className="noise-overlay" />

      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        {DUST_PARTICLES.map((p) => (
          <span
            key={p.id}
            className="dust-particle"
            style={{
              left: `${p.left}%`,
              width: p.size,
              height: p.size,
              animationDuration: `${p.duration}s`,
              animationDelay: `${p.delay}s`,
            }}
          />
        ))}
      </div>

      <div
        className="animate-pulse-badge absolute left-1/2 top-24 z-20 -translate-x-1/2 rounded-full border border-gold/40 bg-carbon/60 px-5 py-2 backdrop-blur-sm md:left-10 md:top-28 md:translate-x-0"
      >
        <p className="font-body text-[11px] uppercase tracking-[0.2em] text-bone/90 md:text-xs">
          {BRAND.city} &nbsp;|&nbsp; Desde el {BRAND.since} &nbsp;|&nbsp;{" "}
          <span className="text-gold">{BRAND.rating.toFixed(1)} ★</span>
        </p>
      </div>

      <div className="relative z-10 flex flex-col items-center gap-8 px-6 text-center">
        <h1
          ref={titleRef}
          className="font-display text-[13vw] leading-[0.88] text-white sm:text-[10vw] lg:text-[7.5vw]"
        >
          <span data-line className="block">
            Artesanía en madera.
          </span>
          <span data-line className="text-gradient-gold block">
            {withSafeEnye("Diseño sin límites.")}
          </span>
        </h1>

        <p className="max-w-xl font-body text-sm text-white/70 md:text-base">
          {BRAND.slogan}
        </p>

        <a
          ref={ctaRef}
          href="#contacto"
          className="group relative mt-4 inline-flex items-center gap-3 rounded-full bg-gold px-8 py-4 font-body text-sm font-semibold uppercase tracking-widest text-carbon transition-shadow duration-300 hover:shadow-[0_0_40px_rgba(212,175,55,0.5)]"
        >
          Diseña tu Espacio
          <span aria-hidden className="transition-transform duration-300 group-hover:translate-x-1">
            →
          </span>
        </a>
      </div>

      <div className="absolute bottom-8 left-1/2 z-10 -translate-x-1/2 text-center">
        <div className="mx-auto h-10 w-[1px] animate-pulse bg-gradient-to-b from-gold to-transparent" />
        <p className="mt-2 font-body text-[10px] uppercase tracking-[0.3em] text-white/40">Scroll</p>
      </div>
    </section>
  )
}
