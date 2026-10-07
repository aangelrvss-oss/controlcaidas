import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    f = background(W, H, gradient=0.15)
    f += starfield2d(ctx, t, gain=0.3, fov=70, drift=(0.003, 0)) * 0.6
    cx, cy, r = W * 0.33, H * 0.55, 230 * s
    rgb, al = earth_disc(ctx, cx, cy, r, light_dir=(-0.7, -0.4), t=t)
    over(f, rgb, al)
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 1.0))
    # satellite orbits: 3 inclined circles in perspective
    for k in range(3):
        R = r * 1.9; inc = math.radians(55); rot = k * 2.1 + 0.3
        pts = []
        for i in range(121):
            th = 2 * math.pi * i / 120
            x, y, z = R * math.cos(th), R * math.sin(th) * math.cos(inc), R * math.sin(th) * math.sin(inc)
            xr = x * math.cos(rot) - z * math.sin(rot); zr = x * math.sin(rot) + z * math.cos(rot)
            pts.append((cx + xr, cy + y, zr))
        front = [(x, y) for x, y, z in pts if z >= -0.1 * R]
        L.polyline([(x, y) for x, y, z in pts], P.dim, w=1.0, a=0.25 * a)
        # satellite
        th = t * 0.35 + k * 2.0
        x, y, z = R * math.cos(th), R * math.sin(th) * math.cos(inc), R * math.sin(th) * math.sin(inc)
        xr = x * math.cos(rot) - z * math.sin(rot); zr = x * math.sin(rot) + z * math.cos(rot)
        sx, sy = cx + xr, cy + y
        L.radial(sx, sy, 14 * s, P.amber, a=0.8 * a); L.circle(sx, sy, 3 * s, (1, 1, 1), a=a)
        # signal line to a ground point
        gx, gy = cx - r * 0.55, cy + r * 0.25
        L.line(sx, sy, gx, gy, P.cyan, w=1.0, a=0.35 * a * (0.5 + 0.5 * math.sin(t * 3 + k)))
    # ground point & drifting error circle
    gx, gy = cx - r * 0.55, cy + r * 0.25
    L.circle(gx, gy, 4 * s, P.cyan, a=a)
    days = min(1.0, max(0.0, (t - 5.0) / 6.0))
    err = 10.0 * days
    L.circle(gx, gy, 8 * s + 70 * s * days, P.red, w=1.5 * s, a=0.8 * a * smooth(ramp(t, 5.0, 5.6)))
    # readout panel
    x0 = W * 0.64
    T.label(L, "GPS SATELLITE CLOCK  vs  GROUND CLOCK", x0, H * 0.26, H, a=a, align="left", color=P.ink)
    r1 = smooth(ramp(t, 1.0, 1.8)); r2 = smooth(ramp(t, 2.2, 3.0)); r3 = smooth(ramp(t, 3.4, 4.2))
    x1 = x0 + 600 * s
    T.value(L, "special relativity (speed)", x0, H * 0.34, H, a=r1, align="left", color=P.cyan, size=24)
    T.value(L, "−  7 µs / day", x1, H * 0.34, H, a=r1, align="right", color=P.cyan, size=24)
    T.value(L, "general relativity (altitude)", x0, H * 0.39, H, a=r2, align="left", color=P.amber, size=24)
    T.value(L, "+ 45 µs / day", x1, H * 0.39, H, a=r2, align="right", color=P.amber, size=24)
    L.line(x0, H * 0.415, x1, H * 0.415, P.dim, w=1.0, a=0.5 * r3)
    T.value(L, "net", x0, H * 0.46, H, a=r3, align="left", color=P.ink, size=24)
    T.value(L, "+ 38 µs / day", x1, H * 0.46, H, a=r3, align="right", color=P.ink, size=24)
    r4 = smooth(ramp(t, 5.0, 5.8))
    T.label(L, "POSITION ERROR IF UNCORRECTED", x0, H * 0.58, H, a=r4, align="left")
    T.value(L, f"after {days*24:4.1f} h   ≈  {err:4.1f} km", x0, H * 0.64, H, a=r4, align="left", color=P.red, size=28)
    T.source_note(L, "Ashby, Living Rev. Relativ. 6, 1 (2003) · NIST", W, H, a=r1)
    composite(f, L)
    return f
