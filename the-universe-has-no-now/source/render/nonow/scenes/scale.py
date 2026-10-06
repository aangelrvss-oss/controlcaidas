"""Scale journey: atom -> human -> Earth -> Solar System -> galaxy -> observable universe.
Each stage is a self-contained composition that zooms out slowly; stages dissolve into each other.
Also used (in reverse) by final_zoom."""
import math
from .common import *

def _pulse_dot(L, x, y, s, a=1.0, r=18):
    L.radial(x, y, r * s, P.cyan, a=0.9 * a); L.circle(x, y, 3.2 * s, (1, 1, 1), a=a)

LABELS = True
def stage_title(L, W, H, s, name, size_txt, a):
    if not LABELS: return
    T.label(L, name, 70 * s, 90 * s, H, a=a, align="left", color=P.ink, size=22)
    T.caption(L, size_txt, 70 * s, 124 * s, H, a=a * 0.85, size=20)

def readout(L, W, H, s, txt, a, color=P.cyan):
    if not LABELS: return
    T.value(L, txt, W / 2, H * 0.88, H, a=a, color=color, size=30)

# ---------------------------------------------------------------- stages
def atom(ctx, t, zoom, a, L, f):
    W, H = ctx.W, ctx.H; s = S(ctx) * zoom
    cx, cy = W / 2, H * 0.5
    key = ("atom_cloud",)
    if key not in ctx.cache:
        rng = np.random.default_rng(5)
        n = 30000
        r = rng.exponential(1.0, n) ** 1.0 * 0.5  # 1s density ~ r^2 e^{-2r}: sample radius via gamma(3, 0.5)
        r = rng.gamma(3.0, 0.5, n)
        v = rng.standard_normal((n, 3)); v /= np.linalg.norm(v, axis=1, keepdims=True)
        ctx.cache[key] = (v * r[:, None]).astype(np.float32)
    pts = ctx.cache[key]
    R = 150 * s  # Bohr radius in px
    ang = t * 0.15
    x = pts[:, 0] * math.cos(ang) + pts[:, 2] * math.sin(ang)
    px = cx + x * R; py = cy + pts[:, 1] * R
    f += splat_points(W, H, px, py, np.full(len(px), 0.11 * a, np.float32), np.tile(np.array([0.5, 0.85, 1.0], np.float32), (len(px), 1)), size=1.4)
    L.radial(cx, cy, 10 * s, P.amber, a=0.9 * a); L.circle(cx, cy, 2.5 * s, (1, 1, 1), a=a)
    # scale bar: 1 angstrom ~ 2 Bohr radii
    L.line(cx - R, H * 0.72, cx + R, H * 0.72, P.dim, w=1.0, a=0.5 * a)
    T.label(L, "1 × 10⁻¹⁰ m", cx, H * 0.72 + 28 * S(ctx), H, a=0.8 * a)
    # the pulse crosses the atom
    tp = ramp(t, 1.2, 3.4)
    if 0 < tp < 1:
        _pulse_dot(L, cx - R + 2 * R * tp, cy, S(ctx), a)
        L.line(cx - R, cy, cx - R + 2 * R * tp, cy, P.cyan, w=1.2, a=0.5 * a)
    stage_title(L, W, H, S(ctx), "A HYDROGEN ATOM", "diameter ≈ 10⁻¹⁰ m", a)
    readout(L, W, H, S(ctx), "light crossing time ≈ 3 × 10⁻¹⁹ s", a * smooth(ramp(t, 3.4, 4.2)))

def human(ctx, t, zoom, a, L, f):
    W, H = ctx.W, ctx.H; s = S(ctx) * zoom
    cx, base = W / 2, H * 0.5 + 300 * s
    L.radial(cx, base - 300 * s, 420 * s, P.amber, a=0.16 * a)
    silhouette_figure(L, cx, base, 600 * s, color=(0.01, 0.01, 0.015), a=a, t=t, look_up=0.5)
    tp = ramp(t, 1.0, 3.0)
    if 0 < tp < 1:
        y = base - 600 * s + 600 * s * tp
        _pulse_dot(L, cx + 120 * s, y, S(ctx), a)
        L.line(cx + 120 * s, base - 600 * s, cx + 120 * s, y, P.cyan, w=1.2, a=0.5 * a)
    L.line(cx + 190 * s, base - 600 * s, cx + 190 * s, base, P.dim, w=1.0, a=0.5 * a)
    T.label(L, "1.8 m", cx + 230 * s, base - 300 * s, H, a=0.8 * a, align="left")
    stage_title(L, W, H, S(ctx), "A HUMAN BODY", "height ≈ 1.8 m", a)
    readout(L, W, H, S(ctx), "light crossing time ≈ 6 × 10⁻⁹ s", a * smooth(ramp(t, 3.0, 3.8)))

def earth(ctx, t, zoom, a, L, f, slow=20.0):
    W, H = ctx.W, ctx.H; s = S(ctx) * zoom
    cx, cy, r = W / 2, H * 0.5, 280 * s
    rgb, al = earth_disc(ctx, cx, cy, r, light_dir=(-0.6, -0.3), t=0.0)
    over(f, rgb * a, al * a)
    # pulse circling the equator in a tilted circle (shown slowed down)
    laps_per_s = 7.48 / slow
    th = 2 * math.pi * laps_per_s * t - math.pi / 2
    inc = math.radians(62)
    trail = []
    for k in range(60):
        tt = th - k * 0.03
        x, y, z = math.cos(tt), math.sin(tt) * math.cos(inc), math.sin(tt) * math.sin(inc)
        trail.append((cx + x * r * 1.02, cy + y * r * 1.02, z))
    for k in range(len(trail) - 1):
        if trail[k][2] > -0.15:
            L.line(trail[k][0], trail[k][1], trail[k + 1][0], trail[k + 1][1], P.cyan, w=2.0, a=a * (1 - k / 60) * 0.9)
    if trail[0][2] > -0.15: _pulse_dot(L, trail[0][0], trail[0][1], S(ctx), a)
    stage_title(L, W, H, S(ctx), "THE EARTH", "circumference ≈ 40 075 km   ·   shown 20× slower", a)
    readout(L, W, H, S(ctx), f"0.134 s per lap   ·   {laps_per_s*slow:.1f} laps every second", a * smooth(ramp(t, 1.5, 2.3)))

SOLAR = [("MOON", 1.28, "1.3 s", 1.0), ("SUN", 499.0, "8.3 min", 1.0), ("NEPTUNE", 4.1 * 3600, "4.1 h", 1.0), ("VOYAGER 1", 23.0 * 3600, "≈ 23 h", 1.0)]
def solar(ctx, t, zoom, a, L, f):
    W, H = ctx.W, ctx.H; s = S(ctx) * zoom
    cx, cy = W / 2, H * 0.52
    # log-scale rings: r = k * log10(seconds / 0.3)
    def rad(sec): return (90 + 115 * math.log10(sec / 0.3)) * s
    rgb, al = earth_disc(ctx, cx, cy, 40 * s, light_dir=(-0.6, -0.3), t=0.0)
    over(f, rgb * a, al * a)
    for name, sec, lab, _ in SOLAR:
        R = rad(sec)
        L.circle(cx, cy, R, P.dim, w=1.0, a=0.28 * a)
        ang = math.radians(-35)
        px, py = cx + R * math.cos(ang), cy + R * math.sin(ang)
        if name == "SUN":
            L.radial(px, py, 40 * s, P.amber, a=0.8 * a); L.circle(px, py, 9 * s, (1, 1, 0.9), a=a)
        elif name == "MOON":
            L.circle(px, py, 5 * s, P.dim, a=a)
        elif name == "NEPTUNE":
            L.circle(px, py, 6 * s, P.blue, a=a)
        else:
            L.line(px - 6 * s, py, px + 6 * s, py, P.ink, w=1.5, a=a); L.line(px, py - 6 * s, px, py + 6 * s, P.ink, w=1.5, a=a)
    # expanding wavefront in log space
    tw = ramp(t, 0.8, 12.0)
    Rw = rad(0.3) + (rad(23 * 3600) - rad(0.3)) * tw
    L.circle(cx, cy, Rw, P.cyan, w=2.2 * s, a=0.9 * a)
    L.radial(cx, cy, Rw, P.cyan, a=0.06 * a)
    for name, sec, lab, _ in SOLAR:
        R = rad(sec)
        if Rw >= R:
            la = smooth(ramp(Rw - R, 0, 20 * s))
            ang = math.radians(-35)
            px, py = cx + R * math.cos(ang), cy + R * math.sin(ang)
            T.label(L, name, px + 16 * s, py - 14 * s, H, a=la * a, align="left", color=P.ink)
            T.value(L, lab, px + 16 * s, py + 16 * s, H, a=la * a, align="left", color=P.cyan, size=22)
    stage_title(L, W, H, S(ctx), "THE SOLAR SYSTEM", "distances on a logarithmic scale", a)

def galaxy_points(ctx):
    key = ("galaxy",)
    if key not in ctx.cache:
        rng = np.random.default_rng(9); n = 90000
        arm = rng.integers(0, 2, n); rr = rng.gamma(2.0, 0.22, n)
        th = 1.0 * np.log(rr / 0.05 + 1) * 3.2 + arm * math.pi + rng.standard_normal(n) * (0.25 + 0.5 * rr)
        x = rr * np.cos(th); y = rr * np.sin(th); z = rng.standard_normal(n) * 0.012 * (1 + 0.5 * rr)
        bulge = rng.standard_normal((n // 6, 3)) * [0.06, 0.06, 0.035]
        pts = np.concatenate([np.stack([x, y, z], 1), bulge], 0).astype(np.float32)
        col = np.ones((len(pts), 3), np.float32)
        col[: n] = [0.75, 0.82, 1.0]; col[n:] = [1.0, 0.85, 0.65]
        # HII knots
        knots = rng.random(n) < 0.03
        col[:n][knots] = [1.0, 0.5, 0.6]
        ctx.cache[key] = (pts, col)
    return ctx.cache[key]

def galaxy(ctx, t, zoom, a, L, f, tilt=0.55):
    W, H = ctx.W, ctx.H; s = S(ctx) * zoom
    cx, cy = W / 2, H * 0.5
    pts, col = galaxy_points(ctx)
    R = 680 * s
    ang = t * 0.01
    x = pts[:, 0] * math.cos(ang) - pts[:, 1] * math.sin(ang); y = pts[:, 0] * math.sin(ang) + pts[:, 1] * math.cos(ang)
    px = cx + x * R; py = cy + (y * math.cos(tilt) + pts[:, 2] * math.sin(tilt)) * R
    f += splat_points(W, H, px, py, np.full(len(px), 0.055 * a, np.float32), col, size=1.2)
    f += splat_points(W, H, np.array([cx]), np.array([cy]), np.array([3.0 * a]), np.array([[1.0, 0.9, 0.7]]), size=12)
    # the Sun: 2/3 out on one arm
    rs_ = 0.32; ths = math.log(rs_ / 0.05 + 1) * 3.2 + math.pi + ang
    sx, sy = cx + rs_ * R * math.cos(ths), cy + rs_ * R * math.sin(ths) * math.cos(tilt)
    L.circle(sx, sy, 3 * s, (1, 1, 1), a=a)
    T.label(L, "SUN", sx + 12 * s, sy - 10 * s, H, a=0.9 * a, align="left", size=16)
    # expanding wavefront (log scale from 1 light-year to 100 000)
    tw = ramp(t, 0.8, 11.5)
    def rad(ly): return (8 + 90 * math.log10(ly)) * s * 1.05
    Rw = rad(1.0) + (rad(1.2e5) - rad(1.0)) * tw
    L.circle(sx, sy, Rw, P.cyan, w=2.0 * s, a=0.85 * a)
    for name, ly, lab in (("PROXIMA CENTAURI", 4.24, "4.2 years"), ("GALACTIC CENTRE", 26000, "26 000 years"), ("ACROSS THE GALAXY", 1.0e5, "100 000 years")):
        R0 = rad(ly)
        if Rw >= R0:
            la = smooth(ramp(Rw - R0, 0, 20 * s)) * a
            ang2 = math.radians(-50)
            px, py = sx + R0 * math.cos(ang2), sy + R0 * math.sin(ang2)
            L.circle(sx, sy, R0, P.dim, w=1.0, a=0.3 * la)
            T.label(L, name, px + 12 * s, py - 10 * s, H, a=la, align="left", size=16)
            T.value(L, lab, px + 12 * s, py + 16 * s, H, a=la, align="left", color=P.cyan, size=20)
    stage_title(L, W, H, S(ctx), "THE MILKY WAY", "≈ 100 000 light-years across   ·   logarithmic scale", a)

def web_points(ctx):
    key = ("web",)
    if key not in ctx.cache:
        rng = np.random.default_rng(21)
        nodes = rng.standard_normal((160, 3)) * 0.8
        pts = []
        # filaments between nearby nodes + halos at nodes
        for i in range(len(nodes)):
            d = np.linalg.norm(nodes - nodes[i], axis=1); nb = np.argsort(d)[1:4]
            for j in nb:
                k = 160
                u = rng.random(k)[:, None]
                seg = nodes[i] * (1 - u) + nodes[j] * u + rng.standard_normal((k, 3)) * 0.02
                pts.append(seg)
            pts.append(nodes[i] + rng.standard_normal((400, 3)) * 0.05)
        pts = np.concatenate(pts).astype(np.float32)
        ctx.cache[key] = pts
    return ctx.cache[key]

def universe(ctx, t, zoom, a, L, f, figure=True):
    W, H = ctx.W, ctx.H; s = S(ctx) * zoom
    cx, cy = W / 2, H * 0.48
    pts = web_points(ctx)
    ang = t * 0.02
    x = pts[:, 0] * math.cos(ang) + pts[:, 2] * math.sin(ang); z = -pts[:, 0] * math.sin(ang) + pts[:, 2] * math.cos(ang)
    depth = 1 / (2.6 + z)
    R = 900 * s
    px = cx + x * R * depth * 1.8; py = cy + pts[:, 1] * R * depth * 1.8
    b = (0.06 * a * depth * 2.6).astype(np.float32)
    col = np.tile(np.array([0.85, 0.8, 1.0], np.float32), (len(px), 1))
    f += splat_points(W, H, px, py, b, col, size=1.0)
    L.circle(cx, cy, 3 * s, (1, 1, 1), a=a)
    T.label(L, "MILKY WAY", cx + 12 * s, cy - 10 * s, H, a=0.8 * a, align="left", size=16)
    tw = ramp(t, 0.5, 5.5)
    Rw = 20 * s + (560 * s) * tw
    L.circle(cx, cy, Rw, P.cyan, w=1.6 * s, a=0.7 * a)
    layers = (("ANDROMEDA", 0.18, "2.5 million years"), ("GN-z11", 0.62, "13.4 billion years"), ("OLDEST LIGHT  (CMB)", 0.95, "13.8 billion years"))
    for name, frac, lab in layers:
        R0 = 20 * s + 560 * s * frac
        if Rw >= R0:
            la = smooth(ramp(Rw - R0, 0, 20 * s)) * a
            ang2 = math.radians(-40)
            px_, py_ = cx + R0 * math.cos(ang2), cy + R0 * math.sin(ang2)
            L.circle(cx, cy, R0, P.dim, w=1.0, a=0.3 * la)
            T.label(L, name, px_ + 12 * s, py_ - 10 * s, H, a=la, align="left", size=16)
            T.value(L, lab, px_ + 12 * s, py_ + 16 * s, H, a=la, align="left", color=P.cyan, size=20)
    stage_title(L, W, H, S(ctx), "THE OBSERVABLE UNIVERSE", "every direction is a different past", a)
    if figure:
        # HUMAN MOMENT: a figure before a screen, waiting for a signal that is years away
        fx, fy = W * 0.16, H * 0.93
        L.radial(fx, fy - 160 * S(ctx), 260 * S(ctx), P.cyan, a=0.10 * a)
        silhouette_figure(L, fx, fy, 330 * S(ctx), color=(0.01, 0.01, 0.015), a=a, t=t)
        T.label(L, "SIGNAL ARRIVAL", fx + 150 * S(ctx), fy - 250 * S(ctx), H, a=0.8 * a, align="left", size=14)
        blink = 0.6 + 0.4 * math.sin(t * 4)
        T.value(L, "in 4.24 years", fx + 150 * S(ctx), fy - 222 * S(ctx), H, a=0.9 * a, align="left", color=P.cyan, size=20)
        L.circle(fx + 136 * S(ctx), fy - 229 * S(ctx), 3 * S(ctx), P.cyan, a=a * blink)

STAGES = dict(atom=atom, human=human, earth=earth, solar=solar, galaxy=galaxy, universe=universe)

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H
    stage = p["stage"]
    f = background(W, H, gradient=0.15)
    if stage in ("earth", "solar", "galaxy", "universe"):
        f += starfield2d(ctx, t, gain=0.35 if stage != "universe" else 0.15, fov=75, drift=(0.002, 0)) * 0.7
    L = Layer(W, H)
    zoom = 1.0 + 0.35 * (1 - ease_out(ramp(t, 0, dur)))   # slow zoom-out across the stage
    a = smooth(ramp(t, 0.0, 0.6))
    STAGES[stage](ctx, t, zoom, a, L, f)
    composite(f, L)
    return f
