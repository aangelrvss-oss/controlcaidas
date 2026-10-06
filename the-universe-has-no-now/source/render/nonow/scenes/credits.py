import math
from .common import *

CREDITS = [
    ("THE UNIVERSE HAS NO NOW", "title"),
    ("What relativity and quantum mechanics reveal about reality", "sub"),
    ("", ""),
    ("WRITTEN, DIRECTED AND PRODUCED BY", "h"), ("Claude (Anthropic)", "n"),
    ("NARRATION", "h"), ("Kokoro-82M text-to-speech, voice af_heart (local synthesis)", "n"),
    ("VISUALS", "h"), ("Procedural renderer in Python · NumPy · Skia · SciPy", "n"),
    ("BLACK HOLE", "h"), ("Schwarzschild null geodesics, thin disk, g³ beaming — computed, not painted", "n"),
    ("MUSIC AND SOUND DESIGN", "h"), ("Procedural synthesis (NumPy), mixed to −14 LUFS", "n"),
    ("SCIENCE REFERENCES", "h"), ("Einstein 1905, 1915 · Schwarzschild 1916 · Bell 1964 · Chou et al. 2010 · EHT 2019/2022 · LIGO 2015", "n"),
    ("", ""), ("Every image in this film was rendered from equations and code.", "n"),
    ("No stock footage. No generative video.", "n"),
]

def render(ctx, t, dur, p, shot):
    W, H = ctx.W, ctx.H; s = S(ctx)
    f = background(W, H, gradient=0.05)
    f += starfield2d(ctx, t, gain=0.15, fov=80, drift=(0.0008, 0)) * 0.5
    L = Layer(W, H)
    speed = (H * 1.75) / max(dur - 2.0, 1)   # px/s so that all credits scroll through
    y = H + 40 * s - t * speed
    for txt, kind in CREDITS:
        if kind == "title":
            T.title(L, txt, W / 2, y, H, size=56); y += 60 * s
        elif kind == "sub":
            T.caption(L, txt, W / 2, y, H, align="center", size=22); y += 70 * s
        elif kind == "h":
            T.label(L, txt, W / 2, y, H, size=14); y += 34 * s
        elif kind == "n":
            T.caption(L, txt, W / 2, y, H, align="center", size=21); y += 54 * s
        else:
            y += 30 * s
    a_out = 1 - smooth(ramp(t, dur - 1.5, dur))
    composite(f, L, gain=a_out)
    return f
