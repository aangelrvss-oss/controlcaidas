import { CONTACT, buildWhatsappUrl } from "../data/contact";

export function Navbar() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/5 bg-titanium-900/70 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-3 sm:px-8">
        <a href="#inicio" className="flex items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-md border border-cyan-500/40 bg-titanium-800 font-kinetic text-lg font-bold text-cyan-400">
            P
          </span>
          <span className="font-kinetic text-xl font-semibold tracking-wide text-white">
            PINTAUTO
          </span>
        </a>

        <nav className="hidden items-center gap-7 font-kinetic text-sm uppercase tracking-widest text-white/70 md:flex">
          <a href="#tecnologia" className="transition hover:text-cyan-400">
            Tecnología
          </a>
          <a href="#trayectoria" className="transition hover:text-cyan-400">
            Trayectoria
          </a>
          <a href="#parte" className="transition hover:text-cyan-400">
            Tramitar Parte
          </a>
          <a href="#contacto" className="transition hover:text-cyan-400">
            Contacto
          </a>
        </nav>

        <a
          href={buildWhatsappUrl({})}
          target="_blank"
          rel="noreferrer"
          className="rounded-full bg-cyan-500 px-4 py-2 font-kinetic text-sm font-semibold uppercase tracking-wide text-titanium-950 transition hover:bg-cyan-400"
        >
          {CONTACT.whatsapp}
        </a>
      </div>
    </header>
  );
}
