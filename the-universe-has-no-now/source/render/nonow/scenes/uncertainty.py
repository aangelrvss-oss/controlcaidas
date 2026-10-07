"""Position/momentum as a Fourier pair: squeeze one wave packet and the other spreads. Δx·Δp ≥ ħ/2."""
import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    f = background(W, H, gradient=0.1)
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 0.8))
    # sigma_x oscillates slowly between wide and narrow; sigma_p = 1/(2 sigma_x) (ħ = 1)
    sx = 0.9 - 0.75 * (0.5 - 0.5 * math.cos(t * 0.9))   # 0.9 -> 0.15 -> ...
    sp = 1 / (2 * sx)
    def panel(x0, y0, w, h, sig, col, title, sym, k0=0.0):
        L.rect(x0, y0, w, h, P.dim, a=0.0, sw=1.0)
        L.line(x0, y0 + h, x0 + w, y0 + h, P.dim, w=1.0, a=0.5 * a)
        xs = np.linspace(-3, 3, 400)
        env = np.exp(-xs ** 2 / (4 * sig ** 2)) / math.sqrt(sig)
        env /= 1.6 / math.sqrt(0.15)
        pts = [(x0 + (xx + 3) / 6 * w, y0 + h - env[i] * h * 0.9) for i, xx in enumerate(xs)]
        # the oscillating real part (for the x-space packet)
        if k0:
            re = env * np.cos(k0 * xs - t * 2.0)
            pts2 = [(x0 + (xx + 3) / 6 * w, y0 + h * 0.5 - re[i] * h * 0.45) for i, xx in enumerate(xs)]
            L.polyline(pts2, col, w=1.2, a=0.35 * a)
        L.polyline(pts + [(x0 + w, y0 + h), (x0, y0 + h)], col, a=0.10 * a, fill=True)
        L.polyline(pts, col, w=2.2 * s, a=0.95 * a)
        T.label(L, title, x0 + w / 2, y0 - 26 * s, H, a=a, color=col)
        T.value(L, f"{sym} = {sig:4.2f}", x0 + w / 2, y0 + h + 44 * s, H, a=a, color=col, size=24)
        # width marker
        L.line(x0 + w / 2 - sig / 6 * w, y0 + h * 0.5, x0 + w / 2 + sig / 6 * w, y0 + h * 0.5, col, w=1.0, a=0.5 * a)
    panel(W * 0.08, H * 0.28, W * 0.38, H * 0.42, sx, P.cyan, "POSITION  |ψ(x)|²", "Δx", k0=6.0)
    panel(W * 0.54, H * 0.28, W * 0.38, H * 0.42, sp, P.amber, "MOMENTUM  |φ(p)|²", "Δp")
    T.equation(L, "Δx · Δp  ≥  ħ / 2", W / 2, H * 0.14, H, a=a, size=46)
    T.value(L, f"Δx · Δp = {sx*sp:4.2f} ħ   (minimum)", W / 2, H * 0.88, H, a=a * smooth(ramp(t, 2.0, 3.0)), color=P.ink, size=24)
    T.caption(L, "a wave narrow in position is necessarily broad in momentum: they are Fourier transforms of each other", W / 2, H * 0.93, H, a=a * 0.7 * smooth(ramp(t, 5.0, 6.0)), align="center", size=19)
    # arrow between panels
    L.line(W * 0.475, H * 0.49, W * 0.525, H * 0.49, P.dim, w=1.5, a=0.6 * a)
    T.label(L, "FOURIER", W * 0.5, H * 0.46, H, a=0.8 * a, size=13)
    composite(f, L)
    return f
