import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    phase = p.get("phase", "axes")
    f = background(W, H, gradient=0.15)
    L = Layer(W, H)
    ox, oy = W * 0.5, H * 0.56           # origin on screen
    u = 70 * s                           # pixels per unit (x in light-seconds, t in seconds; c = 1)
    # boost parameter (phase 'boost')
    v = 0.0
    if phase == "boost":
        v = 0.55 * smooth(ramp(t, 1.5, 6.0))
    g = 1 / math.sqrt(1 - v * v)
    def to_screen(x, tt):
        # draw the REST-frame map, but when boosting we show the moving observer's coordinates:
        # the moving observer's grid (x'=const, t'=const) drawn in the rest frame.
        return ox + x * u, oy - tt * u
    # --- grid (rest frame, faint)
    ga = 0.22 * smooth(ramp(t, 0.0, 1.5)) if phase == "axes" else 0.22
    R = 7
    for i in range(-R, R + 1):
        L.line(*to_screen(i, -R), *to_screen(i, R), P.dim, w=1.0, a=ga * (0.5 if i else 0))
        L.line(*to_screen(-R, i), *to_screen(R, i), P.dim, w=1.0, a=ga * (0.5 if i else 0))
    # --- axes
    aa = smooth(ramp(t, 0.2, 1.2)) if phase == "axes" else 1.0
    L.line(*to_screen(-R, 0), *to_screen(R, 0), P.ink, w=1.6 * s, a=0.8 * aa)
    L.line(*to_screen(0, -R), *to_screen(0, R), P.ink, w=1.6 * s, a=0.8 * aa)
    T.label(L, "SPACE", *to_screen(R - 0.6, -0.5), H, a=aa)
    T.label(L, "TIME", *to_screen(0.7, R - 0.3), H, a=aa)
    # --- light lines (45°)
    la = smooth(ramp(t, 5.0, 6.2)) if phase == "axes" else 1.0
    for sgn in (-1, 1):
        L.line(*to_screen(-R * sgn, -R), *to_screen(R * sgn, R), P.cyan, w=1.8 * s, a=0.9 * la)
    if phase == "axes":
        T.label(L, "LIGHT", *to_screen(5.6, 5.0), H, a=la, color=P.cyan)
        T.label(L, "45°", *to_screen(1.2, 0.45), H, a=la, color=P.cyan, size=16)
    # --- cones
    if phase in ("cones", "elsewhere", "boost"):
        ca = smooth(ramp(t, 4.5, 6.0)) if phase == "cones" else 1.0
        fut = [to_screen(0, 0), to_screen(R, R), to_screen(-R, R)]
        pas = [to_screen(0, 0), to_screen(R, -R), to_screen(-R, -R)]
        L.polyline(fut, P.cyan, a=0.10 * ca, fill=True); L.polyline(pas, P.cyan, a=0.07 * ca, fill=True)
        if phase == "cones":
            T.label(L, "FUTURE", *to_screen(0, 4.8), H, a=ca, color=P.cyan)
            T.label(L, "PAST", *to_screen(0, -4.6), H, a=ca, color=P.cyan)
        if phase == "elsewhere":
            ea = smooth(ramp(t, 0.5, 1.8))
            for sgn in (-1, 1):
                els = [to_screen(0, 0), to_screen(sgn * R, R), to_screen(sgn * R, -R)]
                L.polyline(els, P.amber, a=0.08 * ea * (0.6 + 0.4 * math.sin(t * 1.5) ** 2), fill=True)
            T.label(L, "ELSEWHERE", *to_screen(4.4, 0.6), H, a=ea, color=P.amber)
            T.label(L, "ELSEWHERE", *to_screen(-4.4, 0.6), H, a=ea, color=P.amber)
            T.label(L, "NEITHER BEFORE NOR AFTER", W / 2, H * 0.90, H, a=smooth(ramp(t, 3.5, 4.5)), color=P.amber)
    # --- world lines
    if phase in ("cones", "elsewhere", "boost"):
        wa = smooth(ramp(t, 0.3, 1.5)) if phase == "cones" else 1.0
        tt_max = R * (ramp(t, 0.3, 2.5) if phase == "cones" else 1.0)
        # stationary clock at x=-2, moving clock through origin with v=0.4
        L.line(*to_screen(-2.0, -R), *to_screen(-2.0, tt_max), P.amber, w=2.0 * s, a=0.9 * wa)
        L.line(*to_screen(-0.4 * R, -R), *to_screen(0.4 * tt_max, tt_max), P.amber, w=2.0 * s, a=0.9 * wa)
        # ticks (proper time) on both: stationary every 1 s; moving every 1 s proper = 1/sqrt(1-0.16) coordinate
        for k in range(-6, 7):
            L.circle(*to_screen(-2.0, k), 3.5 * s, P.amber, a=wa)
            tk = k * 1 / math.sqrt(1 - 0.16)
            if abs(tk) <= R: L.circle(*to_screen(0.4 * tk, tk), 3.5 * s, P.amber, a=wa)
        if phase == "cones":
            T.label(L, "WORLD LINE", *to_screen(-2.0, 6.4), H, a=wa, color=P.amber)
            T.label(L, "MOVING CLOCK", *to_screen(2.9, 6.4), H, a=wa, color=P.amber)
    # --- boost: moving observer's grid + simultaneity line through events A and B
    if phase == "boost":
        xa, xb = -3.0, 3.0  # two events simultaneous at t=0 in the rest frame
        ba = smooth(ramp(t, 0.3, 1.2))
        # moving observer's lines of simultaneity t' = const  ->  t = v x + const/g
        import skia
        L.canvas.save(); L.canvas.clipRect(skia.Rect.MakeLTRB(ox - R * u, oy - R * u, ox + R * u, oy + R * u))
        for k in range(-R, R + 1):
            c0 = k / g
            pts = [to_screen(x, v * x + c0) for x in (-R, R)]
            L.line(*pts[0], *pts[1], P.violet, w=1.0, a=0.35 * ba)
            # lines x' = const -> x = v t + const/g
            pts = [to_screen(v * tt + c0, tt) for tt in (-R, R)]
            L.line(*pts[0], *pts[1], P.violet, w=1.0, a=0.2 * ba)
        L.canvas.restore()
        # the present (t'=0) through the origin
        L.line(*to_screen(-R, -v * R), *to_screen(R, v * R), P.violet, w=2.4 * s, a=0.95 * ba)
        T.label(L, "'THE PRESENT' FOR A MOVING OBSERVER", *to_screen(0, -4.9 - 0.4), H, a=ba * smooth(ramp(t, 2.0, 3.0)), color=P.violet)
        # events
        for x, name in ((xa, "A"), (xb, "B")):
            sx, sy = to_screen(x, 0)
            L.radial(sx, sy, 22 * s, P.ink, a=0.5); L.circle(sx, sy, 5 * s, P.ink, a=1.0)
            T.label(L, name, sx, sy - 22 * s, H, a=1.0, color=P.ink)
        # readout: t'_A and t'_B
        tpa = g * (0 - v * xa); tpb = g * (0 - v * xb)
        ra = smooth(ramp(t, 2.5, 3.5))
        T.value(L, f"t'(A) = {tpa:+.2f} s", W * 0.86, H * 0.22, H, a=ra, color=P.violet)
        T.value(L, f"t'(B) = {tpb:+.2f} s", W * 0.86, H * 0.27, H, a=ra, color=P.violet)
        T.value(L, f"v = {v:.2f} c", W * 0.86, H * 0.32, H, a=ra, color=P.violet)
        verdict = "A AND B: SAME TIME" if v < 0.03 else ("B HAPPENS BEFORE A" if tpb < tpa else "A HAPPENS BEFORE B")
        T.label(L, verdict, W * 0.86, H * 0.38, H, a=ra, color=P.amber)
        T.equation(L, "t′ = γ (t − v x / c²)", W * 0.86, H * 0.82, H, a=ra * 0.9, size=30)
    composite(f, L)
    return f
