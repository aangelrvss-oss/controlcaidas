import { useEffect, useRef } from "react"
import { PROCESS_STEPS } from "../lib/content"
import { getGsapCore } from "../lib/gsap"

export default function Process() {
  const sectionRef = useRef<HTMLElement | null>(null)
  const svgRef = useRef<SVGSVGElement | null>(null)
  const pathRef = useRef<SVGPathElement | null>(null)
  const stepsColumnRef = useRef<HTMLDivElement | null>(null)
  const stepRefs = useRef<Array<HTMLDivElement | null>>([])

  useEffect(() => {
    const { gsap } = getGsapCore()
    const section = sectionRef.current
    const svg = svgRef.current
    const path = pathRef.current
    const stepsColumn = stepsColumnRef.current
    if (!section || !svg || !path || !stepsColumn) return

    // SVG is a replaced element: with only `width` set, `height: auto` falls back to the
    // viewBox's intrinsic ratio instead of stretching via inset-y-0, so it's pinned here
    // to the steps column's real height in pixels.
    const syncHeight = () => {
      svg.style.height = `${stepsColumn.offsetHeight}px`
    }
    syncHeight()
    window.addEventListener("resize", syncHeight)

    const ctx = gsap.context(() => {
      const length = path.getTotalLength()
      gsap.set(path, { strokeDasharray: length, strokeDashoffset: length })

      gsap.to(path, {
        strokeDashoffset: 0,
        ease: "none",
        scrollTrigger: {
          trigger: section,
          start: "top 70%",
          end: "bottom 60%",
          scrub: 0.6,
        },
      })

      stepRefs.current.forEach((step, i) => {
        if (!step) return
        gsap.from(step, {
          opacity: 0,
          y: 40,
          duration: 0.6,
          scrollTrigger: {
            trigger: step,
            start: "top 78%",
          },
          delay: i * 0.05,
        })
      })
    }, section)

    return () => {
      window.removeEventListener("resize", syncHeight)
      ctx.revert()
    }
  }, [])

  return (
    <section id="proceso" ref={sectionRef} className="relative bg-carbon-soft py-28 md:py-40">
      <div className="mx-auto max-w-5xl px-6 lg:px-10">
        <div className="mb-20 text-center">
          <p className="font-body text-xs uppercase tracking-[0.3em] text-brand">Nuestro Proceso</p>
          <h2 className="font-display mt-2 text-4xl text-white md:text-6xl">Del plano a tu casa</h2>
        </div>

        <div className="relative">
          <svg
            ref={svgRef}
            className="absolute left-6 top-0 hidden w-8 md:block"
            viewBox="0 0 32 800"
            fill="none"
            preserveAspectRatio="none"
            aria-hidden
          >
            <path ref={pathRef} d="M16 0 L16 800" stroke="url(#brand-navy)" strokeWidth="2" />
            <defs>
              {/* userSpaceOnUse: this path is a perfectly vertical line (zero-width bounding
                  box), and objectBoundingBox gradients are spec'd to disable rendering in that case. */}
              <linearGradient id="brand-navy" gradientUnits="userSpaceOnUse" x1="16" y1="0" x2="16" y2="800">
                <stop offset="0%" stopColor="#E8452F" />
                <stop offset="100%" stopColor="#2547B0" />
              </linearGradient>
            </defs>
          </svg>

          <div ref={stepsColumnRef} className="flex flex-col gap-14 md:pl-20">
            {PROCESS_STEPS.map((step, i) => (
              <div
                key={step.id}
                ref={(el) => {
                  stepRefs.current[i] = el
                }}
                className="relative flex items-start gap-6 rounded-2xl border border-line bg-carbon-card/60 p-6 md:bg-transparent md:border-0 md:p-0"
              >
                <span className="font-display flex h-14 w-14 shrink-0 items-center justify-center rounded-full border border-brand/50 text-xl text-brand">
                  {String(step.id).padStart(2, "0")}
                </span>
                <div>
                  <h3 className="font-heading text-xl font-semibold text-white md:text-2xl">{step.title}</h3>
                  <p className="mt-2 max-w-md font-body text-sm text-white/60 md:text-base">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
