"""Tiny procedural synthesis toolkit (NumPy). 48 kHz float32 stereo."""
import math, numpy as np
from scipy.signal import butter, sosfilt, lfilter

SR = 48000

def sec(n): return int(n * SR)
def t_axis(n): return np.arange(n, dtype=np.float32) / SR

def env_adsr(n, a=0.01, d=0.1, s=0.8, r=0.3):
    e = np.zeros(n, np.float32)
    na, nd, nr = sec(a), sec(d), sec(r)
    ns = max(0, n - na - nd - nr)
    i = 0
    e[i:i + na] = np.linspace(0, 1, na, endpoint=False)[: max(0, min(na, n - i))]; i += na
    e[i:i + nd] = np.linspace(1, s, nd, endpoint=False)[: max(0, min(nd, n - i))]; i += nd
    e[i:i + ns] = s; i += ns
    e[i:i + nr] = np.linspace(s, 0, nr)[: max(0, min(nr, n - i))]
    return e

def sine(freq, n, phase=0.0, fm=None):
    t = t_axis(n)
    if fm is None: return np.sin(2 * np.pi * freq * t + phase).astype(np.float32)
    ph = 2 * np.pi * np.cumsum(freq * (1 + fm)) / SR
    return np.sin(ph + phase).astype(np.float32)

def lowpass(x, fc, order=2):
    fc = min(max(fc, 20), SR / 2 - 100)
    return sosfilt(butter(order, fc, "lp", fs=SR, output="sos"), x).astype(np.float32)
def highpass(x, fc, order=2):
    return sosfilt(butter(order, max(fc, 10), "hp", fs=SR, output="sos"), x).astype(np.float32)
def bandpass(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "bandpass", fs=SR, output="sos"), x).astype(np.float32)

def noise(n, seed=0):
    return np.random.default_rng(seed).standard_normal(n).astype(np.float32)

def pad_voice(freq, n, detune=(0.0, 0.3, -0.3, 0.7), bright=1.0, seed=0, vib=0.004):
    """Soft, slowly-moving pad: detuned sines with a few harmonics through a slow low-pass sweep."""
    t = t_axis(n)
    out = np.zeros(n, np.float32)
    rng = np.random.default_rng(seed)
    for k, dt in enumerate(detune):
        f = freq * (2 ** (dt / 1200))
        lfo = 1 + vib * np.sin(2 * np.pi * (0.07 + 0.03 * k) * t + rng.uniform(0, 6.28))
        ph = 2 * np.pi * np.cumsum(f * lfo) / SR
        out += np.sin(ph) * 0.5 + np.sin(2 * ph) * 0.18 * bright + np.sin(3 * ph) * 0.08 * bright + np.sin(4 * ph) * 0.04 * bright
    out /= len(detune)
    return out

def pluck(freq, n, decay=1.6, bright=0.6, seed=0):
    """Karplus–Strong-ish plucked tone with gentle decay (piano/celesta-like)."""
    t = t_axis(n)
    env = np.exp(-t / decay).astype(np.float32)
    out = (np.sin(2 * np.pi * freq * t) + bright * 0.5 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 3)
           + bright * 0.25 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t * 5) + 0.12 * np.sin(2 * np.pi * 4.01 * freq * t) * np.exp(-t * 8))
    att = np.minimum(1, t / 0.004)
    return (out * env * att).astype(np.float32)

def reverb(x, size=2.8, mix=0.35, seed=1, predelay=0.02):
    """Convolution with a synthetic exponentially-decaying noise IR (stereo decorrelated)."""
    n_ir = sec(size)
    rng = np.random.default_rng(seed)
    t = t_axis(n_ir)
    ir_l = rng.standard_normal(n_ir) * np.exp(-t * (6.9 / size)) * (1 - np.exp(-t * 60))
    ir_r = rng.standard_normal(n_ir) * np.exp(-t * (6.9 / size)) * (1 - np.exp(-t * 60))
    ir_l = lowpass(ir_l.astype(np.float32), 6000); ir_r = lowpass(ir_r.astype(np.float32), 6000)
    ir_l /= np.sqrt(np.sum(ir_l ** 2)) * 1.6; ir_r /= np.sqrt(np.sum(ir_r ** 2)) * 1.6
    pre = np.zeros(sec(predelay), np.float32)
    from scipy.signal import fftconvolve
    if x.ndim == 1: xl = xr = x
    else: xl, xr = x[:, 0], x[:, 1]
    wl = fftconvolve(xl, np.concatenate([pre, ir_l]))[: len(xl)]
    wr = fftconvolve(xr, np.concatenate([pre, ir_r]))[: len(xr)]
    dry = np.stack([xl, xr], 1)
    return (dry * (1 - mix) + np.stack([wl, wr], 1) * mix).astype(np.float32)

def stereo(x, width=0.0, pan=0.0):
    """Mono -> stereo with constant-power pan (-1..1) and optional Haas widening."""
    if x.ndim == 2: return x
    th = (pan + 1) / 2 * np.pi / 2
    l, r = x * math.cos(th), x * math.sin(th)
    if width > 0:
        d = sec(0.012 * width)
        r = np.concatenate([np.zeros(d, np.float32), r[:-d]]) if d < len(r) else r
    return np.stack([l, r], 1).astype(np.float32)

def place(buf, x, start_s, gain=1.0):
    """Add stereo/mono buffer x into stereo buf at time start_s."""
    i = sec(start_s)
    if x.ndim == 1: x = stereo(x)
    n = min(len(x), len(buf) - i)
    if n > 0 and i >= 0: buf[i:i + n] += x[:n] * gain
    elif i < 0:
        x = x[-i:]; n = min(len(x), len(buf))
        buf[:n] += x[:n] * gain

def softclip(x, drive=1.0):
    return np.tanh(x * drive) / math.tanh(drive)

def fade_io(x, fi=0.01, fo=0.05):
    n = len(x); a, b = sec(fi), sec(fo)
    e = np.ones(n, np.float32)
    e[:a] = np.linspace(0, 1, a); e[n - b:] = np.linspace(1, 0, b)
    return x * (e if x.ndim == 1 else e[:, None])
