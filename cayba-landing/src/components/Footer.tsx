import { BRAND } from "../lib/content"
import Logo from "./Logo"

export default function Footer() {
  return (
    <footer className="border-t border-line bg-carbon py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 text-center lg:flex-row lg:text-left">
        <a href="#top">
          <Logo />
        </a>
        <p className="font-body text-xs text-white/40">
          {BRAND.legalName} · {BRAND.address}
        </p>
        <p className="font-body text-xs text-white/40">
          © {new Date().getFullYear()} CAYBA. Los carpinteros del barrio.
        </p>
      </div>
    </footer>
  )
}
