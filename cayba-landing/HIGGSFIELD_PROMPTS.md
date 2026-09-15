# CAYBA — Prompts de Higgsfield para vídeo y textura 3D

Esta landing está cableada para usar vídeo cinemático en tres puntos. Mientras no exista
el asset real, cada `<video>` cae automáticamente en una imagen fija (`poster` / Unsplash)
gracias al fallback nativo del navegador, así que la web funciona igual sin ellos.

Genera cada clip en Higgsfield con los prompts de abajo, expórtalo en **MP4 H.264, 4K,
loop perfecto, sin audio**, y colócalo en la ruta indicada. No hace falta tocar código:
en cuanto el archivo existe en `public/videos/...`, el `<video>` lo sirve automáticamente.

---

## 1. Hero — talla de madera cinemática

**Ruta de destino:** `public/videos/hero-wood-carving-loop.mp4`
**Duración:** 8–12 s en loop perfecto (primer y último frame deben coincidir en composición y luz)
**Formato:** 3840×2160, 24–25 fps, loop seamless

**Prompt:**
> Cinematic macro shot of a craftsman's gouge slowly carving a block of solid dark walnut
> wood, ultra slow motion, fine wood shavings and dust particles floating and drifting
> through a single dramatic shaft of warm overhead light (chiaroscuro, golden hour
> tungsten tone), shallow depth of field, tool and hands mostly out of focus in the
> foreground, wood grain in sharp cinematic focus, dark charcoal-black background,
> volumetric light rays catching dust motes, moody luxury furniture atelier aesthetic,
> shot on ARRI Alexa, 35mm lens, subtle camera drift, seamless loop, no text, no logos.

**Negative prompt:** `low resolution, cartoon, flat lighting, bright white background, people's faces, text overlays, logos, watermark, fast motion, shake`

---

## 2. Antes / Después — morphing de habitación a vestidor

**Ruta de destino:** `public/videos/before-after-morph.mp4`
**Duración:** 6–10 s
**Formato:** 3840×2160, 16:9, loop opcional (se reproduce clippeado por el slider interactivo, así que el loop es menos crítico que en el hero)

**Prompt:**
> Smooth cinematic time-lapse transformation of an empty, bare bedroom with white walls
> and bare concrete floor morphing seamlessly into a fully finished luxury walk-in closet
> made of light oak wood with integrated LED strip lighting, soft warm ambient glow,
> camera locked on a static wide tripod shot, consistent framing and perspective
> throughout the transition so the before and after align pixel-for-pixel, photorealistic
> interior design visualization, architectural render quality, dust-to-polish
> transformation feel, warm color grade, no people, no text.

**Negative prompt:** `camera movement, perspective shift, people, text, warped geometry, flickering`

> Nota técnica: para que el slider interactivo de "Antes/Después" funcione bien, el
> primer frame del vídeo debe coincidir en encuadre exacto con la imagen "antes"
> (`BEFORE_AFTER.before.image` en `src/lib/content.ts`) y el último frame con la imagen
> "después". Si Higgsfield no puede fijar cámara con precisión, genera el clip solo como
> referencia y usa fotografía real fija para el slider (ya soportado, ver `BeforeAfter.tsx`).

---

## 3. Texturas de madera para las tarjetas de Servicios

No son vídeo, pero Higgsfield también puede generar renders 3D fotorrealistas fijos
(exporta como PNG/JPG 4K) para sustituir las imágenes de stock en `src/lib/content.ts`
(campo `image` de cada objeto en `SERVICES`).

**01. Armarios & Vestidores** — sustituye `SERVICES[0].image`
> Photorealistic 3D render of a custom-built walk-in wardrobe interior in warm oak wood,
> soft-close sliding doors half open revealing organized shelving and drawers, warm
> interior LED lighting, luxury minimalist interior design, architectural visualization,
> shot straight-on, no people.

**02. Palillería & Escaleras** — sustituye `SERVICES[1].image`
> Extreme close-up photorealistic 3D render of vertical dark walnut wood slats
> (palillería) arranged in a rhythmic pattern with dramatic raking side light creating
> long shadows between each slat, luxury joinery detail, shallow depth of field,
> architectural material study.

**03. Mobiliario de Baño & Salón** — sustituye `SERVICES[2].image`
> Photorealistic interior render of a contemporary bathroom vanity unit in matte dark
> wood with brass fixtures, humidity-resistant lacquer finish, soft warm lighting,
> luxury minimalist bathroom design, no people.

**04. Reformas Integrales** — sustituye `SERVICES[3].image`
> Wide photorealistic architectural render of a fully renovated open-plan living space
> mid-construction-to-finished split, exposed structural beams on one side transitioning
> into a polished contemporary interior on the other, warm natural light, no people.

---

## 4. Transición "corte láser" entre secciones (opcional, pulido extra)

Si se quiere una transición de pantalla completa entre secciones (mencionada en el brief
como "distorsión/máscara de corte de madera"), genera un clip corto para usar como
overlay de máscara CSS (`mix-blend-mode` o `mask-image` con vídeo en escala de grises):

**Ruta sugerida:** `public/videos/laser-cut-transition.mp4`

**Prompt:**
> Top-down macro shot of a laser cutter head moving across a sheet of plywood, bright
> orange spark line following the cut path, thin trail of smoke, black background,
> high contrast, grayscale-friendly lighting (strong white cut line against pure black
> wood surface) so the footage can be used as a luminance mask, seamless horizontal pan,
> no text, no watermark.

---

## Flujo de trabajo recomendado

1. Genera cada clip en Higgsfield con el prompt correspondiente.
2. Exporta en MP4 H.264 (compatibilidad universal en navegadores).
3. Comprime a un tamaño razonable para web (idealmente <8MB por clip en 1080p, o usa
   4K solo si el hosting soporta streaming adaptativo).
4. Copia el archivo a la ruta exacta indicada en `public/videos/`.
5. Recarga la página — el `<video>` lo detecta automáticamente, sin cambios de código.
