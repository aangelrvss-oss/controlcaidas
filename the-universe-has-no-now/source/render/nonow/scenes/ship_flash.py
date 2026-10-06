import math
from .common import *

def ship_outline(L, cx, cy, w, h, a=1.0, color=P.ink):
    """A long vessel: rounded hull with a tapered nose (to the right)."""
    L.rect(cx - w / 2, cy - h / 2, w, h, color, a=a, sw=1.6, rx=h * 0.28)
    # windows
    for i in range(-5, 6):
        L.circle(cx + i * w * 0.075, cy - h * 0.18, h * 0.045, color, w=1.0, a=a * 0.45)
    # nose marker
    L.line(cx + w / 2, cy - h * 0.1, cx + w / 2 + h * 0.4, cy, color, w=1.6, a=a)
    L.line(cx + w / 2, cy + h * 0.1, cx + w / 2 + h * 0.4, cy, color, w=1.6, a=a)

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    frame = p.get("frame", "ship")
    f = background(W, H, gradient=0.2)
    f += starfield2d(ctx, t, drift=(0.0, 0.0), gain=0.25, fov=80) * 0.5
    L = Layer(W, H)
    v = 0.45  # ship speed as fraction of c (platform frame)
    c = 240 * s  # pixels per second for light
    w, h = 760 * s, 170 * s
    T0 = 3.2  # flash time (local)
    def one(cy, moving, title, a=1.0, scale=1.0):
        ww, hh = w * scale, h * scale
        cx = W / 2 + (v * c * (t - T0) if moving else 0.0)
        ship_outline(L, cx, cy, ww, hh, a=a)
        T.label(L, title, W / 2, cy - hh * 0.75, H, a=a * 0.9, color=P.amber if not moving else P.cyan)
        if moving:
            # motion streaks
            for i in range(8):
                y = cy - hh / 2 + hh * (i + 0.5) / 8
                L.line(cx - ww / 2 - 40 * s, y, cx - ww / 2 - 140 * s - 30 * s * (i % 3), y, P.dim, w=1.0, a=0.18 * a)
        if t >= T0:
            te = t - T0
            x0 = W / 2 + (v * c * 0 if moving else 0)  # emission point stays fixed in this frame
            R = c * te
            # light fronts: two pulses (left/right), plus the expanding circle
            L.circle(x0, cy, R, P.cyan, w=1.5 * scale, a=a * max(0.0, 0.9 - te * 0.12))
            for sgn in (-1, 1):
                xp = x0 + sgn * R
                # has it hit the wall?
                wall = cx + sgn * ww / 2
                hit = (sgn * (xp - wall) >= 0)
                xp = wall if hit else xp
                L.radial(xp, cy, 22 * s, P.cyan, a=0.9 * a)
                L.circle(xp, cy, 3.5 * s, (1, 1, 1), a=a)
                if hit:
                    L.line(wall, cy - hh / 2, wall, cy + hh / 2, P.cyan, w=4 * scale, a=a * 0.9)
            L.radial(x0, cy, 14 * s, (1, 1, 1), a=0.5 * a)
            # arrival times (in the frame's own clock)
            tb = (ww / 2) / (c * (1 + v)) if moving else (ww / 2) / c
            tf = (ww / 2) / (c * (1 - v)) if moving else (ww / 2) / c
            yv = cy + hh * 0.85
            T.value(L, f"back  t = {tb:.2f}", cx - ww * 0.28, yv, H, a=a * smooth(ramp(te, tb, tb + 0.4)), color=P.cyan, size=22)
            T.value(L, f"front t = {tf:.2f}", cx + ww * 0.28, yv, H, a=a * smooth(ramp(te, tf, tf + 0.4)), color=P.cyan, size=22)
            if moving:
                T.label(L, "BACK FIRST", cx, yv + 34 * s, H, a=a * smooth(ramp(te, tf + 0.3, tf + 0.9)), color=P.amber)
            else:
                T.label(L, "SAME INSTANT", cx, yv + 34 * s, H, a=a * smooth(ramp(te, tb + 0.3, tb + 0.9)), color=P.amber)
    a = smooth(ramp(t, 0.0, 0.8))
    if frame == "ship":
        one(H * 0.5, False, "SEEN FROM THE SHIP", a)
    elif frame == "platform":
        one(H * 0.5, True, "SEEN FROM THE PLATFORM", a)
    else:
        one(H * 0.30, False, "SHIP FRAME", a, scale=0.72)
        one(H * 0.72, True, "PLATFORM FRAME", a, scale=0.72)
        q = smooth(ramp(t, 6.0, 7.0))
        T.label(L, "BOTH ARE CORRECT", W / 2, H * 0.515, H, a=q, color=P.ink)
    composite(f, L)
    return f
