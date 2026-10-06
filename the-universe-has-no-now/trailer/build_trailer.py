"""Trailer pipeline: TTS lines -> timeline -> (render via nonow) -> music cue -> mix -> mux. Run steps:
   python trailer/build_trailer.py prep     (tts + timeline + audio)
   python -m nonow.render film --timeline build/trailer_timeline.json --out build/trailer_video.mp4 --workers 4 --crf 18
   python trailer/build_trailer.py mux
"""
import os, sys, json, subprocess, hashlib, numpy as np, soundfile as sf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "source", "audio")); sys.path.insert(0, os.path.join(ROOT, "source", "render")); sys.path.insert(0, os.path.join(ROOT, "trailer"))
from trailer_script import SHOTS
from synth import *

def tts():
    from kokoro_onnx import Kokoro
    from tts import post, MODELS
    k = Kokoro(os.path.join(MODELS, "kokoro-v1.0.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))
    out = os.path.join(ROOT, "voice", "trailer"); os.makedirs(out, exist_ok=True)
    meta = {}
    for s in SHOTS:
        for i, ln in enumerate(s["lines"]):
            key = f"{s['id']}_{i:02d}"
            x, sr = k.create(ln["text"], voice="af_heart", speed=0.9, lang="en-us")
            x, sr = post(np.asarray(x, dtype=np.float64), sr)
            sf.write(os.path.join(out, key + ".wav"), x, sr, subtype="PCM_16")
            meta[key] = dict(text=ln["text"], dur=round(len(x) / sr, 3))
    json.dump(meta, open(os.path.join(ROOT, "voice", "trailer_lines.json"), "w"), indent=1)
    return meta

def timeline(meta):
    from nonow import timeline as TL
    tl = TL.build(meta, shots=SHOTS)
    for k in range(1, len(tl["shots"])):
        p = tl["shots"][k - 1]; tl["shots"][k]["dip_in"] = p["trans_dur"] if p["trans"] == "dip" else 0.0
    json.dump(tl, open(os.path.join(ROOT, "build", "trailer_timeline.json"), "w"), indent=1)
    print("trailer", tl["duration"], "s")
    return tl

def audio(tl):
    from music import drone, motif, pad_chord, CHORDS, note, shimmer, heartbeat_pulse
    from sfx_track import build as sfx_build
    from mix import envelope, loudnorm, measure
    D = tl["duration"]
    buf = np.zeros((sec(D + 4), 2), np.float32)
    sh = {s["id"]: s for s in tl["shots"]}
    drone(buf, note("A", 1), sh["T02"]["start"], sh["T07"]["start"], gain=0.12, attack=2)
    motif(buf, sh["T02"]["start"] + 0.3, gain=0.16, spacing=0.7)
    pad_chord(buf, CHORDS["Am9"], sh["T03"]["start"], sh["T05"]["start"], gain=0.09, bright=0.5, attack=2, release=2)
    pad_chord(buf, CHORDS["Dm"], sh["T05"]["start"], sh["T07"]["start"], gain=0.12, bright=0.65, attack=2, release=2)
    heartbeat_pulse(buf, sh["T04"]["start"], sh["T10"]["end"], period=1.0, gain=0.14, freq=55)
    drone(buf, note("E", 1), sh["T07"]["start"], sh["T10"]["end"], gain=0.16, attack=1.5, release=0.5)
    pad_chord(buf, CHORDS["E5"], sh["T07"]["start"], sh["T09"]["end"], gain=0.11, bright=0.5, attack=2, release=2)
    shimmer(buf, sh["T08"]["start"], sh["T09"]["end"], [("E", 6), ("B", 5), ("A", 6)], gain=0.04, rate=7)
    pad_chord(buf, [("G#", 2), ("D", 3), ("G#", 3)], sh["T10"]["start"], sh["T10"]["end"] - 0.5, gain=0.12, bright=0.7, attack=2.5, release=0.3)
    drone(buf, note("A", 1), sh["T11"]["start"], sh["T12"]["end"], gain=0.10, attack=1)
    pad_chord(buf, CHORDS["Cmaj"], sh["T11"]["start"] + 0.5, sh["T12"]["start"] + 1.5, gain=0.13, bright=0.7, attack=1.5, release=2)
    motif(buf, sh["T12"]["start"] + 0.5, gain=0.14, spacing=0.9)
    music = reverb(buf, size=2.8, mix=0.3)[: sec(D)]
    sfx, _ = sfx_build(tl)
    vo = np.zeros((sec(D), 2), np.float32)
    for s in tl["shots"]:
        for ln in s["lines"]:
            x, sr = sf.read(os.path.join(ROOT, "voice", "trailer", ln["key"] + ".wav"), dtype="float32"); place(vo, stereo(x), ln["start"])
    vo = reverb(vo, size=1.1, mix=0.08)
    env = envelope(vo); duck = 1 - 0.45 * np.clip(env / 0.25, 0, 1)
    mix = softclip(vo + music * duck[:, None] * 0.95 + sfx[: sec(D)] * 0.6, 1.1)
    raw = os.path.join(ROOT, "build", "trailer_mix_raw.wav"); sf.write(raw, mix, SR, subtype="PCM_24")
    out = os.path.join(ROOT, "trailer", "trailer_mix.wav"); loudnorm(raw, out, TP=-1.5); print(measure(out))

def mux():
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, "build", "trailer_video.mp4"), "-i", os.path.join(ROOT, "trailer", "trailer_mix.wav"),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", os.path.join(ROOT, "trailer.mp4")], check=True)
    print("trailer.mp4 written")

if __name__ == "__main__":
    if sys.argv[1] == "prep":
        meta = tts(); tl = timeline(meta); audio(tl)
    else:
        mux()
