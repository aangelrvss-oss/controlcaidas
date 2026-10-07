"""Final pull-back: the two clocks, a light pulse, then Earth -> Solar System -> galaxy -> universe -> black."""
import math
from .common import *
from . import scale
from .two_clocks import render as clocks_render

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    f = background(W, H, gradient=0.12)
    L = Layer(W, H)
    # segment schedule (start, end) per layer; each layer zooms out from 1.0 to 0.3
    segs = [("clocks", 0.0, 6.0), ("earth", 4.5, 10.0), ("solar", 8.5, 14.0), ("galaxy", 12.5, 18.0), ("universe", 16.5, 22.5)]
    st = stars(ctx)
    f += starfield2d(ctx, t, gain=0.3 * smooth(ramp(t, 4.0, 7.0)), fov=75) * 0.7
    scale.LABELS = False
    for name, t0, t1 in segs:
        if t < t0 - 0.01 or t > t1 + 0.01: continue
        u = ramp(t, t0, t1)
        a = fade(t, t0, t0 + 1.2, t1 - 1.2, t1)
        zoom = 1.0 * math.exp(-1.6 * u)
        lt = t - t0
        if name == "clocks":
            sec = 10 + t
            r = 150 * s * zoom; gap = 260 * s * zoom
            draw_clock(L, W / 2 - gap, H / 2, r, sec, a=a, H=H, label=None)
            draw_clock(L, W / 2 + gap, H / 2, r, sec, a=a, H=H, label=None)
            # the pulse leaves A for B (speed of light, ~3 s)
            tp = ramp(t, 1.0, 4.0)
            if tp > 0:
                x = W / 2 - gap + 2 * gap * min(tp, 1.0)
                L.line(W / 2 - gap, H / 2, x, H / 2, P.cyan, w=1.5, a=0.6 * a)
                scale._pulse_dot(L, x, H / 2, s * max(zoom, 0.4), a)
        elif name == "earth":
            scale.earth(ctx, lt, zoom * 0.9, a, L, f)
        elif name == "solar":
            scale.solar(ctx, lt + 8, zoom * 0.9, a, L, f)
        elif name == "galaxy":
            scale.galaxy(ctx, lt + 10, zoom * 0.9, a, L, f)
        elif name == "universe":
            scale.universe(ctx, lt + 2, zoom * 1.1, a * 0.6, L, f, figure=False)
    scale.LABELS = True
    composite(f, L)
    return f
