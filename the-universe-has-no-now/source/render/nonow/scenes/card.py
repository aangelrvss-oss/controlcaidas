import math
from .common import *

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H
    f = np.zeros((H, W, 3), np.float32)
    L = Layer(W, H)
    style = p.get("style", "quote")
    if style == "quote":
        lines = p["text"].split("\n")
        n = sum(len(l) + 2 for l in lines)
        chars = T.reveal(t, 0.6, min(3.2, dur * 0.4), n)
        a = fade(t, 0.0, 0.5, dur - 2.0, dur - 0.3) if dur > 4 else 1.0
        T.quote(L, lines, W / 2, H / 2, H, a=a, chars=chars, size=46 if len(lines) > 2 else 50)
    elif style == "act":
        a = fade(t, 0.0, 0.8, dur - 1.0, dur - 0.1)
        T.act_label(L, "ACT " + p["act_no"], W / 2, H / 2 - 60 * S(ctx), H, a=a)
        T.act_title(L, p["text"], W / 2, H / 2 + 34 * S(ctx), H, a=a, chars=T.reveal(t, 0.2, 1.6, len(p["text"])))
        # thin rule that grows
        wline = 160 * S(ctx) * smooth(ramp(t, 0.1, 1.4))
        L.line(W / 2 - wline, H / 2 - 20 * S(ctx), W / 2 + wline, H / 2 - 20 * S(ctx), P.dim, w=1.0, a=a * 0.6)
    elif style == "year":
        a = fade(t, 0.0, 0.8, dur - 0.9, dur - 0.1)
        L.text(p["text"], W / 2, H / 2 + 30 * S(ctx), 150 * S(ctx), P.ink, a, "Display-Thin" if False else "Display-ExtraLight", tracking=0.08)
        T.label(L, p.get("sub", ""), W / 2, H / 2 + 110 * S(ctx), H, a=a * smooth(ramp(t, 0.8, 1.8)))
    composite(f, L)
    return f
