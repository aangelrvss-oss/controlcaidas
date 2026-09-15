import { CONTACT } from "../data/contact";

export function Footer() {
  return (
    <footer className="border-t border-white/5 bg-titanium-950 px-6 py-10 sm:px-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 text-center sm:flex-row sm:text-left">
        <div>
          <span className="font-kinetic text-lg font-bold uppercase tracking-wide text-white">
            Carrocerías Pintauto
          </span>
          <p className="mt-1 text-xs text-white/40">
            {CONTACT.address} · Desde {CONTACT.founded}
          </p>
        </div>
        <p className="text-xs text-white/30">
          © {new Date().getFullYear()} Carrocerías Pintauto. Taller concertado Mapfre, AXA y Mutua Madrileña.
        </p>
      </div>
    </footer>
  );
}
