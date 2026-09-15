import { useRef, useEffect } from "react"

/** Attracts the element towards the cursor while hovered, springs back on leave. */
export function useMagnetic<T extends HTMLElement>(strength = 0.35) {
  const ref = useRef<T | null>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const handleMove = (event: MouseEvent) => {
      const rect = el.getBoundingClientRect()
      const relX = event.clientX - (rect.left + rect.width / 2)
      const relY = event.clientY - (rect.top + rect.height / 2)
      el.style.transform = `translate(${relX * strength}px, ${relY * strength}px)`
    }

    const handleLeave = () => {
      el.style.transform = "translate(0, 0)"
    }

    el.addEventListener("mousemove", handleMove)
    el.addEventListener("mouseleave", handleLeave)
    return () => {
      el.removeEventListener("mousemove", handleMove)
      el.removeEventListener("mouseleave", handleLeave)
    }
  }, [strength])

  return ref
}
