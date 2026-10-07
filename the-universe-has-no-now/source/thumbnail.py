"""YouTube thumbnail: the ray-traced black hole + one idea in big type. 1280x720 (and a 1920x1080 master)."""
import os, sys, math, numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "source", "render"))
from nonow import bh as BH
from nonow.core import finish, Layer, composite, P
from nonow import text as T
from nonow.scenes.common import draw_clock
from PIL import Image

def make(W=1920, H=1080):
    s = H / 1080
    inc = math.radians(80); az = 0.9; r = 58
    cam = (r * math.sin(inc) * math.cos(az), r * math.sin(inc) * math.sin(az), r * math.cos(inc))
    img, A = BH.render_scaled(W, H, 1.0, cam=cam, look=(0, 0, 0), fov_deg=34, t=104.0, disk_gain=0.5, sky_gain=0.8, rot_speed=0.35)
    # darken the right third for type
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    img *= (1 - 0.55 * np.clip((x / W - 0.50) / 0.35, 0, 1))[..., None]
    L = Layer(W, H)
    L.text("THE UNIVERSE", W * 0.96, H * 0.36, 118 * s, P.ink, 1.0, "Display-SemiBold", align="right", tracking=-0.01)
    L.text("HAS NO", W * 0.96, H * 0.50, 118 * s, P.ink, 1.0, "Display-SemiBold", align="right", tracking=-0.01)
    L.text("NOW", W * 0.96, H * 0.66, 150 * s, P.amber, 1.0, "Display-Bold", align="right", tracking=-0.01)
    T.label(L, "RELATIVITY  ·  QUANTUM MECHANICS  ·  WHAT IS REAL", W * 0.96, H * 0.74, H, a=0.9, align="right", size=20)
    # two small clocks disagreeing
    draw_clock(L, W * 0.80, H * 0.88, 44 * s, 10.0, a=0.95, H=H, minute=False)
    draw_clock(L, W * 0.92, H * 0.88, 44 * s, 14.5, a=0.95, H=H, minute=False)
    composite(img, L)
    out = finish(img, bloom_strength=0.45, vig=0.3)
    return Image.fromarray(out)

if __name__ == "__main__":
    im = make()
    os.makedirs(os.path.join(ROOT, "thumbnail"), exist_ok=True)
    im.save(os.path.join(ROOT, "thumbnail", "thumbnail_1920.png"))
    im.resize((1280, 720), Image.LANCZOS).save(os.path.join(ROOT, "thumbnail.png"))
    im.resize((320, 180), Image.LANCZOS).save(os.path.join(ROOT, "thumbnail", "thumbnail_small_preview.png"))
    print("thumbnail written")
