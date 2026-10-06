import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    f = background(W, H, gradient=0.18)
    f += starfield2d(ctx, t, gain=0.2, fov=80) * 0.4
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 0.8))
    v = 0.6; g = 1 / math.sqrt(1 - v * v)
    h = 230 * s                      # mirror separation (px)
    Tb = 1.1                          # one-way light time, rest frame (s)
    c_px = h / Tb
    # ---------- stationary light clock (upper left)
    x0, yc = W * 0.17, H * 0.37
    mw = 90 * s
    def mirrors(x, y, aa):
        L.line(x - mw, y - h / 2, x + mw, y - h / 2, P.ink, w=3 * s, a=aa)
        L.line(x - mw, y + h / 2, x + mw, y + h / 2, P.ink, w=3 * s, a=aa)
    mirrors(x0, yc, a)
    ph = (t / Tb) % 2.0
    yp = yc - h / 2 + h * (ph if ph < 1 else 2 - ph)
    L.line(x0, yc - h / 2, x0, yc + h / 2, P.cyan, w=1.0, a=0.25 * a)
    L.radial(x0, yp, 18 * s, P.cyan, a=0.9 * a); L.circle(x0, yp, 3.5 * s, (1, 1, 1), a=a)
    ticks0 = int(t / (2 * Tb))
    T.label(L, "AT REST", x0, yc - h / 2 - 28 * s, H, a=a, color=P.amber)
    T.value(L, f"ticks  {ticks0:2d}", x0, yc + h / 2 + 44 * s, H, a=a, color=P.amber)
    # ---------- moving light clock (travels across the upper band)
    xs = W * 0.36; xm = xs + v * c_px * t
    aa = a * smooth(ramp(t, 0.6, 1.4))
    if xm < W + mw:
        mirrors(xm, yc, aa)
        # pulse: in the lab frame the vertical speed is c*sqrt(1-v^2) -> one-way time Tb*g
        phm = (t / (Tb * g)) % 2.0
        ypm = yc - h / 2 + h * (phm if phm < 1 else 2 - phm)
        # zig-zag trail
        pts = []
        tt = 0.0
        while tt <= t:
            k = tt / (Tb * g)
            kk = k % 2.0
            pts.append((xs + v * c_px * tt, yc - h / 2 + h * (kk if kk < 1 else 2 - kk)))
            tt += 0.05
        L.polyline(pts, P.cyan, w=1.0, a=0.3 * aa)
        L.radial(xm, ypm, 18 * s, P.cyan, a=0.9 * aa); L.circle(xm, ypm, 3.5 * s, (1, 1, 1), a=aa)
        ticks1 = int(t / (2 * Tb * g))
        T.label(L, "MOVING  v = 0.6 c", xm, yc - h / 2 - 28 * s, H, a=aa, color=P.cyan)
        T.value(L, f"ticks  {ticks1:2d}", xm, yc + h / 2 + 44 * s, H, a=aa, color=P.cyan)
    # ---------- rulers (lower band): length contraction
    yr = H * 0.80
    Lr = 420 * s
    def ruler(x, y, length, aa, col, n=10):
        L.line(x - length / 2, y, x + length / 2, y, col, w=2.5 * s, a=aa)
        for i in range(n + 1):
            xx = x - length / 2 + length * i / n
            hh = 14 * s if i % 5 == 0 else 7 * s
            L.line(xx, y, xx, y - hh, col, w=1.5 * s, a=aa)
    ruler(x0 + 60 * s, yr, Lr, a, P.ink)
    T.label(L, "AT REST   L", x0 + 60 * s, yr + 34 * s, H, a=a, color=P.amber)
    xr = W * 0.42 + v * c_px * 0.55 * t
    ar = a * smooth(ramp(t, 3.5, 4.3))
    if xr < W + Lr:
        ruler(xr, yr, Lr / g, ar, P.ink)
        T.label(L, f"MOVING   L / γ  =  {1/g:.2f} L", xr, yr + 34 * s, H, a=ar, color=P.cyan)
    # ---------- the factor
    e = smooth(ramp(t, 6.5, 7.5))
    T.equation(L, "γ = 1 / √(1 − v²/c²) = 1.25", W * 0.78, H * 0.60, H, a=e * 0.9, size=34)
    T.label(L, "MOVING CLOCK:  1 TICK TAKES 1.25 REST TICKS", W * 0.78, H * 0.655, H, a=e * 0.8, size=17)
    composite(f, L)
    return f
