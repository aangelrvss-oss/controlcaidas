"""Two great theories, side by side; then pushed together until the seam tears."""
import math
from .common import *
from .gravity_grid import project, well

def gr_half(ctx, L, f, t, a, x0, x1, clash=0.0):
    W, H = ctx.W, ctx.H; s = S(ctx)
    import skia
    L.canvas.save(); L.canvas.clipRect(skia.Rect.MakeLTRB(x0, 0, x1, H))
    cx = (x0 + x1) / 2
    ext = 1.3; dense = np.linspace(-ext, ext, 70); g = np.linspace(-ext, ext, 19)
    yaw = 0.3 + 0.02 * t
    def proj(xs, ys, zs):
        sx, sy, d = project(ctx, xs, ys, zs, cam_yaw=yaw, dist=3.4, zoom=0.75)
        return sx - (W / 2 - cx), sy
    for gi in g:
        for xs, ys in ((dense, np.full_like(dense, gi)), (np.full_like(dense, gi), dense)):
            zs = well(xs, ys, 1.0)
            # clash: jitter the geometry near the seam
            if clash > 0:
                zs = zs + clash * 0.15 * np.sin(xs * 40 + t * 30) * np.exp(-((xs - 1.3) ** 2) * 3)
            sx, sy = proj(xs, ys, zs)
            L.polyline(list(zip(sx, sy)), P.amber, w=1.0, a=0.4 * a)
    # orbiting body
    th = t * 0.9
    ox, oy = 0.9 * math.cos(th), 0.75 * math.sin(th)
    sx, sy = proj(np.array([ox]), np.array([oy]), well(np.array([ox]), np.array([oy]), 1.0) + 0.02)
    L.radial(sx[0], sy[0], 14 * s, P.amber, a=0.9 * a); L.circle(sx[0], sy[0], 3.5 * s, (1, 1, 1), a=a)
    # gravitational-wave chirp waveform
    xs = np.linspace(0, 1, 300)
    chirp = np.sin(2 * math.pi * (6 * xs + 30 * xs ** 3) - t * 4) * (0.3 + 0.7 * xs ** 2) * np.where(xs < 0.92, 1, np.exp(-(xs - 0.92) * 40))
    pts = [(x0 + 60 * s + (x1 - x0 - 120 * s) * xs[i], H * 0.86 + chirp[i] * 28 * s) for i in range(300)]
    L.polyline(pts, P.amber, w=1.4, a=0.8 * a)
    T.label(L, "GW150914  ·  LIGO, 2015", cx, H * 0.93, H, a=a * 0.8, color=P.amber, size=13)
    L.canvas.restore()

def qft_half(ctx, L, f, t, a, x0, x1, clash=0.0):
    W, H = ctx.W, ctx.H; s = S(ctx)
    import skia
    L.canvas.save(); L.canvas.clipRect(skia.Rect.MakeLTRB(x0, 0, x1, H))
    cx = (x0 + x1) / 2
    # a field: lattice of oscillators with two localized excitations ("particles") travelling
    nx, ny = 34, 20
    xs = np.linspace(x0 + 40 * s, x1 - 40 * s, nx); ys = np.linspace(H * 0.30, H * 0.72, ny)
    X, Y = np.meshgrid(xs, ys)
    def packet(px, py, k, w):
        d2 = (X - px) ** 2 + (Y - py) ** 2
        return np.exp(-d2 / (2 * (w * s) ** 2)) * np.cos(k * (X - px) / s - t * 6)
    px1 = x0 + 100 * s + ((t * 70 * s) % (x1 - x0 - 200 * s)); px2 = x1 - 100 * s - ((t * 45 * s + 200) % (x1 - x0 - 200 * s))
    Z = packet(px1, H * 0.46, 0.25, 70) * 1.0 + packet(px2, H * 0.58, 0.2, 60) * 0.8
    Z += 0.08 * np.sin(X / (30 * s) + t * 3) * np.sin(Y / (25 * s) - t * 2)   # vacuum jitter
    if clash > 0:
        Z += clash * 0.6 * np.random.default_rng(int(t * 24)).standard_normal(Z.shape) * np.exp(-((X - x0) / (160 * s)) ** 2)
    for j in range(ny):
        pts = [(X[j, i], Y[j, i] - Z[j, i] * 26 * s) for i in range(nx)]
        L.polyline(pts, P.cyan, w=1.0, a=0.45 * a)
    for i in range(nx):
        pts = [(X[j, i], Y[j, i] - Z[j, i] * 26 * s) for j in range(ny)]
        L.polyline(pts, P.cyan, w=1.0, a=0.25 * a)
    # excitation markers
    for px, py in ((px1, H * 0.46), (px2, H * 0.58)):
        L.radial(px, py - 30 * s, 24 * s, P.cyan, a=0.5 * a)
    T.label(L, "PARTICLE = EXCITATION OF A FIELD", cx, H * 0.80, H, a=a * 0.8, color=P.cyan, size=13)
    # g-factor digits
    dig = "2.00231930436"
    n = int(min(len(dig), 1 + t * 1.6))
    T.value(L, f"electron g-factor  {dig[:n]}", cx, H * 0.88, H, a=a, color=P.cyan, size=22)
    T.label(L, "THEORY AND EXPERIMENT AGREE TO 12 DIGITS", cx, H * 0.93, H, a=a * smooth(ramp(t, 7.0, 8.0)) * 0.8, color=P.cyan, size=13)
    L.canvas.restore()

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    phase = p.get("phase", "gr")
    f = background(W, H, gradient=0.1)
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 0.8))
    if phase == "gr":
        gr_half(ctx, L, f, t, a, 0, W)
        T.act_label(L, "GENERAL RELATIVITY", W / 2, H * 0.12, H, a=a)
        T.quote(L, ["gravity is the geometry of spacetime"], W / 2, H * 0.18, H, a=a * smooth(ramp(t, 1.0, 2.0)), size=28)
    elif phase == "qft":
        qft_half(ctx, L, f, t, a, 0, W)
        T.act_label(L, "QUANTUM FIELD THEORY", W / 2, H * 0.12, H, a=a)
        T.quote(L, ["particles are excitations of fields"], W / 2, H * 0.18, H, a=a * smooth(ramp(t, 1.0, 2.0)), size=28)
    else:
        clash = 0.0 if phase == "both" else smooth(ramp(t, 3.0, 9.0))
        seam = W / 2
        gr_half(ctx, L, f, t, a, 0, seam, clash)
        qft_half(ctx, L, f, t, a, seam, W, clash)
        L.line(seam, H * 0.08, seam, H * 0.92, P.dim, w=1.0, a=0.5 * a)
        T.act_label(L, "GENERAL RELATIVITY", W * 0.25, H * 0.12, H, a=a)
        T.act_label(L, "QUANTUM FIELD THEORY", W * 0.75, H * 0.12, H, a=a)
        if phase == "both":
            q = smooth(ramp(t, 5.0, 6.0))
            T.quote(L, ["smooth, dynamic stage"], W * 0.25, H * 0.19, H, a=q, size=24, color=P.amber)
            T.quote(L, ["fixed stage, uncertain actors"], W * 0.75, H * 0.19, H, a=q, size=24, color=P.cyan)
        else:
            # infinities at the seam
            q = clash
            if q > 0:
                rng = np.random.default_rng(int(t * 24))
                for k in range(int(40 * q)):
                    yy = rng.uniform(H * 0.25, H * 0.80); ww = rng.uniform(10, 90) * s * q
                    L.line(seam - ww, yy, seam + ww, yy, P.red, w=1.0, a=0.5 * q)
                T.label(L, "∞", seam, H * 0.50, H, a=q, color=P.red, size=60, face="Display-Light")
                T.label(L, "NON-RENORMALISABLE", seam, H * 0.58, H, a=q * smooth(ramp(t, 6.0, 7.0)), color=P.red, size=16)
            q2 = smooth(ramp(t, 9.5, 10.5))
            T.quote(L, ["centre of a black hole   ·   first instant of the universe"], W / 2, H * 0.19, H, a=q2, size=24, color=P.dim)
    composite(f, L)
    return f
