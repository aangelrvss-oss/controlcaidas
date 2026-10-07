"""Act V: the Schwarzschild black hole. Camera choreography per phase."""
import math
from .common import *
from .. import bh as BH

def cam_path(phase, t, dur):
    """Returns (cam position, look-at, fov) in units of M. Disk lies in z=0."""
    u = ramp(t, 0, dur)
    look = (0.0, 0.0, 0.0)
    if phase == "approach":
        r = 190 - 128 * ease_in_out(u)            # 190 -> 62
        inc = math.radians(74 + 4 * u); az = 0.2 + 0.05 * t; fov = 36
    elif phase == "reveal":
        r = 62 - 4 * u; inc = math.radians(78); az = 0.9 + 0.06 * t; fov = 36
    elif phase == "disk":
        r = 56; inc = math.radians(78 + 8 * ease_in_out(u)); az = 1.7 + 0.05 * t; fov = 34
    elif phase == "doppler":
        r = 56 - 18 * ease_in_out(u); inc = math.radians(85); az = 2.4 + 0.04 * t; fov = 32
    elif phase == "ring":
        r = 40; inc = math.radians(80); az = 3.0 + 0.03 * t; fov = 11 - 2.5 * ease_in_out(u)
    else:  # fall
        r = 60; inc = math.radians(80); az = 3.6 + 0.02 * t; fov = 36
    cam = np.array([r * math.sin(inc) * math.cos(az), r * math.sin(inc) * math.sin(az), r * math.cos(inc)])
    if phase == "ring":
        fwd = -cam / r; right = np.cross(fwd, np.array([0, 0, 1.0])); right /= np.linalg.norm(right)
        look = tuple(-right * 5.1)                # aim at the left edge of the shadow (b ≈ b_crit)
    return tuple(cam), look, fov

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    phase = p.get("phase", "approach")
    cam, look, fov = cam_path(phase, t, dur)
    scale = 0.75 if W >= 1900 else 1.0
    img, A = BH.render_scaled(W, H, scale, cam=cam, look=look, fov_deg=fov, t=t * 1.0 + (0 if phase == "approach" else 100),
                              disk_gain=0.42, sky_gain=0.8, rot_speed=0.35)
    f = img
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 1.0))
    if phase == "reveal":
        T.label(L, "SCHWARZSCHILD METRIC  ·  NULL GEODESICS  ·  THIN DISK  ·  g³ BEAMING", W / 2, H * 0.93, H, a=a * smooth(ramp(t, 1.0, 2.0)) * 0.75, size=15)
    if phase == "disk":
        q = smooth(ramp(t, 4.0, 5.0))
        T.label(L, "FAR SIDE OF THE DISK, LENSED OVER THE TOP", W / 2, H * 0.14, H, a=q, color=P.cyan, size=18)
        L.line(W / 2, H * 0.16, W / 2, H * 0.26, P.cyan, w=1.0, a=0.6 * q)
    if phase == "doppler":
        q = smooth(ramp(t, 2.0, 3.0))
        T.label(L, "APPROACHING  ·  BRIGHTER, BLUE-SHIFTED", W * 0.24, H * 0.85, H, a=q, color=P.cyan, size=17)
        T.label(L, "RECEDING  ·  DIMMER, RED-SHIFTED", W * 0.76, H * 0.85, H, a=q, color=P.red, size=17)
        T.equation(L, "g = √(1 − 3M/r) / (1 − Ω Lz)", W / 2, H * 0.93, H, a=q * 0.8, size=26)
    if phase == "ring":
        q = smooth(ramp(t, 1.5, 2.5))
        T.label(L, "PHOTON RING  ·  LIGHT THAT ORBITED BEFORE ESCAPING", W / 2, H * 0.10, H, a=q, color=P.cyan, size=17)
        q2 = smooth(ramp(t, 6.0, 7.0))
        # EHT note: shadow diameter ≈ 2·b_crit = 2·3√3 GM/c² ≈ 5.2 r_s (matches the observed ring scale)
        T.value(L, "shadow diameter ≈ 2 · 3√3 GM/c²  ≈  5.2 Schwarzschild radii", W / 2, H * 0.90, H, a=q2, color=P.ink, size=22)
        T.caption(L, "M87*: EHT 2019  ·  Sgr A*: EHT 2022", W / 2, H * 0.94, H, a=q2 * 0.8, align="center", size=18)
    if phase == "fall":
        # HUMAN MOMENT: astronaut silhouette drifting toward the horizon (screen-space choreography)
        u = ramp(t, 0.5, dur - 2.0)
        fx = W * 0.78 - (W * 0.78 - W * 0.515) * ease_in(u); fy = H * 0.62 - (H * 0.62 - H * 0.53) * ease_in(u)
        size = 260 * s * (1 - 0.75 * ease_in(u))
        L.radial(fx, fy - size / 2, size * 0.9, P.amber, a=0.12 * a)
        silhouette_figure(L, fx, fy, size, color=(0.0, 0.0, 0.0), a=a, pose="astronaut")
        # clocks: the faller's own clock vs. what a distant observer sees
        rr = 16.0 - 13.9 * ease_in(u)                     # radial coordinate of the faller (M units)
        rate = math.sqrt(max(1 - 2.0 / rr, 0.0))            # observed tick rate (static-observer redshift factor)
        tau = 10 + t
        tobs = 10 + t * rate
        q = smooth(ramp(t, 1.0, 2.0))
        T.label(L, "THE FALLING CLOCK, AS IT SEES ITSELF", W * 0.17, H * 0.20, H, a=q, size=15)
        T.value(L, f"τ = {tau:6.2f} s", W * 0.17, H * 0.25, H, a=q, color=P.amber, size=30)
        T.label(L, "THE SAME CLOCK, SEEN FROM FAR AWAY", W * 0.17, H * 0.33, H, a=q, size=15)
        T.value(L, f"t = {tobs:6.2f} s", W * 0.17, H * 0.38, H, a=q, color=P.cyan, size=30)
        T.value(L, f"tick rate  √(1 − 2M/r) = {rate:4.2f}", W * 0.17, H * 0.43, H, a=q, color=P.dim, size=20)
    composite(f, L)
    return f
