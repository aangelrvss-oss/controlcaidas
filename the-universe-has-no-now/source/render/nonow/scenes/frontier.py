"""The unknown: a single point; three candidate ideas tagged ACTIVE RESEARCH; established vs research; the thesis."""
import math
from .common import *

def tag(L, s_, x, y, H, a, text="ACTIVE RESEARCH", col=P.violet):
    w = 150 * s_ if len(text) > 12 else 120 * s_
    L.rect(x - w / 2, y - 12 * s_, w, 24 * s_, col, a=0.0, sw=1.0)
    L.rect(x - w / 2, y - 12 * s_, w, 24 * s_, col, a=0.9 * a, sw=1.0, rx=3 * s_)
    T.label(L, text, x, y + 5 * s_, H, a=a, color=col, size=11)

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    phase = p.get("phase", "question")
    f = background(W, H, gradient=0.06)
    L = Layer(W, H)
    a = smooth(ramp(t, 0.0, 1.0))
    if phase == "question":
        # a single point of light, breathing
        br = 0.6 + 0.4 * math.sin(t * 0.8)
        L.radial(W / 2, H / 2, 90 * s, P.ink, a=0.12 * a * br); L.circle(W / 2, H / 2, 2.5 * s, (1, 1, 1), a=a)
        T.quote(L, ["What is reality made of,", "at the deepest level?"], W / 2, H * 0.72, H, a=a * smooth(ramp(t, 1.2, 2.4)), size=36)
    elif phase == "candidates":
        cols = (W * 0.2, W * 0.5, W * 0.8); cy = H * 0.46
        names = ("STRING THEORY", "LOOP QUANTUM GRAVITY", "EMERGENT SPACETIME")
        subs = ("particles as vibrating strings", "space woven from discrete loops", "geometry from entanglement, like temperature from motion")
        for k, cx in enumerate(cols):
            aa = a * smooth(ramp(t, 2.0 + 2.0 * k, 3.0 + 2.0 * k))
            if aa <= 0: continue
            if k == 0:
                pts = [(cx + 120 * s * math.cos(th) * (1 + 0.12 * math.sin(5 * th + t * 5)), cy + 80 * s * math.sin(th) * (1 + 0.12 * math.sin(5 * th + t * 5))) for th in np.linspace(0, 2 * math.pi, 160)]
                L.polyline(pts, P.violet, w=2.0 * s, a=0.9 * aa, close=True)
            elif k == 1:
                rng = np.random.default_rng(4)
                nodes = [(cx + rng.uniform(-130, 130) * s, cy + rng.uniform(-90, 90) * s) for _ in range(14)]
                for i in range(14):
                    for j in range(i + 1, 14):
                        d = math.hypot(nodes[i][0] - nodes[j][0], nodes[i][1] - nodes[j][1])
                        if d < 110 * s: L.line(*nodes[i], *nodes[j], P.violet, w=1.0, a=0.6 * aa)
                for n_ in nodes: L.circle(n_[0], n_[1], 4 * s, P.violet, a=aa)
            else:
                rng = np.random.default_rng(8)
                u = 0.5 + 0.5 * math.sin(t * 0.7)
                for i in range(9):
                    for j in range(7):
                        gx, gy = cx - 120 * s + i * 30 * s, cy - 90 * s + j * 30 * s
                        rx, ry = gx + rng.uniform(-40, 40) * s, gy + rng.uniform(-40, 40) * s
                        x, y = rx * (1 - u) + gx * u, ry * (1 - u) + gy * u
                        L.circle(x, y, 2.5 * s, P.violet, a=0.9 * aa)
            T.label(L, names[k], cx, cy + 135 * s, H, a=aa, color=P.ink, size=15)
            T.caption(L, subs[k], cx, cy + 165 * s, H, a=aa * 0.8, align="center", size=16)
            tag(L, s, cx, cy + 205 * s, H, aa)
    elif phase == "status":
        xl, xr = W * 0.27, W * 0.73; y0 = H * 0.26
        T.label(L, "ESTABLISHED", xl, y0, H, a=a, color=P.amber, size=20)
        T.label(L, "ACTIVE RESEARCH  /  SPECULATION", xr, y0, H, a=a, color=P.violet, size=20)
        L.line(xl - 220 * s, y0 + 16 * s, xl + 220 * s, y0 + 16 * s, P.amber, w=1.0, a=0.6 * a)
        L.line(xr - 220 * s, y0 + 16 * s, xr + 220 * s, y0 + 16 * s, P.violet, w=1.0, a=0.6 * a)
        est = ["relativity of simultaneity", "time dilation (GPS, optical clocks)", "curved spacetime, lensing, black holes", "gravitational waves (2015)",
               "quantum superposition & interference", "Bell-inequality violations", "no faster-than-light signalling"]
        res = ["string theory", "loop quantum gravity", "emergent spacetime", "what happens inside a black hole", "the first instant of the universe", "a quantum theory of gravity"]
        for i, e in enumerate(est):
            T.caption(L, e, xl, y0 + 60 * s + i * 40 * s, H, a=a * smooth(ramp(t, 0.5 + i * 0.25, 1.0 + i * 0.25)), align="center", size=22)
        for i, e in enumerate(res):
            T.caption(L, e, xr, y0 + 60 * s + i * 40 * s, H, a=a * smooth(ramp(t, 1.0 + i * 0.3, 1.5 + i * 0.3)), align="center", size=22, color=P.dim)
    else:  # established: the thesis, line by line, as the audio delivers it
        lines = [("THERE IS NO UNIVERSAL NOW", 2.6), ("TIME IS LOCAL, RELATIVE, SHAPED BY MASS", 5.0),
                 ("THE SMALLEST SCALES ARE PROBABILISTIC AND NON-CLASSICALLY CORRELATED", 8.4),
                 ("OUR TWO BEST THEORIES DO NOT YET FIT TOGETHER", 12.5)]
        for i, (txt, t0) in enumerate(lines):
            aa = a * smooth(ramp(t, t0, t0 + 0.8))
            T.label(L, txt, W / 2, H * 0.36 + i * 72 * s, H, a=aa, color=P.ink if i < 3 else P.amber, size=20)
        L.radial(W / 2, H * 0.14, 60 * s, P.ink, a=0.10 * a); L.circle(W / 2, H * 0.14, 2.5 * s, (1, 1, 1), a=a)
    composite(f, L)
    return f
