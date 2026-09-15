import { useEffect, useState } from "react"
import { BRAND } from "../lib/content"

const LINKS = [
  { href: "#manifiesto", label: "Historia" },
  { href: "#servicios", label: "Servicios" },
  { href: "#antes-despues", label: "Antes / Después" },
  { href: "#proceso", label: "Proceso" },
  { href: "#contacto", label: "Contacto" },
]

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40)
    onScroll()
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  return (
    <header
      className={`fixed top-0 z-50 w-full transition-all duration-500 ${
        scrolled
          ? "bg-carbon/85 backdrop-blur-md border-b border-line py-3 shadow-[0_10px_30px_rgba(0,0,0,0.4)]"
          : "bg-transparent py-6"
      }`}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 lg:px-10">
        <a href="#top" className="font-display text-2xl tracking-widest text-white">
          CAY<span className="text-gold">BA</span>
        </a>

        <nav className="hidden items-center gap-8 md:flex">
          {LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="wood-underline font-body text-sm uppercase tracking-wider text-white/80 transition-colors hover:text-white"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <a
          href={BRAND.phoneHref}
          className="hidden rounded-full border border-gold/60 px-5 py-2 font-body text-sm uppercase tracking-wider text-gold transition-colors hover:bg-gold hover:text-carbon md:inline-block"
        >
          {BRAND.phone}
        </a>
      </div>
    </header>
  )
}
