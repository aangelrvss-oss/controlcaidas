import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    f = background(W, H, gradient=0.2)
    f += starfield2d(ctx, t, drift=(0.001, 0.0), gain=0.25, fov=80) * 0.5
    L = Layer(W, H)
    phase = p.get("phase", "two")
    if phase == "two":
        a1 = smooth(ramp(t, 0.3, 1.3)); a2 = smooth(ramp(t, 5.4, 6.4))
        T.label(L, "POSTULATE I", W * 0.27, H * 0.26, H, a=a1, color=P.amber)
        T.quote(L, ["The laws of physics are the same", "in every inertial frame."], W * 0.27, H * 0.36, H, a=a1, size=30)
        T.label(L, "POSTULATE II", W * 0.73, H * 0.26, H, a=a2, color=P.cyan)
        T.quote(L, ["The speed of light in vacuum is the same", "for every observer: c = 299 792 458 m/s."], W * 0.73, H * 0.36, H, a=a2, size=30)
        # lower diagram: three observers at different speeds, one light pulse passing all at c
        y = H * 0.70
        L.line(W * 0.08, y, W * 0.92, y, P.dim, w=1.0, a=0.3)
        speeds = (0.0, 0.25, 0.5)
        for k, v in enumerate(speeds):
            x = W * (0.2 + 0.08 * k) + v * 120 * s * (t % 6)
            if x < W * 0.9:
                silhouette_figure(L, x, y, 90 * s, color=(0.0, 0.0, 0.0), a=1.0, t=t + k)
                L.radial(x, y - 45 * s, 70 * s, P.amber if k == 0 else P.dim, a=0.07)
                T.label(L, f"v = {v:.2f} c" if v else "v = 0", x, y + 30 * s, H, a=0.8, size=16)
        # light pulse crosses at fixed speed regardless
        xp = W * 0.08 + ((t * 0.55) % 1.0) * W * 0.84
        L.radial(xp, y - 60 * s, 26 * s, P.cyan, a=0.9)
        L.circle(xp, y - 60 * s, 4 * s, (1, 1, 1), a=1.0)
        L.line(W * 0.08, y - 60 * s, xp, y - 60 * s, P.cyan, w=1.2, a=0.35)
        T.label(L, "c", xp, y - 85 * s, H, a=0.9, color=P.cyan, size=18)
        T.label(L, "the same c, measured by all three", W / 2, H * 0.86, H, a=0.7 * smooth(ramp(t, 7.0, 8.0)))
    else:
        a = smooth(ramp(t, 0.2, 1.0))
        T.quote(L, ["same laws", "+", "same speed of light"], W / 2, H * 0.42, H, a=a, size=40)
        # the word NOW comes apart: letters drift away from each other
        sep = 70 * s * smooth(ramp(t, 2.6, 4.4))
        T.label(L, "A SHARED", W / 2, H * 0.60, H, a=a)
        letters = ["N", "O", "W"]
        size = 96 * s
        widths = [L.text_width(ch, size, "Display-Light") for ch in letters]
        total = sum(widths)
        x = W / 2 - total / 2 - sep
        for k, ch in enumerate(letters):
            L.text(ch, x, H * 0.70, size, P.amber, a, "Display-Light", align="left")
            x += widths[k] + sep
        if sep > 1:
            T.label(L, "no longer shared", W / 2, H * 0.78, H, a=a * smooth(ramp(t, 4.0, 5.0)), color=P.dim)
    composite(f, L)
    return f
