# CAYBA — Landing inmersiva

Landing page promocional para **CAYBA S.L. — Mobiliario y Decoración**
(C. de la Fresadora 14, Polígono Santa Ana, Rivas-Vaciamadrid), carpintería y alta
ebanistería a medida.

Estética dark-mode premium con la marca real de CAYBA (rojo/naranja del icono de tejado +
azul marino del wordmark), tipografía kinética, scroll horizontal
con pinning, revelado de texto por scroll y un comparador antes/después interactivo.

## Stack

- React 19 + TypeScript + Vite
- Tailwind CSS v4 (tema custom: `carbon`, `brand` (rojo/naranja), `navy`, ver `src/index.css`)
- GSAP + ScrollTrigger para todas las animaciones ligadas al scroll

## Desarrollo

```bash
cd cayba-landing
npm install
npm run dev
```

```bash
npm run build    # build de producción
npm run lint      # oxlint
```

## Estructura

```
src/
  components/
    Logo.tsx              icono de tejado (recreado en SVG) + wordmark, usado en Nav y Footer
    Nav.tsx              nav fija, cambia de estilo al hacer scroll, menú hamburguesa en móvil
    Hero.tsx              tipografía kinética, HUD badge, CTA magnético, vídeo/dust
    Manifesto.tsx          revelado de texto palabra a palabra ligado al scroll
    ServicesShowcase.tsx   scroll horizontal con pin (GSAP), puertas correderas
    BeforeAfter.tsx        slider antes/después arrastrable
    Process.tsx            línea de blueprint animada + 4 pasos
    Contact.tsx             formulario -> WhatsApp/llamada + "mapa" oscuro
    Footer.tsx
  lib/
    content.ts             todos los textos/datos de marca (una sola fuente de verdad)
    useMagnetic.ts          hook para el botón magnético del hero
    gsap.ts                 registro de ScrollTrigger (una vez)
    text.tsx                fix de compatibilidad de fuente (ver nota abajo)
```

## Vídeo e imágenes

Los tres puntos de vídeo cinemático (hero, antes/después, transición opcional) están
cableados con `<video poster="...">` apuntando a rutas en `public/videos/` que **no
existen todavía**: el navegador cae automáticamente en la imagen `poster` mientras tanto,
así que la web funciona igual sin los vídeos.

Los prompts exactos para generar esos clips (y las texturas 3D de madera) con Higgsfield
están en **[`HIGGSFIELD_PROMPTS.md`](./HIGGSFIELD_PROMPTS.md)**. Cuando tengas los MP4,
solo hay que copiarlos a la ruta indicada — no requiere tocar código.

Las imágenes de servicio actuales usan Unsplash como placeholder; sustitúyelas por fotos
reales de proyectos de CAYBA en `src/lib/content.ts` cuando estén disponibles.

## Nota: fuente Bebas Neue y la "ñ"

Se detectó que la build de Bebas Neue servida por Google Fonts no incluye el glifo de la
"ñ" (sí incluye vocales acentuadas como "í"), por lo que "Diseño" se renderizaba como
"Diseno" en los títulos grandes. `src/lib/text.tsx` (`withSafeEnye`) envuelve solo ese
carácter en la fuente secundaria (Syne) para que siga siendo legible sin perder la
estética de Bebas Neue en el resto del texto. Si en el futuro se cambia la fuente de
display, conviene revisar si este workaround sigue siendo necesario.

## Personalización rápida

- Todos los datos de marca (teléfono, dirección, servicios, pasos del proceso, tipos de
  mueble del formulario) están centralizados en `src/lib/content.ts`.
- Paleta de color y fuentes: `src/index.css`, bloque `@theme`.
