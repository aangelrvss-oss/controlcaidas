import { useEffect, useState } from "react"
import { BRAND } from "../lib/content"
import Logo from "./Logo"

const LINKS = [
  { href: "#manifiesto", label: "Historia" },
  { href: "#servicios", label: "Servicios" },
  { href: "#antes-despues", label: "Antes / Después" },
  { href: "#proceso", label: "Proceso" },
  { href: "#contacto", label: "Contacto" },
]

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40)
    onScroll()
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : ""
    return () => {
      document.body.style.overflow = ""
    }
  }, [menuOpen])

  const closeMenu = () => setMenuOpen(false)

  return (
    <header
      className={`fixed top-0 z-50 w-full transition-all duration-500 ${
        scrolled || menuOpen
          ? "bg-carbon/85 backdrop-blur-md border-b border-line py-3 shadow-[0_10px_30px_rgba(0,0,0,0.4)]"
          : "bg-transparent py-6"
      }`}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 lg:px-10">
        <a href="#top" onClick={closeMenu}>
          <Logo />
        </a>

        <nav className="hidden items-center gap-8 md:flex">
          {LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="brand-underline font-body text-sm uppercase tracking-wider text-white/80 transition-colors hover:text-white"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <a
          href={BRAND.phoneHref}
          className="hidden rounded-full border border-brand/60 px-5 py-2 font-body text-sm uppercase tracking-wider text-brand transition-colors hover:bg-brand hover:text-carbon md:inline-block"
        >
          {BRAND.phone}
        </a>

        <button
          type="button"
          onClick={() => setMenuOpen((v) => !v)}
          aria-label={menuOpen ? "Cerrar menú" : "Abrir menú"}
          aria-expanded={menuOpen}
          className="relative z-50 flex h-10 w-10 flex-col items-center justify-center gap-1.5 md:hidden"
        >
          <span
            className={`h-[1.5px] w-6 bg-white transition-all duration-300 ${menuOpen ? "translate-y-[3.5px] rotate-45" : ""}`}
          />
          <span
            className={`h-[1.5px] w-6 bg-white transition-all duration-300 ${menuOpen ? "-translate-y-[3.5px] -rotate-45" : ""}`}
          />
        </button>
      </div>

      <div
        className={`grid overflow-hidden transition-all duration-[400ms] ease-out md:hidden ${
          menuOpen ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"
        }`}
      >
        <div className="overflow-hidden">
          <nav className="flex flex-col gap-1 border-t border-line px-6 pb-8 pt-4">
            {LINKS.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={closeMenu}
                className="border-b border-line/60 py-4 font-body text-base uppercase tracking-wider text-white/85 transition-colors hover:text-brand"
              >
                {link.label}
              </a>
            ))}
            <a
              href={BRAND.phoneHref}
              onClick={closeMenu}
              className="mt-6 rounded-full bg-brand px-5 py-3 text-center font-body text-sm font-semibold uppercase tracking-wider text-carbon"
            >
              Llamar: {BRAND.phone}
            </a>
          </nav>
        </div>
      </div>
    </header>
  )
}
