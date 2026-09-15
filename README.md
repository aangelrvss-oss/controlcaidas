# Carrocerías Pintauto · Landing Page

Landing page monumental e inmersiva para **Carrocerías Pintauto** (C. de la Polea, 29-31,
Rivas-Vaciamadrid), taller de chapa y pintura con más de 50 años de historia (desde 1968),
concertado con Mapfre, AXA, Mutua Madrileña y otras aseguradoras.

## Concepto

- Estética **Dark Titanium & Cyan Blue**: fondos en gris titanio oscuro/negro, acentos en
  azul cian metálico y rojo industrial.
- Tipografía kinetic (Barlow Condensed) con efecto de brillo metálico y expansión al
  hacer scroll.
- Animaciones de scroll con GSAP + ScrollTrigger: parallax en el hero, showcase de
  tecnología con scroll horizontal pineado, timeline de historia 1968 → hoy.
- Vídeos hiperrealistas generados con Higgsfield: transformación del taller 1968 → 2026,
  cabina de pintura ecológica al agua, escaneo de bancada universal, partículas de
  recubrimiento cerámico y gota de agua repeliendo en acabado espejo.
- Selector interactivo en 3 pasos (aseguradora → tipo de servicio → datos del vehículo)
  que genera un mensaje de WhatsApp directo al taller para tramitar partes y citas.

## Stack

- React 19 + TypeScript + Vite
- Tailwind CSS v4
- GSAP + ScrollTrigger
- Fuentes autoalojadas (`@fontsource/rajdhani`, `@fontsource/barlow-condensed`)

## Desarrollo

```bash
npm install
npm run dev
```

## Estructura

- `src/components/Hero.tsx` — sección de apertura con vídeo de fondo y tipografía kinetic.
- `src/components/TrustCarousel.tsx` — carrusel infinito de aseguradoras concertadas.
- `src/components/TechShowcase.tsx` — showcase de tecnología con scroll horizontal pineado.
- `src/components/Timeline.tsx` — línea de tiempo 1968 → hoy.
- `src/components/PartesForm.tsx` — selector de 3 pasos para tramitar partes por WhatsApp.
- `src/components/ContactMap.tsx` — datos de contacto, jefe de taller y mapa.
- `src/data/` — contenido (aseguradoras, servicios, hitos, contacto, vídeos).
