"""Sound design library: deliberate, UI/perception/energy sounds. Space is silent — these are interfaces and transitions."""
import math, numpy as np
from synth import *

def tick(seed=0, bright=1.0):
    n = sec(0.06)
    x = noise(n, seed) * np.exp(-t_axis(n) * 180)
    x = bandpass(x, 1800 * bright, 5200 * bright) * 2.0
    x += sine(2200 * bright, n) * np.exp(-t_axis(n) * 300) * 0.4
    return fade_io(x, 0.001, 0.02).astype(np.float32)

def tick_loop(dur, period=1.0, gain=0.5, seed=0, bright=1.0, two=True):
    buf = np.zeros((sec(dur), 2), np.float32)
    t = 0.0; k = 0
    while t < dur:
        tk = tick(seed + k, bright) * gain * (0.85 + 0.15 * ((k % 2) == 0))
        place(buf, stereo(tk, pan=-0.35 if (two and k % 2 == 0) else 0.35), t)
        t += period; k += 1
    return buf

def tick_slow(dur, gain=0.5):
    """ticks whose period stretches (clock seen near the horizon)."""
    buf = np.zeros((sec(dur), 2), np.float32)
    t = 0.0; k = 0; period = 1.0
    while t < dur:
        place(buf, stereo(tick(k, 0.9) * gain), t)
        period *= 1.22; t += period; k += 1
    return buf

def pulse(freq=55.0, dur=1.8, gain=0.8):
    n = sec(dur); t = t_axis(n)
    x = sine(freq, n) * np.exp(-t * 2.2) + sine(freq * 2, n) * np.exp(-t * 5) * 0.3
    return fade_io((x * gain).astype(np.float32), 0.005, 0.2)

def pulse_hi(gain=0.5):
    n = sec(0.5); t = t_axis(n)
    x = sine(1760, n) * np.exp(-t * 14) + sine(2640, n) * np.exp(-t * 20) * 0.4
    return fade_io((x * gain).astype(np.float32), 0.002, 0.1)

def ui_in(gain=0.35, seed=0):
    n = sec(0.35); t = t_axis(n)
    f = 900 + 1400 * (1 - np.exp(-t * 20))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)
    x += bandpass(noise(n, seed), 3000, 9000) * np.exp(-t * 40) * 0.5
    return fade_io((x * gain).astype(np.float32), 0.002, 0.1)

def ui_out(gain=0.35, seed=1):
    n = sec(0.35); t = t_axis(n)
    f = 2200 - 1500 * (1 - np.exp(-t * 15))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    return fade_io((x * gain).astype(np.float32), 0.002, 0.1)

def data_tick(gain=0.3, seed=3):
    """a short burst of tiny clicks (readout)"""
    buf = np.zeros((sec(1.2), 2), np.float32)
    rng = np.random.default_rng(seed)
    for i in range(14):
        place(buf, stereo(tick(seed + i, 1.6) * gain * 0.6, pan=rng.uniform(-0.3, 0.3)), i * 0.07 + rng.uniform(0, 0.02))
    return buf

def whoosh(dur=1.6, gain=0.6, seed=5, rise=True):
    n = sec(dur); t = t_axis(n)
    x = noise(n, seed)
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    fc = (300 + 2500 * (t / dur)) if rise else (2800 - 2400 * (t / dur))
    # time-varying filter via segment processing
    out = np.zeros(n, np.float32); seg = sec(0.05)
    for i in range(0, n, seg):
        j = min(n, i + seg)
        out[i:j] = bandpass(x[i:j], max(60, fc[i] * 0.5), min(SR / 2 - 200, fc[i] * 1.5))
    out *= env
    return stereo(fade_io((out * gain).astype(np.float32), 0.02, 0.1), width=0.8)

def sub_drop(gain=0.9):
    n = sec(2.5); t = t_axis(n)
    f = 70 * np.exp(-t * 1.2) + 32
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4)
    return fade_io((x * gain).astype(np.float32), 0.005, 0.3)

def sub_swell(dur=3.5, gain=0.7):
    n = sec(dur); t = t_axis(n)
    env = np.sin(np.pi * t / dur) ** 1.5
    x = (sine(41.2, n) + 0.4 * sine(82.4, n)) * env
    return fade_io((x * gain).astype(np.float32), 0.02, 0.2)

def drone_in(dur=6.0, gain=0.5):
    n = sec(dur); t = t_axis(n)
    env = np.clip(t / (dur * 0.6), 0, 1) ** 2 * np.clip((dur - t) / (dur * 0.4), 0, 1)
    x = pad_voice(36.7, n, detune=(0, 5, -5), bright=0.4) * env
    x += lowpass(noise(n, 9), 220) * env * 0.5
    return stereo(fade_io((x * gain).astype(np.float32)), width=0.6)

def flash(gain=0.5):
    n = sec(0.8); t = t_axis(n)
    x = highpass(noise(n, 11), 3000) * np.exp(-t * 12) * 0.6 + sine(3520, n) * np.exp(-t * 8) * 0.5
    return fade_io((x * gain).astype(np.float32), 0.001, 0.2)

def detector(dur=10.0, gain=0.25, seed=21):
    """sparse random clicks: single detections / outcomes."""
    buf = np.zeros((sec(dur), 2), np.float32)
    rng = np.random.default_rng(seed); t = 0.3
    while t < dur:
        place(buf, stereo(tick(int(t * 100), 1.3) * gain, pan=rng.uniform(-0.5, 0.5)), t)
        t += rng.uniform(0.12, 0.5)
    return buf

def tick_light(dur, gain=0.3):
    return tick_loop(dur, period=2.2, gain=gain, bright=1.4, two=False)

def tick_pair(dur, gain=0.4):
    """two clocks drifting: one at 1.00 s, one at 1.12 s period."""
    a = tick_loop(dur, 1.0, gain, 0, 1.0, two=False)
    b = tick_loop(dur, 1.12, gain, 100, 0.8, two=False)
    return a * np.array([1.0, 0.2], np.float32) + b * np.array([0.2, 1.0], np.float32)

def whoosh_long(gain=0.6):
    return whoosh(5.0, gain, 7, rise=True)

def whoosh_soft(gain=0.4):
    return whoosh(1.4, gain, 8, rise=True)

LIBRARY = dict(tick_loop=lambda d: tick_loop(d), tick_slow=lambda d: tick_slow(d), pulse_low=lambda d: pulse(), pulse_hi=lambda d: pulse_hi(),
               ui_in=lambda d: ui_in(), ui_out=lambda d: ui_out(), data_tick=lambda d: data_tick(), whoosh_soft=lambda d: whoosh_soft(),
               whoosh_long=lambda d: whoosh_long(), sub_drop=lambda d: sub_drop(), sub_swell=lambda d: sub_swell(), drone_in=lambda d: drone_in(),
               flash=lambda d: flash(), detector=lambda d: detector(min(d, 14.0)), tick_light=lambda d: tick_light(d), tick_pair=lambda d: tick_pair(d))
