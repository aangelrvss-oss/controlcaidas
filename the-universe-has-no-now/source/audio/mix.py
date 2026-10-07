"""Final mix: narration (centre) + score + sfx, with music ducking under the voice, then EBU R128 loudness
normalisation to -14 LUFS integrated / -1 dBTP via ffmpeg loudnorm (two-pass, linear).  Writes audio/mix.wav."""
import os, sys, json, subprocess, numpy as np, soundfile as sf
from synth import *
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def narration_track(tl):
    buf = np.zeros((sec(tl["duration"]), 2), np.float32)
    for s in tl["shots"]:
        for ln in s["lines"]:
            x, sr = sf.read(os.path.join(ROOT, "voice", "lines", ln["key"] + ".wav"), dtype="float32")
            assert sr == SR
            place(buf, stereo(x), ln["start"])
    return buf

def envelope(x, attack=0.02, release=0.6):
    e = np.abs(x).max(1)
    out = np.empty_like(e); v = 0.0
    ca, cr = np.exp(-1 / (attack * SR)), np.exp(-1 / (release * SR))
    for i, s in enumerate(e):
        v = s + (v - s) * (ca if s > v else cr); out[i] = v
    return out

def loudnorm(inp, out, I=-14.0, TP=-1.0, LRA=11.0):
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", inp, "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(m[m.rfind("{"):m.rfind("}") + 1])
    af = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
          f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true:print_format=summary")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", inp, "-af", af, "-ar", "48000", "-c:a", "pcm_s24le", out], check=True)
    return j

def measure(path):
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = m[m.rfind("Summary:"):]
    return tail

if __name__ == "__main__":
    tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
    vo = narration_track(tl)
    music, _ = sf.read(os.path.join(ROOT, "music", "score.wav"), dtype="float32")
    sfx, _ = sf.read(os.path.join(ROOT, "sound-design", "sfx.wav"), dtype="float32")
    n = len(vo); music = music[:n]; sfx = sfx[:n]
    # a touch of room on the voice so it sits in the picture
    vo_r = reverb(vo, size=1.1, mix=0.08, predelay=0.03)
    env = envelope(vo_r)
    duck = 1.0 - 0.5 * np.clip(env / 0.25, 0, 1)
    duck_s = 1.0 - 0.3 * np.clip(env / 0.25, 0, 1)
    mix = vo_r * 1.0 + music * duck[:, None] * 0.9 + sfx * duck_s[:, None] * 0.6
    mix = softclip(mix, 1.1)
    os.makedirs(os.path.join(ROOT, "audio"), exist_ok=True)
    raw = os.path.join(ROOT, "build", "mix_raw.wav"); sf.write(raw, mix, SR, subtype="PCM_24")
    out = os.path.join(ROOT, "audio", "mix.wav")
    j = loudnorm(raw, out, TP=-2.5)
    print("pass1:", {k: j[k] for k in ("input_i", "input_tp", "input_lra")})
    print(measure(out))
