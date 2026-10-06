"""Spacetime as geometry: a flat grid bends into a well; a body follows a geodesic; the field equations."""
import math
from .common import *

def project(ctx, X, Y, Z, cam_pitch=0.62, cam_yaw=0.0, dist=3.2, zoom=1.0):
    """Perspective projection of world points (X right, Y depth, Z up) -> screen."""
    W, H = ctx.W, ctx.H
    cy_, sy_ = math.cos(cam_yaw), math.sin(cam_yaw)
    x1 = X * cy_ - Y * sy_; y1 = X * sy_ + Y * cy_
    cp, sp = math.cos(cam_pitch), math.sin(cam_pitch)
    y2 = y1 * cp - Z * sp; z2 = y1 * sp + Z * cp      # rotate about X axis
    d = y2 + dist
    f = 0.95 * H * zoom
    sx = W / 2 + x1 * f / d; sy = H * 0.52 - z2 * f / d
    return sx, sy, d

def well(X, Y, M, soft=0.30):
    r = np.sqrt(X * X + Y * Y)
    return -M / np.sqrt(r * r + soft * soft) * 0.30

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    phase = p.get("phase", "flat_to_curved")
    f = background(W, H, gradient=0.12)
    f += starfield2d(ctx, t, gain=0.25, fov=80, drift=(0.0015, 0)) * 0.5
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 0.8))
    M = 1.0 if phase != "flat_to_curved" else 1.0 * smooth(ramp(t, 2.5, 6.0))
    yaw = 0.25 + 0.03 * t
    n = 26; ext = 1.6
    g = np.linspace(-ext, ext, n)
    # grid lines along X and Y with the well deformation
    def draw_line(xs, ys, col, aa, w=1.0):
        zs = well(xs, ys, M)
        sx, sy, d = project(ctx, xs, ys, zs, cam_yaw=yaw)
        pts = list(zip(sx, sy))
        depth_fade = np.clip((5.0 - d) / 3.0, 0.15, 1.0)
        for k in range(len(pts) - 1):
            L.line(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], col, w=w, a=aa * float(depth_fade[k]))
    dense = np.linspace(-ext, ext, 90)
    for gi in g:
        draw_line(dense, np.full_like(dense, gi), P.amber if abs(gi) < 1e-6 else P.dim, 0.55 * a)
        draw_line(np.full_like(dense, gi), dense, P.amber if abs(gi) < 1e-6 else P.dim, 0.55 * a)
    # the mass
    if M > 0.01:
        sx, sy, d = project(ctx, np.array([0.0]), np.array([0.0]), np.array([well(0.0, 0.0, M) + 0.05]), cam_yaw=yaw)
        L.radial(sx[0], sy[0], 60 * s * M, P.amber, a=0.8 * a); L.circle(sx[0], sy[0], 11 * s * M, (1, 0.95, 0.85), a=a)
    if phase == "flat_to_curved":
        T.label(L, "FLAT SPACETIME" if M < 0.05 else "CURVED BY MASS", W / 2, H * 0.12, H, a=a, color=P.amber)
    if phase == "equation":
        e = smooth(ramp(t, 0.3, 1.2))
        T.equation(L, "Gμν + Λgμν  =  (8πG / c⁴) Tμν", W / 2, H * 0.17, H, a=e, size=50)
        T.label(L, "GEOMETRY OF SPACETIME", W * 0.36, H * 0.235, H, a=e * smooth(ramp(t, 1.2, 2.0)), color=P.amber)
        T.label(L, "MASS AND ENERGY", W * 0.70, H * 0.235, H, a=e * smooth(ramp(t, 2.6, 3.4)), color=P.cyan)
        L.line(W * 0.27, H * 0.205, W * 0.455, H * 0.205, P.amber, w=1.2, a=e * smooth(ramp(t, 1.2, 2.0)) * 0.7)
        L.line(W * 0.60, H * 0.205, W * 0.80, H * 0.205, P.cyan, w=1.2, a=e * smooth(ramp(t, 2.6, 3.4)) * 0.7)
        T.caption(L, "Einstein, 1915", W / 2, H * 0.27, H, a=e * 0.8, align="center", size=20)
    if phase in ("orbit", "equation"):
        # a small body on an eccentric orbit (Newtonian ellipse as the weak-field geodesic) drawn on the surface
        ecc = 0.35; aa_ = 1.05; per = 7.0
        def pos(tt):
            Mn = 2 * math.pi * tt / per
            E = Mn
            for _ in range(8): E = E - (E - ecc * math.sin(E) - Mn) / (1 - ecc * math.cos(E))
            x = aa_ * (math.cos(E) - ecc); y = aa_ * math.sqrt(1 - ecc * ecc) * math.sin(E)
            return x, y
        trail = [pos(t - k * 0.08) for k in range(60)]
        xs = np.array([q[0] for q in trail]); ys = np.array([q[1] for q in trail])
        sx, sy, d = project(ctx, xs, ys, well(xs, ys, M) + 0.02, cam_yaw=yaw)
        for k in range(len(trail) - 1):
            L.line(sx[k], sy[k], sx[k + 1], sy[k + 1], P.cyan, w=2.0, a=a * (1 - k / 60) * 0.9)
        L.radial(sx[0], sy[0], 16 * s, P.cyan, a=0.9 * a); L.circle(sx[0], sy[0], 4 * s, (1, 1, 1), a=a)
        if phase == "orbit":
            # the same path lifted off the surface: an ellipse (what we call an orbit)
            lift = smooth(ramp(t, 3.0, 5.0))
            th = np.linspace(0, 2 * math.pi, 120)
            ex = aa_ * (np.cos(th) - ecc); ey = aa_ * math.sqrt(1 - ecc * ecc) * np.sin(th)
            sx2, sy2, d2 = project(ctx, ex, ey, well(ex, ey, M) * (1 - lift) + 0.45 * lift, cam_yaw=yaw)
            L.polyline(list(zip(sx2, sy2)), P.cyan, w=1.2, a=0.5 * a * lift)
            T.label(L, "A STRAIGHT PATH THROUGH CURVED GEOMETRY", W / 2, H * 0.12, H, a=a, color=P.cyan)
            T.label(L, "= AN ORBIT", W / 2, H * 0.16, H, a=a * lift, color=P.cyan)
    composite(f, L)
    return f
