import { useEffect, useRef } from "react"
import { BRAND } from "../lib/content"
import { getGsapCore } from "../lib/gsap"

const HEADLINE =
  "Del pequeño taller artesanal a la ebanistería de alta gama en Rivas-Vaciamadrid."

export default function Manifesto() {
  const sectionRef = useRef<HTMLElement | null>(null)
  const textRef = useRef<HTMLParagraphElement | null>(null)

  useEffect(() => {
    const { gsap } = getGsapCore()
    const section = sectionRef.current
    const text = textRef.current
    if (!section || !text) return

    const words = text.querySelectorAll<HTMLElement>(".reveal-word")

    const ctx = gsap.context(() => {
      gsap.to(words, {
        opacity: 1,
        stagger: 0.06,
        ease: "none",
        scrollTrigger: {
          trigger: section,
          start: "top 75%",
          end: "bottom 55%",
          scrub: 0.5,
        },
      })

      gsap.to(section.querySelector("[data-bg-image]"), {
        filter: "blur(0px)",
        opacity: 0.35,
        scale: 1.05,
        ease: "none",
        scrollTrigger: {
          trigger: section,
          start: "top bottom",
          end: "bottom top",
          scrub: 0.6,
        },
      })
    }, section)

    return () => ctx.revert()
  }, [])

  return (
    <section id="manifiesto" ref={sectionRef} className="relative overflow-hidden bg-carbon-soft py-32 md:py-48">
      <div
        data-bg-image
        className="absolute inset-0 bg-cover bg-center opacity-0 blur-md"
        style={{
          backgroundImage:
            "url(https://images.unsplash.com/photo-1601058268499-e52658b8bb88?w=1920&q=80&fit=crop)",
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-carbon-soft via-carbon-soft/80 to-carbon-soft" />
      <div className="noise-overlay" />

      <div className="relative z-10 mx-auto max-w-5xl px-6 lg:px-10">
        <p className="mb-8 font-body text-xs uppercase tracking-[0.3em] text-gold">Manifiesto &amp; Historia</p>

        <p
          ref={textRef}
          className="font-heading text-3xl font-semibold leading-tight text-white sm:text-4xl md:text-5xl lg:text-6xl"
        >
          {HEADLINE.split(" ").map((word, i) => (
            <span key={i} className="reveal-word">
              {word}{" "}
            </span>
          ))}
        </p>

        <div className="mt-16 grid gap-10 md:grid-cols-2">
          <p className="font-body text-base leading-relaxed text-white/70">
            Nacidos en el {BRAND.since} como taller artesanal fundado por{" "}
            <span className="text-bone">{BRAND.founders}</span>, décadas de oficio se han convertido en la
            carpintería de referencia de {BRAND.city}.
          </p>
          <p className="font-body text-base leading-relaxed text-white/70">
            Hoy seguimos siendo <span className="text-gold">los carpinteros del barrio</span>: la misma cercanía
            de siempre, elevada a la alta ebanistería a medida que exige cada proyecto contemporáneo.
          </p>
        </div>
      </div>
    </section>
  )
}
