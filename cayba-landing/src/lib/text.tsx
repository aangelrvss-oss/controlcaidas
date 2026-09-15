import type { ReactNode } from "react"

/**
 * The Bebas Neue webfont serves an incomplete Latin-1 set in some delivery paths
 * (missing ñ/Ñ while other accented vowels are present), silently rendering "Diseño"
 * as "Diseno". Wrap just that glyph in a font known to carry it so display headings
 * stay legible regardless of the active Bebas Neue build.
 */
export function withSafeEnye(text: string): ReactNode[] {
  return text.split(/([ñÑ])/g).map((chunk, i) =>
    chunk === "ñ" || chunk === "Ñ" ? (
      <span key={i} style={{ fontFamily: "var(--font-heading)" }}>
        {chunk}
      </span>
    ) : (
      chunk
    ),
  )
}
