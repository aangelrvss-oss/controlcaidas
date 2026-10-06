"""Gravitational lensing by a point mass: the lens equation beta = theta - theta_E^2/theta, applied to a
procedural background galaxy. A compact lens crosses in front; arcs form, then an Einstein ring."""
import math
from .common import *

def source_galaxy(ctx):
    key = ("lens_src",)
    if key not in ctx.cache:
        H, W = ctx.H, ctx.W
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        ctx.cache[key] = (x, y)
    return ctx.cache[key]

def galaxy_image(bx, by, cx, cy, rr, ang=0.6, q=0.55):
    """Elliptical Sérsic-like profile in source-plane coords."""
    dx, dy = bx - cx, by - cy
    u = dx * math.cos(ang) + dy * math.sin(ang); v = -dx * math.sin(ang) + dy * math.cos(ang)
    r = np.sqrt(u * u + (v / q) ** 2) / rr
    I = np.exp(-1.7 * (r ** 0.6)) * 1.1 + np.exp(-(r * 6) ** 2) * 1.2
    col = np.stack([I * 1.0, I * 0.86, I * 0.72], -1)
    # bluish spiral-ish texture
    tex = 0.5 + 0.5 * np.cos(4 * np.arctan2(v, u) - 2.5 * np.log(r + 0.2))
    col[..., 2] += I * 0.35 * tex
    return col * 0.55

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    x, y = source_galaxy(ctx)
    f = background(W, H, gradient=0.10)
    f += starfield2d(ctx, t, gain=0.3, fov=80) * 0.6
    # lens moves from left to centre, then holds
    u = smooth(ramp(t, 0.5, 7.5))
    lx = W * 0.12 + (W * 0.5 - W * 0.12) * u; ly = H * 0.5
    thetaE = 150 * s  # Einstein radius in pixels
    dx, dy = x - lx, y - ly
    th2 = dx * dx + dy * dy + 1e-3
    # lens equation (point mass): beta = theta * (1 - thetaE^2 / |theta|^2)
    fac = 1 - thetaE ** 2 / th2
    bx, by = lx + dx * fac, ly + dy * fac
    img = galaxy_image(bx, by, W * 0.5, H * 0.5, 55 * s)
    # magnification-aware brightness is already implicit in the mapping (surface brightness conserved)
    f += img
    # the lens itself: a compact dark cluster core with faint glow
    L = Layer(W, H)
    L.radial(lx, ly, 40 * s, P.amber, a=0.35)
    L.circle(lx, ly, 6 * s, (1, 0.9, 0.7), a=0.9)
    aa = smooth(ramp(t, 0.0, 0.8))
    T.label(L, "FOREGROUND MASS", lx, ly + 70 * s, H, a=aa * 0.8, color=P.amber, size=16)
    e = smooth(ramp(t, 7.5, 8.5))
    T.label(L, "EINSTEIN RING", W / 2, H * 0.5 - thetaE - 28 * s, H, a=e, color=P.cyan)
    L.circle(W / 2, H / 2, thetaE, P.cyan, w=1.0, a=0.35 * e)
    T.equation(L, "β = θ − θE² / θ", W * 0.82, H * 0.86, H, a=aa * 0.85, size=30)
    T.caption(L, "point-mass lens equation, applied pixel by pixel", W * 0.82, H * 0.905, H, a=aa * 0.7, align="center", size=18)
    composite(f, L)
    return f
