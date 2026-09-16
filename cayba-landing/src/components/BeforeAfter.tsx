import { useCallback, useRef, useState } from "react"
import { BEFORE_AFTER } from "../lib/content"

export default function BeforeAfter() {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const [position, setPosition] = useState(50)
  const draggingRef = useRef(false)

  const updateFromClientX = useCallback((clientX: number) => {
    const el = containerRef.current
    if (!el) return
    const rect = el.getBoundingClientRect()
    const pct = ((clientX - rect.left) / rect.width) * 100
    setPosition(Math.min(100, Math.max(0, pct)))
  }, [])

  const onPointerDown = (e: React.PointerEvent) => {
    draggingRef.current = true
    ;(e.target as HTMLElement).setPointerCapture(e.pointerId)
    updateFromClientX(e.clientX)
  }

  const onPointerMove = (e: React.PointerEvent) => {
    if (!draggingRef.current) return
    updateFromClientX(e.clientX)
  }

  const onPointerUp = () => {
    draggingRef.current = false
  }

  return (
    <section id="antes-despues" className="relative bg-carbon py-28 md:py-40">
      <div className="mx-auto max-w-6xl px-6 lg:px-10">
        <div className="mb-14 text-center">
          <p className="font-body text-xs uppercase tracking-[0.3em] text-gold">Transformación Real</p>
          <h2 className="font-display mt-2 text-4xl text-white md:text-6xl">Antes / Después</h2>
          <p className="mx-auto mt-4 max-w-xl font-body text-white/60">
            Arrastra para ver cómo una habitación vacía se convierte en un vestidor de roble iluminado a medida.
          </p>
        </div>

        <div
          ref={containerRef}
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          className="relative aspect-[16/9] w-full touch-pan-y select-none overflow-hidden rounded-3xl border border-line shadow-[0_40px_100px_rgba(0,0,0,0.55)]"
        >
          <video
            className="absolute inset-0 h-full w-full object-cover"
            style={{ clipPath: `inset(0 0 0 ${position}%)` }}
            autoPlay
            muted
            loop
            playsInline
            poster={BEFORE_AFTER.before.image}
          >
            <source src="/videos/before-after-morph.mp4" type="video/mp4" />
          </video>

          <img
            src={BEFORE_AFTER.after.image}
            alt="Vestidor de roble a medida terminado"
            className="absolute inset-0 h-full w-full object-cover"
            style={{ clipPath: `inset(0 ${100 - position}% 0 0)` }}
          />

          <div className="pointer-events-none absolute inset-y-0 z-10" style={{ left: `${position}%` }}>
            <div className="h-full w-[2px] bg-gold shadow-[0_0_20px_rgba(212,175,55,0.8)]" />
            <div className="absolute top-1/2 flex h-12 w-12 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full border-2 border-gold bg-carbon text-gold shadow-lg">
              <span className="text-xs">↔</span>
            </div>
          </div>

          <span className="absolute left-4 top-4 z-10 rounded-full bg-carbon/70 px-3 py-1 font-body text-xs uppercase tracking-wider text-white/80 backdrop-blur-sm">
            {BEFORE_AFTER.before.label}
          </span>
          <span className="absolute right-4 top-4 z-10 rounded-full bg-gold/90 px-3 py-1 font-body text-xs uppercase tracking-wider text-carbon backdrop-blur-sm">
            {BEFORE_AFTER.after.label}
          </span>
        </div>
      </div>
    </section>
  )
}
