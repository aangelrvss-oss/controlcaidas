"""Schwarzschild black hole renderer (G = c = M = 1).

Null geodesics are integrated once per impact parameter b (Binet equation
u'' + u = 3 u^2, u = 1/r) into a lookup table r(phi; b).  Because the metric
is spherically symmetric, every pixel's ray lies in a plane through the centre,
so a pixel is rendered by (1) finding its b and orbital-plane basis, (2) taking
the analytic angles where that plane crosses the equatorial (disk) plane, and
(3) looking up r at those angles.  Disk emission uses a Shakura–Sunyaev-like
profile with Keplerian orbits; the observed intensity is scaled by g^3 with
g = sqrt(1 - 3/r) / (1 - Omega * L_z)  (gravitational + Doppler shift).
Background stars are mapped through the asymptotic escape direction.

Validation (tests/test_physics.py): critical impact parameter -> 3*sqrt(3),
weak-field deflection -> 4/b, horizon capture.
"""
import math, numpy as np
from scipy.ndimage import zoom as nd_zoom, map_coordinates
from .core import Stars, rgb_from_temp

B_CRIT = 3 * math.sqrt(3)

class GeodesicTable:
    def __init__(self, R_far=80.0, dphi=0.004, phimax=4 * math.pi):
        b1 = np.arange(0.0, 4.6, 0.01)
        b2 = np.arange(4.6, 5.9, 0.0004)
        b3 = np.arange(5.9, 12.0, 0.004)
        b4 = np.arange(12.0, R_far, 0.02)
        self.b = np.concatenate([b1, b2, b3, b4]).astype(np.float64)
        self.R_far, self.dphi = R_far, dphi
        nb = len(self.b); nphi = int(phimax / dphi) + 1
        self.nphi = nphi
        u = np.full(nb, 1.0 / R_far); bb = np.maximum(self.b, 1e-6)
        du = np.sqrt(np.maximum(1.0 / bb ** 2 - u ** 2 * (1 - 2 * u), 0.0))
        self.r = np.full((nb, nphi), np.nan, np.float32)
        self.r[:, 0] = R_far
        alive = np.ones(nb, bool); captured = np.zeros(nb, bool); escaped = np.zeros(nb, bool)
        self.phi_end = np.full(nb, phimax); self.end_idx = np.full(nb, nphi - 1)
        def f(u, du): return du, 3 * u * u - u
        h = dphi
        for i in range(1, nphi):
            k1u, k1d = f(u, du); k2u, k2d = f(u + 0.5 * h * k1u, du + 0.5 * h * k1d)
            k3u, k3d = f(u + 0.5 * h * k2u, du + 0.5 * h * k2d); k4u, k4d = f(u + h * k3u, du + h * k3d)
            un = u + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u); dun = du + h / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
            u = np.where(alive, un, u); du = np.where(alive, dun, du)
            cap = alive & (u >= 0.5); esc = alive & (u <= 1.0 / R_far) & (du < 0)
            self.r[:, i] = np.where(alive, 1.0 / np.maximum(u, 1e-9), np.nan)
            newly = (cap | esc)
            self.phi_end[newly] = i * dphi; self.end_idx[newly] = i
            captured |= cap; escaped |= esc; alive &= ~newly
        self.captured = captured | (~escaped)          # rays that never escaped within phimax are treated as captured
        # direction angles (in the table frame) at phi=0 and at phi_end, from finite differences of positions
        self.theta0 = self._dir_angle(0, +1)
        self.theta_end = self._dir_angle(self.end_idx, -1)

    def _dir_angle(self, idx, sign):
        idx = np.broadcast_to(np.asarray(idx), self.b.shape).astype(int)
        j0 = np.clip(idx, 0, self.nphi - 2); j1 = j0 + 1
        if sign < 0: j1 = np.clip(idx, 1, self.nphi - 1); j0 = j1 - 1
        ar = np.arange(len(self.b))
        r0 = self.r[ar, j0]; r1 = self.r[ar, j1]
        p0 = np.stack([r0 * np.cos(j0 * self.dphi), r0 * np.sin(j0 * self.dphi)], 1)
        p1 = np.stack([r1 * np.cos(j1 * self.dphi), r1 * np.sin(j1 * self.dphi)], 1)
        v = p1 - p0
        return np.arctan2(v[:, 1], v[:, 0])

    def phi_start(self, r0):
        """phi where r(phi) first drops to r0 on the inbound branch (per b)."""
        rr = np.nan_to_num(self.r, nan=1e9)
        hit = rr <= r0
        idx = np.argmax(hit, axis=1)
        has = hit[np.arange(len(self.b)), idx]
        i1 = np.clip(idx, 1, self.nphi - 1); i0 = i1 - 1
        ar = np.arange(len(self.b))
        ra, rb = rr[ar, i0], rr[ar, i1]
        frac = np.clip((ra - r0) / np.maximum(ra - rb, 1e-9), 0, 1)
        phi = (i0 + frac) * self.dphi
        phi[~has] = np.nan                       # rays that never reach r0 (b > r0): straight-ish, handled separately
        return phi

    def lookup_r(self, bi, phi):
        """bilinear r at fractional b index bi and angle phi (vectorised)."""
        fi = phi / self.dphi
        i0 = np.clip(np.floor(fi).astype(int), 0, self.nphi - 2); fr = np.clip(fi - i0, 0, 1)
        b0 = np.clip(np.floor(bi).astype(int), 0, len(self.b) - 2); fb = np.clip(bi - b0, 0, 1)
        r00 = self.r[b0, i0]; r01 = self.r[b0, i0 + 1]; r10 = self.r[b0 + 1, i0]; r11 = self.r[b0 + 1, i0 + 1]
        return (r00 * (1 - fr) + r01 * fr) * (1 - fb) + (r10 * (1 - fr) + r11 * fr) * fb

_PERM = np.random.default_rng(11).permutation(512).astype(np.int64)
def _noise2(x, y):
    ix, iy = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    fx, fy = x - ix, y - iy; fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    def h(a, b): return _PERM[(_PERM[a & 511] + b) & 511] / 511.0
    v = (h(ix, iy) * (1 - fx) + h(ix + 1, iy) * fx) * (1 - fy) + (h(ix, iy + 1) * (1 - fx) + h(ix + 1, iy + 1) * fx) * fy
    return v
def _fbm2(x, y, oct=4):
    v = np.zeros_like(x); amp = 1.0; f = 1.0; n = 0.0
    for _ in range(oct):
        v += amp * _noise2(x * f, y * f); n += amp; amp *= 0.5; f *= 2.0
    return v / n

_TABLE = None
def table():
    global _TABLE
    if _TABLE is None: _TABLE = GeodesicTable()
    return _TABLE

_SKY = None
def skymap(W=3072, H=1536):
    """Equirectangular star map (longitude 0..2pi, latitude -pi/2..pi/2)."""
    global _SKY
    if _SKY is None:
        st = Stars(n=42000, seed=3)
        d = st.dirs
        lon = np.arctan2(d[:, 0], d[:, 2]) % (2 * math.pi); lat = np.arcsin(np.clip(d[:, 1], -1, 1))
        x = lon / (2 * math.pi) * W; y = (0.5 - lat / math.pi) * H
        from .core import splat_points
        img = splat_points(W, H, x, y, st.bright * 1.9, st.col, size=1.0)
        # faint milky-way band
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        band = np.exp(-((yy / H - 0.5 + 0.08 * np.sin(xx / W * 2 * math.pi * 2)) / 0.08) ** 2) * 0.05
        img += band[..., None] * np.array([0.6, 0.65, 0.8], np.float32)
        _SKY = img
    return _SKY

def render_bh(W, H, cam, look, fov_deg, t, r_in=6.0, r_out=20.0, T_peak=3800.0, disk_gain=1.0, sky_gain=1.0,
              turb=1.0, up=(0, 0, 1), K=4, rot_speed=1.0):
    tab = table()
    cam = np.asarray(cam, np.float64); look = np.asarray(look, np.float64); upv = np.asarray(up, np.float64)
    fwd = look - cam; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, upv); right /= np.linalg.norm(right); upc = np.cross(right, fwd)
    tanf = math.tan(math.radians(fov_deg) / 2)
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float64)
    px = (xs + 0.5) / W * 2 - 1; py = 1 - (ys + 0.5) / H * 2
    d = fwd[None, None] + px[..., None] * right[None, None] * tanf + py[..., None] * upc[None, None] * tanf * (H / W)
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    r0 = np.linalg.norm(cam)
    e1 = cam / r0
    dd = d @ e1
    Lvec = np.cross(cam[None, None, :], d)             # angular momentum per unit energy
    b = np.linalg.norm(Lvec, axis=-1)
    Lz = -Lvec[..., 2]                                  # photon momentum points toward the camera (-d)
    e2 = d - dd[..., None] * e1[None, None]; e2 /= np.maximum(np.linalg.norm(e2, axis=-1, keepdims=True), 1e-9)
    direction = np.where(dd > 0, -1.0, 1.0)             # outbound (-1) or inbound (+1) along the table
    # table index for b
    bi = np.interp(b, tab.b, np.arange(len(tab.b)))
    ps_tab = tab.phi_start(r0)                           # per-b start angle
    phi_s = np.interp(b, tab.b, np.nan_to_num(ps_tab, nan=0.0))
    valid_b = b < r0 - 1e-3
    phi_end = np.interp(b, tab.b, tab.phi_end)
    captured_b = np.interp(b, tab.b, tab.captured.astype(np.float64)) > 0.5
    # disk-plane crossings: z = r (e1z cos psi + e2z sin psi) = 0
    e1z = e1[2]; e2z = e2[..., 2]
    psi0 = np.arctan2(e2z, e1z)
    psi_c = (psi0 + math.pi / 2) % math.pi
    psi_c = np.where(psi_c < 1e-4, psi_c + math.pi, psi_c)
    out = np.zeros((H, W, 3), np.float32)
    A = np.zeros((H, W), np.float32)
    Omega_t = t * rot_speed
    for k in range(K):
        psi = psi_c + k * math.pi
        phi_k = phi_s + direction * psi
        ok = valid_b & (phi_k >= 0) & (phi_k <= phi_end)
        rk = tab.lookup_r(bi, np.clip(phi_k, 0, tab.nphi * tab.dphi - tab.dphi))
        hit = ok & np.isfinite(rk) & (rk >= r_in) & (rk <= r_out)
        if not hit.any(): continue
        rh = rk[hit]
        # position in the disk plane
        pos = rh[:, None] * (np.cos(psi[hit])[:, None] * e1[None, :] + np.sin(psi[hit])[:, None] * e2[hit])
        phid = np.arctan2(pos[:, 1], pos[:, 0])
        Om = rh ** -1.5
        g = np.sqrt(np.maximum(1 - 3.0 / rh, 1e-3)) / np.maximum(1 - Om * Lz[hit], 0.05)
        x = r_in / rh
        prof = x ** 3 * (1 - np.sqrt(x)) * 12.0            # Shakura–Sunyaev-like radial profile (peaks ~ 1)
        T = 1200 + T_peak * (x ** 0.75) * np.maximum(1 - np.sqrt(x), 0) ** 0.25 * 1.9
        # turbulence: pattern co-rotating differentially
        ang = phid - Om * Omega_t
        lr = np.log(rh) * 6.0
        n1 = _fbm2(ang * 2.2, lr, 5)
        n2 = _fbm2(ang * 9.0 + 7.0, lr * 2.5 + 3.0, 4)
        streak = _fbm2(ang * 0.6 + 2.0, lr * 7.0, 3)
        tex = np.clip(0.55 + turb * (1.3 * (n1 - 0.5) + 0.8 * (n2 - 0.5) + 0.6 * (streak - 0.5)) + 0.45, 0.05, None)
        edge = np.clip((r_out - rh) / 4.0, 0, 1) * np.clip((rh - r_in) / 0.6, 0, 1)
        I = prof * tex * (g ** 3) * disk_gain
        col = (rgb_from_temp(np.clip(T * g, 1500, 25000)) ** 1.8) * I[:, None]
        alpha = np.clip(edge * 1.2, 0, 1).astype(np.float32)
        contrib = (1 - A[hit])[:, None] * alpha[:, None] * col
        out[hit] += contrib.astype(np.float32)
        A[hit] += (1 - A[hit]) * alpha
    # background sky for escaping rays
    esc = (~captured_b) | (~valid_b)
    # escape direction in the ray plane
    theta_end = np.interp(b, tab.b, tab.theta_end); theta0 = np.interp(b, tab.b, tab.theta0)
    alpha_ang = np.where(direction > 0, theta_end - phi_s, phi_s - (theta0 + math.pi))
    dir3 = np.cos(alpha_ang)[..., None] * e1[None, None] + np.sin(alpha_ang)[..., None] * e2
    dir3 = np.where(valid_b[..., None], dir3, d)       # rays with b > r0: no table; nearly straight
    sky = skymap()
    lon = np.arctan2(dir3[..., 0], dir3[..., 2]) % (2 * math.pi); lat = np.arcsin(np.clip(dir3[..., 1], -1, 1))
    sx = lon / (2 * math.pi) * sky.shape[1]; sy = (0.5 - lat / math.pi) * sky.shape[0]
    bg = np.stack([map_coordinates(sky[..., c], [sy, sx], order=1, mode="wrap") for c in range(3)], -1)
    out += (bg * sky_gain * esc[..., None] * (1 - A)[..., None]).astype(np.float32)
    return out, A, captured_b & valid_b

def render_scaled(W, H, scale, **kw):
    w, h = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    img, A, cap = render_bh(w, h, **kw)
    if scale != 1.0:
        img = nd_zoom(img, (H / h, W / w, 1), order=1)[:H, :W]
        A = nd_zoom(A, (H / h, W / w), order=1)[:H, :W]
    return img, A
