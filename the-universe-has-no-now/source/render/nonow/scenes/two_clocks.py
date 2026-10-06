import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    mode = p.get("mode", "sync")
    f = background(W, H, gradient=0.25)
    f += starfield2d(ctx, t, drift=(0.002, 0.0), gain=0.35, fov=80) * 0.6
    L = Layer(W, H)
    sec = 10.0 + t  # clock reading
    if mode in ("sync", "return", "doubt"):
        push = 1.0 + 0.04 * ease_in_out(t / max(dur, 1))
        r = 170 * s * push
        gap = 300 * s * push
        a = smooth(ramp(t, 0.0, 1.2)) if mode != "return" else smooth(ramp(t, 0.0, 0.8))
        secB = sec
        if mode == "doubt":
            # clock B hesitates: its hand lags more and more after t=1.5
            lag = 0.0 if t < 1.5 else 0.9 * (1 - math.exp(-(t - 1.5) / 1.6))
            secB = sec - lag
        draw_clock(L, W / 2 - gap, H / 2, r, sec, a=a, label="A", H=H)
        draw_clock(L, W / 2 + gap, H / 2, r, secB, a=a, label="B", H=H)
        # faint line of simultaneity between them
        L.line(W / 2 - gap + r * 1.15, H / 2, W / 2 + gap - r * 1.15, H / 2, P.dim, w=1.0, a=0.25 * a)
        if mode == "doubt":
            q = smooth(ramp(t, 2.0, 3.0))
            T.label(L, "SAME MOMENT ?", W / 2, H / 2 - 8 * s, H, a=q * 0.8, color=P.amber)
    elif mode == "sync_wide":
        a = smooth(ramp(t, 0.0, 0.8))
        r = 46 * s
        # curved horizon (planet limb) — two observers far apart on the same world
        y0 = H * 0.78
        pts = [(x, y0 + 0.00022 * (x - W / 2) ** 2 / s) for x in np.linspace(0, W, 80)]
        L.polyline(pts, P.dim, w=1.2, a=0.35 * a)
        for k, cx in enumerate((W * 0.22, W * 0.78)):
            cy = y0 - 170 * s + 0.00022 * (cx - W / 2) ** 2 / s
            silhouette_figure(L, cx, cy + 150 * s, 120 * s, color=(0.0, 0.0, 0.0), a=a, t=t)
            L.radial(cx, cy + 90 * s, 90 * s, P.amber, a=0.08 * a)
            draw_clock(L, cx, cy - 130 * s, r, sec, a=a, H=H, label=("A", "B")[k], minute=False)
        T.label(L, "6 000 km", W / 2, y0 - 30 * s, H, a=0.7 * a)
        L.line(W * 0.30, y0 - 50 * s, W * 0.70, y0 - 50 * s, P.dim, w=1.0, a=0.3 * a)
    composite(f, L)
    return f
