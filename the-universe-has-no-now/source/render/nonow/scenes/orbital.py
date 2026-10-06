"""Hydrogen orbitals as sampled probability clouds (|psi|^2 of the analytic eigenfunctions), not planets."""
import math
from .common import *

def sample_orbital(n, l, m, N, rng):
    """Rejection-sample |psi_nlm|^2 (real orbitals: 1s, 2p_z, 3d_z2) in Bohr radii."""
    # analytic radial parts (a0 = 1)
    def R(r):
        if (n, l) == (1, 0): return 2 * np.exp(-r)
        if (n, l) == (2, 1): return (1 / (2 * math.sqrt(6))) * r * np.exp(-r / 2)
        if (n, l) == (3, 2): return (4 / (81 * math.sqrt(30))) * r * r * np.exp(-r / 3)
        if (n, l) == (2, 0): return (1 / (2 * math.sqrt(2))) * (2 - r) * np.exp(-r / 2)
    def Y(th, ph):
        if l == 0: return np.full_like(th, 0.2821)
        if (l, m) == (1, 0): return 0.4886 * np.cos(th)
        if (l, m) == (2, 0): return 0.3154 * (3 * np.cos(th) ** 2 - 1)
        if (l, m) == (2, 2): return 0.5462 * np.sin(th) ** 2 * np.cos(2 * ph)
    pts = []
    rmax = {1: 6.0, 2: 14.0, 3: 24.0}[n]
    pmax = {(1, 0, 0): 4 * 0.2821 ** 2 * 1.05, (2, 1, 0): 0.006, (3, 2, 0): 0.0009, (2, 0, 0): 0.5, (3, 2, 2): 0.0009}[(n, l, m)]
    while sum(len(p) for p in pts) < N:
        x = rng.uniform(-rmax, rmax, (N * 2, 3))
        r = np.linalg.norm(x, axis=1) + 1e-9
        th = np.arccos(np.clip(x[:, 2] / r, -1, 1)); ph = np.arctan2(x[:, 1], x[:, 0])
        p = (R(r) * Y(th, ph)) ** 2 * r ** 0  # density per unit volume
        keep = rng.uniform(0, pmax, len(p)) < p
        pts.append(x[keep])
    return np.concatenate(pts)[:N].astype(np.float32)

ORBS = [((1, 0, 0), "1s"), ((2, 1, 0), "2p"), ((3, 2, 0), "3d")]

def cloud(ctx, key):
    k = ("orb", key)
    if k not in ctx.cache:
        ctx.cache[k] = sample_orbital(*key, 40000, np.random.default_rng(sum(key) + 7))
    return ctx.cache[k]

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    phase = p.get("phase", "not_planet")
    f = background(W, H, gradient=0.12)
    L = Layer(W, H)
    cx, cy = W / 2, H * 0.52
    a = smooth(ramp(t, 0.0, 0.8))
    if phase == "not_planet":
        # the wrong picture: a planetary atom, drawn then struck out
        pa = fade(t, 0.0, 0.8, 2.2, 3.6)
        L.circle(cx, cy, 10 * s, P.amber, a=pa)
        for k, (rx, ry, rot) in enumerate(((150, 60, 0.3), (150, 60, 1.35), (150, 60, 2.4))):
            pts = []
            for i in range(121):
                th = 2 * math.pi * i / 120
                x, y = rx * s * math.cos(th), ry * s * math.sin(th)
                pts.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
            L.polyline(pts, P.dim, w=1.2, a=0.7 * pa, close=True)
            th = t * 2.5 + k * 2
            x, y = rx * s * math.cos(th), ry * s * math.sin(th)
            L.circle(cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot), 5 * s, P.cyan, a=pa)
        xa = smooth(ramp(t, 2.0, 2.6)) * pa
        L.line(cx - 190 * s, cy - 110 * s, cx - 190 * s + 380 * s * xa, cy - 110 * s + 220 * s * xa, P.red, w=3 * s, a=0.9)
        T.label(L, "NOT THIS", cx, cy + 150 * s, H, a=xa, color=P.red)
        # the cloud fades in
        ca = smooth(ramp(t, 3.4, 5.0))
        if ca > 0:
            pts = cloud(ctx, (1, 0, 0))
            R = 120 * s
            ang = t * 0.2
            x = pts[:, 0] * math.cos(ang) + pts[:, 2] * math.sin(ang)
            f += splat_points(W, H, cx + x * R, cy + pts[:, 1] * R, np.full(len(pts), 0.22 * ca, np.float32),
                              np.tile(np.array([0.5, 0.85, 1.0], np.float32), (len(pts), 1)), size=1.5)
            T.label(L, "|ψ|²   WHERE THE ELECTRON IS LIKELY TO BE FOUND", cx, cy + 150 * s, H, a=ca, color=P.cyan)
            T.equation(L, "iħ ∂ψ/∂t = Ĥψ", W * 0.82, H * 0.86, H, a=ca * 0.9, size=34)
            T.caption(L, "Schrödinger, 1926", W * 0.82, H * 0.905, H, a=ca * 0.7, align="center", size=18)
    else:
        # morph through 1s -> 2p -> 3d with cross-fades; show the nodal plane
        seq = [(0.0, 3.0), (3.0, 6.5), (6.5, 20.0)]
        for k, (t0, t1) in enumerate(seq):
            w = fade(t, t0 - 0.6, t0 + 0.6, t1 - 0.6, t1 + 0.6) if k > 0 else fade(t, -1, 0, t1 - 0.6, t1 + 0.6)
            if w <= 0: continue
            key, name = ORBS[k]
            pts = cloud(ctx, key)
            R = {1: 130, 2: 46, 3: 24}[key[0]] * s
            ang = t * 0.25
            x = pts[:, 0] * math.cos(ang) - pts[:, 1] * math.sin(ang)
            # colour by sign of the angular part (phase) for p and d: cyan vs amber lobes
            if key[1] == 1: sign = np.sign(pts[:, 2])
            elif key[1] == 2: sign = np.sign(3 * (pts[:, 2] ** 2) - np.sum(pts ** 2, 1))
            else: sign = np.ones(len(pts))
            col = np.where(sign[:, None] > 0, np.array([0.5, 0.85, 1.0], np.float32), np.array([0.96, 0.7, 0.34], np.float32))
            f += splat_points(W, H, cx + x * R, cy - pts[:, 2] * R, np.full(len(pts), 0.20 * w, np.float32), col, size=1.5)
            T.label(L, name.upper() + "  ORBITAL", W * 0.5, H * 0.12, H, a=w)
            if key[1] > 0:
                T.label(L, "NODAL SURFACE  ·  PROBABILITY ZERO", W * 0.5, H * 0.90, H, a=w * 0.8, color=P.amber, size=16)
                if key[1] == 1: L.line(cx - 220 * s, cy, cx + 220 * s, cy, P.amber, w=1.0, a=0.35 * w)
        T.label(L, "PHASE  +", W * 0.82, H * 0.80, H, a=a, color=P.cyan, size=16, align="left")
        T.label(L, "PHASE  −", W * 0.82, H * 0.84, H, a=a, color=P.amber, size=16, align="left")
    L.radial(cx, cy, 8 * s, P.amber, a=0.8 * a); L.circle(cx, cy, 2.2 * s, (1, 1, 1), a=a)
    composite(f, L)
    return f
