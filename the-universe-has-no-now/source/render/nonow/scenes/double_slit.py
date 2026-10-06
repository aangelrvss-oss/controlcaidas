"""Two-slit interference: wave field (sum of two cylindrical waves) and single detections accumulating on a screen."""
import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    f = background(W, H, gradient=0.1)
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 0.8))
    # geometry (pixels): slits at x=xs, y = cy ± d/2; screen at x = xsc
    xs, cy = W * 0.28, H * 0.5; d = 110 * s; lam = 34 * s; xsc = W * 0.80
    key = ("slit_grid",)
    if key not in ctx.cache:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32); ctx.cache[key] = (x, y)
    x, y = ctx.cache[key]
    r1 = np.sqrt((x - xs) ** 2 + (y - cy - d / 2) ** 2) + 1e-3; r2 = np.sqrt((x - xs) ** 2 + (y - cy + d / 2) ** 2) + 1e-3
    k = 2 * math.pi / lam; om = 2 * math.pi * 1.2
    region = (x > xs) & (x < xsc)
    # amplitude falls as 1/sqrt(r); a slow front moves out from the slits
    front = np.clip((t * 260 * s - (np.minimum(r1, r2))) / (60 * s), 0, 1)
    psi = (np.cos(k * r1 - om * t) / np.sqrt(r1 / (40 * s)) + np.cos(k * r2 - om * t) / np.sqrt(r2 / (40 * s))) * 0.5
    inten = (np.cos(k * r1 - om * t) + np.cos(k * r2 - om * t))  # instantaneous field for the moving-wave look
    env = (psi ** 2) * front * region
    # time-averaged |psi|^2 pattern (stationary)  = 2 + 2 cos(k (r1-r2))  (per unit amplitude)
    pat = (1 + np.cos(k * (r1 - r2))) * 0.5
    field = (0.35 * np.clip(psi + 0.5, 0, 1.4) * front + 0.0) * region
    f += (field[..., None] * np.array([0.25, 0.5, 0.7], np.float32)) * a
    # source wave on the left
    src = np.clip(np.cos(k * (x - W * 0.08) - om * t), 0, 1) * (x < xs) * (x > W * 0.06) * 0.25
    f += src[..., None] * np.array([0.25, 0.5, 0.7], np.float32) * a
    # barrier with two slits
    L.rect(xs - 6 * s, 0, 12 * s, cy - d / 2 - 9 * s, P.ink, a=0.9 * a)
    L.rect(xs - 6 * s, cy - d / 2 + 9 * s, 12 * s, d - 18 * s, P.ink, a=0.9 * a)
    L.rect(xs - 6 * s, cy + d / 2 + 9 * s, 12 * s, H, P.ink, a=0.9 * a)
    # screen + detections accumulate from t=4
    L.line(xsc, H * 0.08, xsc, H * 0.92, P.dim, w=2.0, a=0.6 * a)
    rng = np.random.default_rng(42)
    n_det = int(max(0.0, t - 4.0) * 60)
    ys = np.linspace(H * 0.08, H * 0.92, 2000)
    r1s = np.sqrt((xsc - xs) ** 2 + (ys - cy - d / 2) ** 2); r2s = np.sqrt((xsc - xs) ** 2 + (ys - cy + d / 2) ** 2)
    prob = (1 + np.cos(k * (r1s - r2s))) * np.exp(-((ys - cy) / (H * 0.32)) ** 2)
    prob /= prob.sum()
    if n_det > 0:
        hits = rng.choice(ys, size=n_det, p=prob)
        xj = rng.uniform(-10, 10, n_det) * s
        f += splat_points(W, H, xsc + 14 * s + xj, hits, np.full(n_det, 1.6, np.float32), np.tile(np.array([0.6, 0.9, 1.0], np.float32), (n_det, 1)), size=1.5)
        # newest detection flashes
        L.radial(xsc + 14 * s + xj[-1], hits[-1], 16 * s, P.cyan, a=0.9)
    # predicted |psi|^2 curve on the right
    pa = smooth(ramp(t, 8.0, 9.0))
    pts = [(xsc + 40 * s + 130 * s * (prob[i] / prob.max()), ys[i]) for i in range(0, 2000, 10)]
    L.polyline(pts, P.amber, w=1.5, a=0.8 * pa)
    T.label(L, "|ψ|²  PREDICTED", xsc + 110 * s, H * 0.06, H, a=pa, color=P.amber, size=15)
    T.value(L, f"detections  {n_det:5d}", xsc - 10 * s, H * 0.96, H, a=a * smooth(ramp(t, 4.0, 4.5)), color=P.cyan, size=20, align="right")
    T.label(L, "ONE PARTICLE AT A TIME", W * 0.14, H * 0.90, H, a=a * smooth(ramp(t, 4.0, 5.0)), size=15)
    T.equation(L, "ψ = ψ₁ + ψ₂        P = |ψ₁ + ψ₂|²", W * 0.5, H * 0.09, H, a=a, size=30)
    composite(f, L)
    return f
