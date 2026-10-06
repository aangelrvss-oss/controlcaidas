"""Gravitational time dilation: two clocks at different heights; the lower one runs slow (exaggerated, labelled)."""
import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    f = background(W, H, gradient=0.14, center=(0.5, 0.95))
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 0.8))
    # ground / potential well suggestion: horizontal contour lines denser near the ground
    for k in range(14):
        yy = H * 0.92 - (k ** 1.45) * 16 * s
        L.line(W * 0.15, yy, W * 0.85, yy, P.amber, w=1.0, a=0.12 * a * (1 - k / 16))
    L.line(W * 0.1, H * 0.92, W * 0.9, H * 0.92, P.ink, w=1.5, a=0.5 * a)
    # vertical scale with height marks
    xs = W * 0.5
    L.line(xs, H * 0.92, xs, H * 0.22, P.dim, w=1.0, a=0.5 * a)
    # two clocks: lower at height 0, upper raised by 33 cm (exaggerated 1.0 m visual)
    y_low = H * 0.70; y_high = H * 0.40
    r = 90 * s
    exag = 0.12  # exaggerated fractional rate difference (labelled)
    draw_clock(L, W * 0.30, y_low, r, 10 + t, a=a, H=H, label="LOWER CLOCK", minute=False)
    draw_clock(L, W * 0.70, y_high, r, 10 + t * (1 + exag), a=a, H=H, label="RAISED 33 cm", minute=False)
    L.line(W * 0.30 + r + 20 * s, y_low, xs - 10 * s, y_low, P.dim, w=1.0, a=0.3 * a)
    L.line(W * 0.70 - r - 20 * s, y_high, xs + 10 * s, y_high, P.dim, w=1.0, a=0.3 * a)
    T.label(L, "Δh = 33 cm", xs + 70 * s, (y_low + y_high) / 2, H, a=a * 0.9, color=P.amber)
    L.line(xs, y_low, xs, y_high, P.amber, w=2.0, a=0.8 * a)
    # readouts
    r1 = smooth(ramp(t, 3.0, 3.8)); r2 = smooth(ramp(t, 6.0, 6.8))
    T.equation(L, "Δf / f  =  g Δh / c²  ≈  3.6 × 10⁻¹⁷", W / 2, H * 0.14, H, a=r1, size=36)
    T.caption(L, "one extra second every ~900 million years  ·  rate difference exaggerated on screen", W / 2, H * 0.19, H, a=r1 * 0.8, align="center", size=20)
    T.source_note(L, "Chou, Hume, Rosenband & Wineland, Science 329, 1630 (2010): Al⁺ optical clocks, Δh = 33 cm", W, H, a=r2)
    composite(f, L)
    return f
