"""Narration synthesis with Kokoro (local, CPU) + post-processing.

Usage: python tts.py [--voice af_heart] [--speed 0.95] [--force]
Writes voice/lines/<shot>_<i>.wav (48 kHz mono) and voice/lines.json (durations).
"""
import sys, os, json, argparse, hashlib
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "source", "script"))
from script import SHOTS

MODELS = os.environ.get("KOKORO_MODELS", os.path.join(ROOT, "build", "models"))
OUT = os.path.join(ROOT, "voice", "lines")

def post(x, sr):
    """Clean narration: resample to 48k, trim silence, HPF, gentle de-ess/compress, peak normalise."""
    if sr != 48000:
        x = resample_poly(x, 48000, sr); sr = 48000
    # trim silence (threshold -45 dBFS with 60 ms guard)
    env = np.abs(x); thr = 10 ** (-45 / 20)
    idx = np.where(env > thr)[0]
    if len(idx):
        a = max(0, idx[0] - int(0.06 * sr)); b = min(len(x), idx[-1] + int(0.12 * sr))
        x = x[a:b]
    sos = butter(2, 70, "hp", fs=sr, output="sos"); x = sosfilt(sos, x)
    # subtle presence lift 2.5-5 kHz (+1.5 dB) via parallel band-pass
    sos_bp = butter(2, [2500, 5000], "bandpass", fs=sr, output="sos")
    x = x + 0.18 * sosfilt(sos_bp, x)
    # soft-knee compression (feed-forward, RMS detector)
    win = int(0.02 * sr)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, mode="same") + 1e-12)
    thr_c = 10 ** (-18 / 20); ratio = 2.5
    gain = np.where(rms > thr_c, (thr_c * (rms / thr_c) ** (1 / ratio)) / rms, 1.0)
    # smooth gain (attack 5ms / release 80ms)
    g = np.empty_like(gain); gv = 1.0
    att = np.exp(-1 / (0.005 * sr)); rel = np.exp(-1 / (0.08 * sr))
    for i, gi in enumerate(gain):
        gv = gi + (gv - gi) * (att if gi < gv else rel); g[i] = gv
    x = x * g
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.7
    return x.astype(np.float32), sr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="af_heart"); ap.add_argument("--speed", type=float, default=0.95)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(MODELS, "kokoro-v1.0.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))
    os.makedirs(OUT, exist_ok=True)
    meta_path = os.path.join(ROOT, "voice", "lines.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    lang = "en-gb" if a.voice.startswith("b") else "en-us"
    for s in SHOTS:
        for i, ln in enumerate(s["lines"]):
            key = f"{s['id']}_{i:02d}"
            h = hashlib.md5(f"{ln['text']}|{a.voice}|{a.speed}".encode()).hexdigest()[:10]
            fn = os.path.join(OUT, key + ".wav")
            if not a.force and meta.get(key, {}).get("hash") == h and os.path.exists(fn):
                continue
            x, sr = k.create(ln["text"], voice=a.voice, speed=a.speed, lang=lang)
            x, sr = post(np.asarray(x, dtype=np.float64), sr)
            sf.write(fn, x, sr, subtype="PCM_16")
            meta[key] = dict(text=ln["text"], dur=round(len(x) / sr, 3), hash=h, voice=a.voice, speed=a.speed)
            print(key, f"{len(x)/sr:5.2f}s", ln["text"][:60])
            json.dump(meta, open(meta_path, "w"), indent=1)
    tot = sum(v["dur"] for v in meta.values())
    print("TOTAL narration", round(tot, 1), "s =", round(tot / 60, 2), "min")

if __name__ == "__main__":
    main()
