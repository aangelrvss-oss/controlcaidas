"""Core rendering primitives for THE UNIVERSE HAS NO NOW.

Frames are float32 arrays (H, W, 3), scene-linear, values may exceed 1 (bloom
reads the overshoot).  Vector/text layers are drawn with Skia and composited
with premultiplied alpha.  Everything is deterministic (seeded).
"""
import os, math
import numpy as np
import skia
from scipy.ndimage import gaussian_filter, zoom as nd_zoom

FONT_DIR = "/usr/share/fonts/opentype/inter/"
_TF = {}
def typeface(name="Display-Light"):
    """name: 'Display-Light', 'Display-Regular', 'Display-Medium', 'Light', 'Regular', 'Medium', 'SemiBold', 'Mono'"""
    if name not in _TF:
        if name == "Mono":
            path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        elif name == "Serif":
            path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
        elif name == "Symbols":
            path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        else:
            path = FONT_DIR + ("Inter" + name if name.startswith("Display") else "Inter-" + name) + ".otf"
        _TF[name] = skia.Typeface.MakeFromFile(path)
    return _TF[name]

# ------------------------------------------------------------------ palette
class P:
    bg      = (0.010, 0.012, 0.020)
    ink     = (0.92, 0.91, 0.88)
    dim     = (0.55, 0.56, 0.60)
    amber   = (0.96, 0.70, 0.34)   # time, clocks, gravity
    cyan    = (0.42, 0.84, 0.96)   # light, quantum
    blue    = (0.30, 0.45, 0.95)
    red     = (0.95, 0.35, 0.30)
    violet  = (0.70, 0.55, 0.95)

def c4(rgb, a=1.0):
    return skia.Color4f(float(rgb[0]), float(rgb[1]), float(rgb[2]), float(a))

def lerp(a, b, t): return a + (b - a) * t
def clamp01(x): return min(1.0, max(0.0, x))
def smooth(t): t = clamp01(t); return t * t * (3 - 2 * t)
def ease_in_out(t): t = clamp01(t); return 0.5 - 0.5 * math.cos(math.pi * t)
def ease_out(t): t = clamp01(t); return 1 - (1 - t) ** 3
def ease_in(t): t = clamp01(t); return t ** 3
def ramp(t, t0, t1): return clamp01((t - t0) / max(1e-6, (t1 - t0)))
def fade(t, t0, t1, t2, t3):
    """0 before t0, up to 1 at t1, hold, down to 0 at t3."""
    if t < t1: return smooth(ramp(t, t0, t1))
    if t < t2: return 1.0
    return 1 - smooth(ramp(t, t2, t3))

# ------------------------------------------------------------------ layers
class Layer:
    """A Skia RGBA drawing surface the size of the frame."""
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.surface = skia.Surface(W, H)
        self.canvas = self.surface.getCanvas()
        self.canvas.clear(skia.Color4f(0, 0, 0, 0))
    def array(self):
        a = self.surface.makeImageSnapshot().toarray()  # BGRA premultiplied
        rgb = a[..., [2, 1, 0]].astype(np.float32) / 255.0
        alpha = a[..., 3].astype(np.float32) / 255.0
        return rgb * alpha[..., None], alpha   # premultiply (toarray() is unpremultiplied)
    def paint(self, color, a=1.0, width=None, stroke=False, blend=None, aa=True):
        p = skia.Paint(AntiAlias=aa, Color=c4(color, a))
        if stroke or width is not None:
            p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(float(width or 1.0))
            p.setStrokeCap(skia.Paint.kRound_Cap)
        if blend == "add": p.setBlendMode(skia.BlendMode.kPlus)
        return p
    def line(self, x0, y0, x1, y1, color, w=1.5, a=1.0, blend=None):
        self.canvas.drawLine(float(x0), float(y0), float(x1), float(y1), self.paint(color, a, w, blend=blend))
    def polyline(self, pts, color, w=1.5, a=1.0, close=False, blend=None, fill=False):
        if len(pts) < 2: return
        path = skia.Path(); path.moveTo(float(pts[0][0]), float(pts[0][1]))
        for x, y in pts[1:]: path.lineTo(float(x), float(y))
        if close: path.close()
        p = self.paint(color, a, None if fill else w, blend=blend)
        if not fill: p.setStrokeJoin(skia.Paint.kRound_Join)
        self.canvas.drawPath(path, p)
    def circle(self, x, y, r, color, w=None, a=1.0, blend=None):
        self.canvas.drawCircle(float(x), float(y), float(r), self.paint(color, a, w, blend=blend))
    def arc(self, x, y, r, a0, a1, color, w=1.5, a=1.0):
        rect = skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r)
        self.canvas.drawArc(rect, float(a0), float(a1 - a0), False, self.paint(color, a, w))
    def rect(self, x, y, w, h, color, a=1.0, sw=None, rx=0):
        r = skia.Rect.MakeXYWH(float(x), float(y), float(w), float(h))
        p = self.paint(color, a, sw)
        if rx: self.canvas.drawRoundRect(r, rx, rx, p)
        else: self.canvas.drawRect(r, p)
    def radial(self, x, y, r, color, a=1.0, blend="add", inner=1.0):
        """Soft radial glow."""
        sh = skia.GradientShader.MakeRadial((float(x), float(y)), float(r),
             [c4(color, a * inner), c4(color, a * 0.35), c4(color, 0.0)], [0.0, 0.35, 1.0])
        p = skia.Paint(AntiAlias=True); p.setShader(sh)
        if blend == "add": p.setBlendMode(skia.BlendMode.kPlus)
        self.canvas.drawCircle(float(x), float(y), float(r), p)
    def text(self, s, x, y, size=40, color=P.ink, a=1.0, face="Display-Light", align="center",
             tracking=0.0, blend=None, max_alpha_chars=None):
        """Draw a line of text with optional letter tracking (in em). Returns width."""
        font = skia.Font(typeface(face), float(size)); font.setSubpixel(True); font.setEdging(skia.Font.Edging.kSubpixelAntiAlias)
        p = self.paint(color, a, blend=blend)
        tr = tracking * size
        if tr == 0 and max_alpha_chars is None:
            w = font.measureText(s)
            x0 = x - w / 2 if align == "center" else (x - w if align == "right" else x)
            self.canvas.drawString(s, float(x0), float(y), font, p)
            return w
        widths = [font.measureText(ch) + tr for ch in s]
        w = sum(widths) - tr
        x0 = x - w / 2 if align == "center" else (x - w if align == "right" else x)
        cx = x0
        for i, ch in enumerate(s):
            if max_alpha_chars is not None:
                aa = clamp01(max_alpha_chars - i)
                if aa <= 0: break
                p = self.paint(color, a * aa, blend=blend)
            self.canvas.drawString(ch, float(cx), float(y), font, p); cx += widths[i]
        return w
    def text_width(self, s, size, face="Display-Light", tracking=0.0):
        font = skia.Font(typeface(face), float(size))
        return sum(font.measureText(ch) + tracking * size for ch in s) - tracking * size
    def image(self, arr_rgb, alpha=None, x=0, y=0):
        h, w = arr_rgb.shape[:2]
        rgba = np.empty((h, w, 4), np.uint8)
        rgba[..., :3] = np.clip(arr_rgb * 255, 0, 255)
        rgba[..., 3] = 255 if alpha is None else np.clip(alpha * 255, 0, 255)
        img = skia.Image.fromarray(rgba, skia.ColorType.kRGBA_8888_ColorType)
        self.canvas.drawImage(img, float(x), float(y))

def composite(frame, layer, gain=1.0):
    """Alpha-composite a Layer over a float frame (in place) and return it."""
    rgb, a = layer.array()
    frame *= (1 - a)[..., None]
    frame += rgb * gain
    return frame

def add_layer(frame, layer, gain=1.0):
    rgb, a = layer.array()
    frame += rgb * gain
    return frame

# ------------------------------------------------------------------ post
def bloom(frame, threshold=0.6, sigma=18, strength=0.6, down=4):
    """Cheap wide bloom: threshold, downsample, blur, upsample, add."""
    H, W = frame.shape[:2]
    small = frame[::down, ::down]
    bright = np.clip(small - threshold, 0, None)
    bl = gaussian_filter(bright, (sigma / down, sigma / down, 0))
    up = nd_zoom(bl, (down, down, 1), order=1)
    up = up[:H, :W]
    if up.shape[0] < H or up.shape[1] < W:
        pad = np.zeros_like(frame); pad[:up.shape[0], :up.shape[1]] = up; up = pad
    return frame + up * strength

def glow_pass(frame, sigma=3, strength=0.25):
    """Tight glow on everything bright (gives lines a filmic halo)."""
    return frame + gaussian_filter(np.clip(frame - 0.25, 0, None), (sigma, sigma, 0)) * strength

def vignette(frame, amount=0.45, power=2.2):
    H, W = frame.shape[:2]
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) / 1.2
    v = 1 - amount * np.clip(r, 0, 1) ** power
    return frame * v[..., None]

_GRAIN_RNG = np.random.default_rng(12345)
def grain(frame, amount=0.009, seed=0):
    rng = np.random.default_rng(seed)
    H, W = frame.shape[:2]
    g = rng.standard_normal((H // 2, W // 2, 1)).astype(np.float32)
    g = np.repeat(np.repeat(g, 2, 0), 2, 1)[:H, :W]
    return frame + g * amount * (0.35 + np.clip(frame.mean(-1, keepdims=True), 0, 1))

def tonemap(frame):
    """Soft-knee highlight roll-off then sRGB-ish gamma, to uint8."""
    x = np.clip(frame, 0, None)
    x = np.where(x < 0.8, x, 0.8 + 0.2 * (1 - np.exp(-(x - 0.8) / 0.2)))
    x = np.clip(x, 0, 1) ** (1 / 1.7)
    return (x * 255 + 0.5).astype(np.uint8)

def finish(frame, seed=0, bloom_strength=0.35, vig=0.4):
    f = frame
    if bloom_strength > 0: f = bloom(f, strength=bloom_strength)
    f = glow_pass(f)
    f = vignette(f, vig)
    f = grain(f, seed=seed)
    return tonemap(f)

# ------------------------------------------------------------------ backgrounds
def background(W, H, color=P.bg, gradient=0.35, center=(0.5, 0.5)):
    """Dark base with a faint radial lift."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x / W - center[0]) * (W / H)) ** 2 + (y / H - center[1]) ** 2)
    lift = (1 - np.clip(r / 0.9, 0, 1)) * gradient
    f = np.empty((H, W, 3), np.float32)
    for i in range(3): f[..., i] = color[i] * (1 + lift)
    return f

class Stars:
    """Deterministic star catalogue on the unit sphere with colours and magnitudes."""
    def __init__(self, n=14000, seed=7):
        rng = np.random.default_rng(seed)
        v = rng.standard_normal((n, 3)); v /= np.linalg.norm(v, axis=1, keepdims=True)
        self.dirs = v.astype(np.float32)
        m = rng.power(0.45, n)  # magnitude-ish distribution: many faint, few bright
        self.bright = (m ** 3.5 * 1.6 + 0.02).astype(np.float32)
        temp = rng.random(n)
        col = np.stack([0.75 + 0.3 * temp, 0.82 + 0.1 * temp, 1.05 - 0.35 * temp], 1)
        self.col = np.clip(col, 0, 1.2).astype(np.float32)
        self.twk = rng.random(n).astype(np.float32) * 6.28

    def render_dirs(self, W, H, forward, up, fov_deg, t=0.0, gain=1.0, size=1.0, extra_dirs=None):
        """Project star directions through a pinhole camera; returns float frame."""
        fwd = forward / np.linalg.norm(forward)
        right = np.cross(fwd, up); right /= np.linalg.norm(right)
        upv = np.cross(right, fwd)
        d = self.dirs
        z = d @ fwd; vis = z > 0.05
        f = (W / 2) / math.tan(math.radians(fov_deg) / 2)
        x = (d[vis] @ right) / z[vis] * f + W / 2
        y = -(d[vis] @ upv) / z[vis] * f + H / 2
        b = self.bright[vis] * gain * (1 + 0.15 * np.sin(t * 2.1 + self.twk[vis]))
        return splat_points(W, H, x, y, b, self.col[vis], size)

def splat_points(W, H, x, y, b, col, size=1.0):
    """Additive splat of points with 2x2 bilinear footprint, then a tiny blur for the bright ones."""
    frame = np.zeros((H, W, 3), np.float32)
    ok = (x >= 0) & (x < W - 1) & (y >= 0) & (y < H - 1)
    x, y, b, col = x[ok], y[ok], b[ok], col[ok]
    xi, yi = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = (x - xi).astype(np.float32), (y - yi).astype(np.float32)
    for dx, dy, w in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        np.add.at(frame, (yi + dy, xi + dx), (b * w)[:, None] * col)
    if size > 0:
        frame = gaussian_filter(frame, (0.6 * size, 0.6 * size, 0)) + gaussian_filter(frame, (2.5 * size, 2.5 * size, 0)) * 0.5
    return frame

def rgb_from_temp(T):
    """Approximate black-body colour (normalised), T in Kelvin, vectorised."""
    T = np.asarray(T, dtype=np.float32) / 100.0
    r = np.where(T <= 66, 255, 329.698727446 * np.clip(T - 60, 1e-3, None) ** -0.1332047592)
    g = np.where(T <= 66, 99.4708025861 * np.log(np.clip(T, 1e-3, None)) - 161.1195681661,
                 288.1221695283 * np.clip(T - 60, 1e-3, None) ** -0.0755148492)
    b = np.where(T >= 66, 255, np.where(T <= 19, 0, 138.5177312231 * np.log(np.clip(T - 10, 1e-3, None)) - 305.0447927307))
    c = np.stack([r, g, b], -1) / 255.0
    return np.clip(c, 0, 1)

def silhouette_figure(layer, x, y, h, color=(0, 0, 0), a=1.0, pose="stand", t=0.0, look_up=0.0):
    """A simple, well-proportioned human silhouette (8 heads tall), drawn with thick round strokes.
    pose: 'stand' | 'astronaut'. Breathing motion from t."""
    u = h / 8.0
    breathe = 0.012 * u * math.sin(t * 1.3)
    cx, base = x, y
    if pose == "astronaut":
        # helmet, torso block, backpack, limbs — floating
        hy = base - 7.3 * u
        layer.circle(cx, hy, 0.78 * u, color, a=a)
        layer.rect(cx - 0.9 * u, hy + 0.55 * u, 1.8 * u, 3.0 * u, color, a=a, rx=0.4 * u)
        layer.rect(cx - 1.25 * u, hy + 0.7 * u, 0.45 * u, 2.2 * u, color, a=a, rx=0.15 * u)  # backpack
        layer.line(cx + 0.8 * u, hy + 1.0 * u, cx + 1.9 * u, hy + 2.3 * u, color, w=0.55 * u, a=a)  # arm raised to look at wrist
        layer.line(cx + 1.9 * u, hy + 2.3 * u, cx + 1.1 * u, hy + 1.9 * u, color, w=0.5 * u, a=a)
        layer.line(cx - 0.7 * u, hy + 1.0 * u, cx - 1.6 * u, hy + 2.6 * u, color, w=0.55 * u, a=a)
        layer.line(cx - 0.45 * u, hy + 3.4 * u, cx - 0.8 * u, hy + 6.2 * u, color, w=0.62 * u, a=a)
        layer.line(cx + 0.45 * u, hy + 3.4 * u, cx + 0.9 * u, hy + 6.0 * u, color, w=0.62 * u, a=a)
        return
    # standing figure, slight look-up
    hy = base - 7.4 * u + breathe
    layer.circle(cx + look_up * 0.15 * u, hy, 0.52 * u, color, a=a)                    # head
    layer.line(cx, hy + 0.5 * u, cx, hy + 1.0 * u, color, w=0.35 * u, a=a)                # neck
    layer.rect(cx - 0.72 * u, hy + 0.9 * u, 1.44 * u, 2.9 * u, color, a=a, rx=0.45 * u)   # torso
    layer.line(cx - 0.62 * u, hy + 1.3 * u, cx - 0.85 * u, hy + 4.2 * u, color, w=0.42 * u, a=a)  # arms
    layer.line(cx + 0.62 * u, hy + 1.3 * u, cx + 0.85 * u, hy + 4.2 * u, color, w=0.42 * u, a=a)
    layer.line(cx - 0.35 * u, hy + 3.7 * u, cx - 0.42 * u, hy + 7.3 * u, color, w=0.55 * u, a=a)   # legs
    layer.line(cx + 0.35 * u, hy + 3.7 * u, cx + 0.48 * u, hy + 7.3 * u, color, w=0.55 * u, a=a)
    layer.rect(cx - 0.75 * u, hy + 7.1 * u, 0.7 * u, 0.3 * u, color, a=a, rx=0.1 * u)        # feet
    layer.rect(cx + 0.15 * u, hy + 7.1 * u, 0.75 * u, 0.3 * u, color, a=a, rx=0.1 * u)
