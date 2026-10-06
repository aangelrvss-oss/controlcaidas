import math, numpy as np
from ..core import P, Layer, background, composite, add_layer, Stars, smooth, ramp, fade, lerp, ease_out, ease_in, ease_in_out, clamp01, silhouette_figure, splat_points
from .. import text as T

def S(ctx): return ctx.H / 1080.0

def draw_clock(L, cx, cy, r, sec, color=P.ink, accent=P.amber, a=1.0, w=None, ticks=True, hand=True, glow=True, label=None, H=1080, minute=True):
    """Elegant analog clock: thin ring, 60 ticks, hour marks, sweeping second hand (sec in seconds)."""
    w = w or max(1.2, r * 0.012)
    if glow:
        L.radial(cx, cy, r * 1.6, accent, a=0.10 * a)
    L.circle(cx, cy, r, color, w=w, a=a)
    if ticks:
        for i in range(60):
            ang = math.radians(i * 6 - 90)
            long = i % 5 == 0
            r0 = r * (0.86 if long else 0.93); r1 = r * 0.975
            L.line(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang), cx + r1 * math.cos(ang), cy + r1 * math.sin(ang),
                   color, w=w * (1.3 if long else 0.8), a=a * (0.9 if long else 0.45))
    if hand:
        if minute:
            ang = math.radians((sec / 60.0) * 6 - 90)
            L.line(cx, cy, cx + r * 0.58 * math.cos(ang), cy + r * 0.58 * math.sin(ang), color, w=w * 1.8, a=a * 0.9)
        ang = math.radians(sec * 6 - 90)
        L.line(cx - r * 0.12 * math.cos(ang), cy - r * 0.12 * math.sin(ang), cx + r * 0.80 * math.cos(ang), cy + r * 0.80 * math.sin(ang), accent, w=w * 1.1, a=a)
        L.circle(cx, cy, w * 2.2, accent, a=a)
    if label:
        T.label(L, label, cx, cy + r * 1.28 + 24 * H / 1080, H, a=a, color=P.dim)

def stars(ctx, key="stars"):
    if key not in ctx.cache: ctx.cache[key] = Stars()
    return ctx.cache[key]

def starfield2d(ctx, t, drift=(0.0, 0.0), gain=1.0, fov=70.0, yaw=0.0, pitch=0.0, size=1.0):
    st = stars(ctx)
    yaw = yaw + drift[0] * t; pitch = pitch + drift[1] * t
    fwd = np.array([math.sin(yaw) * math.cos(pitch), math.sin(pitch), math.cos(yaw) * math.cos(pitch)], np.float32)
    return st.render_dirs(ctx.W, ctx.H, fwd, np.array([0, 1, 0], np.float32), fov, t=t, gain=gain, size=size)

def horizon_line(L, W, H, y, a=0.3):
    L.line(0, y, W, y, P.dim, w=1.0, a=a)

def earth_disc(ctx, cx, cy, r, light_dir=(-0.6, -0.3), t=0.0, detail=True):
    """Procedural Earth: shaded sphere with noise continents, atmosphere limb. Returns (rgb, alpha) arrays (full frame)."""
    H, W = ctx.H, ctx.W
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = (x - cx) / r, (y - cy) / r
    rr = dx * dx + dy * dy
    inside = rr < 1
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    ld = np.array([light_dir[0], light_dir[1], 0.75]); ld /= np.linalg.norm(ld)
    ndl = np.clip(dx * ld[0] + dy * ld[1] + z * ld[2], 0, 1)
    # continents + clouds via fBm on the sphere (rotating slowly with t)
    key = ("earthtex", int(r), int(cx), int(cy), int(t * 2))
    if key not in ctx.cache:
        rot = t * 0.015
        px = dx * np.cos(rot) + z * np.sin(rot); pz = -dx * np.sin(rot) + z * np.cos(rot); py = dy
        n = fbm3(px * 2.6, py * 2.6, pz * 2.6, octaves=6)
        land = smooth_arr((n - 0.50) * 9.0)
        ice = smooth_arr((np.abs(py) - 0.80) * 8.0)
        n2 = fbm3(px * 4.0 + 5, py * 4.0 - 3, pz * 4.0 + 2, octaves=5)
        cloud = smooth_arr((n2 - 0.52) * 7.0) * 0.8
        ctx.cache.clear() if len(ctx.cache) > 40 else None
        ctx.cache[key] = (land, ice, cloud, n)
    land, ice, cloud, n = ctx.cache[key]
    ocean = np.array([0.03, 0.09, 0.26], np.float32); landc = np.array([0.20, 0.21, 0.12], np.float32)
    desert = np.array([0.36, 0.30, 0.18], np.float32)
    lc = landc[None, None] * (1 - (n[..., None] - 0.5) * 2) + desert[None, None] * np.clip((n[..., None] - 0.5) * 2, 0, 1)
    col = ocean[None, None] * (1 - land[..., None]) + lc * land[..., None]
    col = col * (1 - ice[..., None]) + ice[..., None] * 0.85
    col = col * (1 - cloud[..., None]) + cloud[..., None] * 0.95
    shade = (ndl ** 0.9) * 1.1 + 0.02
    rgb = col * shade[..., None]
    # atmosphere rim (inside) + halo (outside)
    rim = np.clip(1 - z, 0, 1) ** 4 * np.clip(ndl + 0.25, 0, 1)
    rgb += rim[..., None] * np.array([0.35, 0.6, 1.0], np.float32) * 0.8
    rgb *= inside[..., None]
    halo = np.exp(-np.clip(np.sqrt(rr) - 1, 0, None) * 9) * (~inside) * np.clip(dx * ld[0] + dy * ld[1] + 0.5, 0.05, 1) ** 1.5
    rgb += halo[..., None] * np.array([0.3, 0.55, 1.0], np.float32) * 0.6
    alpha = np.clip(inside + halo * 0.9, 0, 1).astype(np.float32)
    return rgb.astype(np.float32), alpha

_PERM = np.random.default_rng(11).permutation(512).astype(np.int64)
def _hash3(ix, iy, iz):
    return _PERM[(_PERM[(_PERM[ix & 255] + iy) & 511] + iz) & 511] / 511.0
def noise3(x, y, z):
    """Value noise on a 3D lattice with smoothstep interpolation (vectorised)."""
    ix, iy, iz = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64), np.floor(z).astype(np.int64)
    fx, fy, fz = x - ix, y - iy, z - iz
    fx, fy, fz = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy), fz * fz * (3 - 2 * fz)
    def c(dx, dy, dz): return _hash3(ix + dx, iy + dy, iz + dz)
    x00 = c(0, 0, 0) * (1 - fx) + c(1, 0, 0) * fx; x10 = c(0, 1, 0) * (1 - fx) + c(1, 1, 0) * fx
    x01 = c(0, 0, 1) * (1 - fx) + c(1, 0, 1) * fx; x11 = c(0, 1, 1) * (1 - fx) + c(1, 1, 1) * fx
    y0 = x00 * (1 - fy) + x10 * fy; y1 = x01 * (1 - fy) + x11 * fy
    return y0 * (1 - fz) + y1 * fz
def fbm3(x, y, z, octaves=5, lac=2.0, gain=0.5):
    v = np.zeros_like(x); amp = 1.0; f = 1.0; norm = 0.0
    for _ in range(octaves):
        v += amp * noise3(x * f + 17.1 * f, y * f + 3.7 * f, z * f + 9.2 * f); norm += amp; amp *= gain; f *= lac
    return v / norm

def smooth_arr(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def over(frame, rgb, alpha):
    frame *= (1 - alpha)[..., None]; frame += rgb; return frame
