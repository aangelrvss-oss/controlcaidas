"""Typography system.

Hierarchy (at 1080p; scaled by H/1080):
  title     : Inter Display Light 92, tracking 0.02, ink
  act label : Inter Display Regular 22, tracking 0.32, uppercase, dim      ("ACT II")
  act title : Inter Display Light 64, tracking 0.06, uppercase, ink
  quote     : Inter Display Light 52, ink, multi-line centred
  label     : Inter Medium 20, tracking 0.22, uppercase, dim/accent   (diagram labels)
  value     : DejaVu Mono 26, accent                                   (readouts)
  caption   : Inter Regular 24, dim                                    (lower-third source notes)
  equation  : DejaVu Serif/Sans 44, ink                                (unicode math)
Every text element has a purpose: a title, a label on a diagram, a measured value, or a source.
"""
from .core import P, Layer, clamp01, smooth

def S(H): return H / 1080.0

def title(layer, s, cx, cy, H, a=1.0, size=92, color=P.ink, chars=None):
    layer.text(s, cx, cy, size * S(H), color, a, "Display-Light", tracking=0.02, max_alpha_chars=chars)

def act_label(layer, s, cx, cy, H, a=1.0):
    layer.text(s, cx, cy, 22 * S(H), P.dim, a, "Display-Regular", tracking=0.32)

def act_title(layer, s, cx, cy, H, a=1.0, chars=None):
    layer.text(s, cx, cy, 64 * S(H), P.ink, a, "Display-Light", tracking=0.06, max_alpha_chars=chars)

def quote(layer, lines, cx, cy, H, a=1.0, size=50, chars=None, color=P.ink):
    lh = size * 1.45 * S(H)
    y0 = cy - lh * (len(lines) - 1) / 2
    used = 0
    for i, ln in enumerate(lines):
        c = None if chars is None else max(0.0, chars - used)
        layer.text(ln, cx, y0 + i * lh, size * S(H), color, a, "Display-Light", tracking=0.01, max_alpha_chars=c)
        used += len(ln) + 2

def label(layer, s, x, y, H, a=1.0, color=P.dim, align="center", size=20, face="Medium"):
    layer.text(s, x, y, size * S(H), color, a, face, align=align, tracking=0.22)

def value(layer, s, x, y, H, a=1.0, color=P.amber, align="center", size=26):
    layer.text(s, x, y, size * S(H), color, a, "Mono", align=align)

def caption(layer, s, x, y, H, a=1.0, color=P.dim, align="left", size=22):
    layer.text(s, x, y, size * S(H), color, a, "Regular", align=align, tracking=0.01)

def equation(layer, s, x, y, H, a=1.0, color=P.ink, size=44, align="center", face="Serif"):
    layer.text(s, x, y, size * S(H), color, a, face, align=align)

def source_note(layer, s, W, H, a=1.0):
    """Lower-left source line, used sparingly for measured facts."""
    caption(layer, s, 70 * S(H), H - 54 * S(H), H, a=a * 0.85, size=20)

def reveal(t, t0, dur, n):
    """Typewriter-style character count for a reveal starting at t0 over dur seconds."""
    return clamp01((t - t0) / dur) * n * 1.15
