"""Entanglement: correlation without signalling. Two observers, random outcomes, perfect correlations,
Bell curve above the classical bound, and an explicit 'no signal' statement."""
import math
from .common import *

def observer(L, x, y, s, a, t, label, col):
    L.radial(x, y - 70 * s, 150 * s, col, a=0.10 * a)
    silhouette_figure(L, x, y, 170 * s, color=(0.01, 0.01, 0.015), a=a, t=t)
    # detector: a small instrument box with a dial
    L.rect(x + 60 * s, y - 120 * s, 70 * s, 50 * s, P.ink, a=0.0, sw=1.5 * s)
    L.rect(x + 60 * s, y - 120 * s, 70 * s, 50 * s, P.ink, a=0.8 * a, sw=1.5 * s)
    T.label(L, label, x, y + 28 * s, H_, a=a, color=col, size=15)

H_ = 1080
def outcomes(rng, n):
    """Perfectly anti-correlated singlet outcomes with aligned settings (for the display)."""
    a = rng.integers(0, 2, n); return a, 1 - a

def render(ctx, t, dur, p, shot):
    global H_
    W, H = ctx.W, ctx.H; s = S(ctx); H_ = H
    phase = p.get("phase", "separate")
    f = background(W, H, gradient=0.12)
    f += starfield2d(ctx, t, gain=0.25, fov=80, drift=(0.001, 0)) * 0.5
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 0.8))
    xe, xf = W * 0.20, W * 0.80; y = H * 0.70
    if phase == "separate":
        # the pair is prepared at the centre, then separates
        u = smooth(ramp(t, 1.0, 6.0))
        x1 = W / 2 - (W / 2 - xe) * u; x2 = W / 2 + (xf - W / 2) * u
        yy = H * 0.45
        L.radial(W / 2, yy, 60 * s * (1 - u) + 10 * s, P.violet, a=0.35 * a * (1 - u))
        for x in (x1, x2):
            L.radial(x, yy, 26 * s, P.violet, a=0.9 * a); L.circle(x, yy, 5 * s, (1, 1, 1), a=a)
        # the shared state: a faint ribbon, not a wire
        pts = [(x1 + (x2 - x1) * k / 60, yy + 10 * s * math.sin(k / 60 * math.pi * 3 + t * 2) * u) for k in range(61)]
        L.polyline(pts, P.violet, w=1.0, a=0.25 * a)
        T.label(L, "ONE SHARED QUANTUM STATE", W / 2, yy - 50 * s, H, a=a * smooth(ramp(t, 0.3, 1.2)), color=P.violet)
        T.equation(L, "|ψ⟩ = ( |↑↓⟩ − |↓↑⟩ ) / √2", W / 2, yy + 70 * s, H, a=a * smooth(ramp(t, 2.0, 3.0)), size=32)
        # Earth and a distant craft appear as destinations
        eu = smooth(ramp(t, 4.0, 5.5))
        rgb, al = earth_disc(ctx, xe, y + 200 * s, 92 * s, light_dir=(-0.5, -0.4), t=0.0)
        over(f, rgb * eu, al * eu)
        observer(L, xe, y + 30 * s, s, eu, t, "EARTH LABORATORY", P.amber)
        observer(L, xf, y + 30 * s, s, eu, t + 1, "DISTANT SPACECRAFT", P.cyan)
        T.value(L, "4 light-hours apart", W / 2, H * 0.80, H, a=eu, color=P.dim, size=22)
    elif phase in ("measure", "nosignal"):
        rgb, al = earth_disc(ctx, xe, y + 200 * s, 92 * s, light_dir=(-0.5, -0.4), t=0.0)
        over(f, rgb, al)
        observer(L, xe, y + 30 * s, s, a, t, "EARTH", P.amber)
        observer(L, xf, y + 30 * s, s, a, t + 1, "SPACECRAFT", P.cyan)
        rng = np.random.default_rng(3)
        A_, B_ = outcomes(rng, 40)
        if phase == "measure":
            n = int(max(0.0, t - 0.8) / 0.55)
            n = min(n, 16)
            # two columns of outcomes, and a 'match' column in the middle
            y0 = H * 0.12; dy = 24 * s
            T.label(L, "EARTH", W * 0.36, y0 - 10 * s, H, a=a, color=P.amber, size=14)
            T.label(L, "SPACECRAFT", W * 0.64, y0 - 10 * s, H, a=a, color=P.cyan, size=14)
            T.label(L, "COMPARE", W * 0.5, y0 - 10 * s, H, a=a * smooth(ramp(t, 5.0, 6.0)), size=14)
            for i in range(n):
                yy = y0 + 24 * s + i * dy
                aa = smooth(ramp(t - 0.8 - i * 0.55, 0, 0.3))
                T.value(L, "↑" if A_[i] else "↓", W * 0.36, yy, H, a=aa, color=P.amber, size=22)
                T.value(L, "↑" if B_[i] else "↓", W * 0.64, yy, H, a=aa, color=P.cyan, size=22)
                ca = smooth(ramp(t - 5.0 - i * 0.2, 0, 0.3))
                T.value(L, "opposite ✓", W * 0.5, yy, H, a=ca, color=P.violet, size=18)
            T.label(L, "EACH LIST ALONE: A RANDOM COIN", W / 2, H * 0.52, H, a=a * smooth(ramp(t, 3.0, 4.0)), size=15)
            # Bell curve inset (bottom-right): E(a,b) = -cos(theta) vs classical bound |E| <= 1 - 2|theta|/pi
            ba = smooth(ramp(t, 8.0, 9.5))
            bx, by, bw, bh = W * 0.37, H * 0.60, W * 0.26, H * 0.22
            if ba > 0:
                L.rect(bx, by, bw, bh, P.dim, a=0.0, sw=1.0)
                L.line(bx, by + bh / 2, bx + bw, by + bh / 2, P.dim, w=1.0, a=0.4 * ba)
                th = np.linspace(0, math.pi, 100)
                q = [(bx + bw * i / 99, by + bh / 2 + bh / 2 * math.cos(th[i]) * 0.95) for i in range(100)]
                L.polyline(q, P.violet, w=2.2 * s, a=0.95 * ba)
                cl = [(bx + bw * i / 99, by + bh / 2 + bh / 2 * (1 - 2 * th[i] / math.pi) * 0.95) for i in range(100)]
                L.polyline(cl, P.dim, w=1.4, a=0.8 * ba)
                T.label(L, "QUANTUM  −cos θ", bx + bw * 0.5, by - 12 * s, H, a=ba, color=P.violet, size=14)
                T.label(L, "ANY LOCAL HIDDEN-VARIABLE MODEL", bx + bw * 0.5, by + bh + 22 * s, H, a=ba, size=13)
                T.label(L, "θ  (angle between detector settings)", bx + bw * 0.5, by + bh + 42 * s, H, a=ba * 0.7, size=12)
                T.source_note(L, "Bell 1964 · Aspect 1982 · Hensen et al. 2015 · Nobel Prize in Physics 2022", W, H, a=ba)
        else:
            # a would-be message is drawn Earth -> craft and struck out; the light cone remains
            u = smooth(ramp(t, 1.5, 3.0))
            yy = H * 0.30
            L.line(xe, yy, xe + (xf - xe) * u, yy, P.red, w=3 * s, a=0.9 * a)
            T.label(L, "MESSAGE ?", W / 2, yy - 24 * s, H, a=a * u, color=P.red)
            xa = smooth(ramp(t, 3.2, 3.8))
            if xa > 0:
                L.line(W / 2 - 40 * s, yy - 40 * s, W / 2 - 40 * s + 80 * s * xa, yy - 40 * s + 80 * s * xa, P.red, w=4 * s, a=0.95)
                L.line(W / 2 + 40 * s, yy - 40 * s, W / 2 + 40 * s - 80 * s * xa, yy - 40 * s + 80 * s * xa, P.red, w=4 * s, a=0.95)
            q = smooth(ramp(t, 4.0, 5.0))
            T.label(L, "NO ONE CAN CHOOSE THE OUTCOME  →  NOTHING TO ENCODE", W / 2, yy + 40 * s, H, a=q, color=P.ink, size=16)
            q2 = smooth(ramp(t, 6.5, 7.5))
            T.label(L, "NO-COMMUNICATION THEOREM", W / 2, H * 0.50, H, a=q2, color=P.violet)
            T.caption(L, "the statistics on one side are identical whatever is done on the other side", W / 2, H * 0.545, H, a=q2 * 0.8, align="center", size=19)
            # the only causal channel: a light signal taking 4 hours, shown as a slow pulse
            q3 = smooth(ramp(t, 8.0, 9.0))
            L.line(xe, H * 0.60, xf, H * 0.60, P.cyan, w=1.0, a=0.3 * q3)
            xp = xe + (xf - xe) * ((t * 0.08) % 1.0)
            L.radial(xp, H * 0.60, 14 * s, P.cyan, a=0.8 * q3)
            T.label(L, "A LIGHT SIGNAL: THE ONLY WAY TO COMPARE  ·  4 HOURS", W / 2, H * 0.635, H, a=q3, color=P.cyan, size=14)
    composite(f, L)
    return f
