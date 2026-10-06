"""Lay out the sound-design cue sheet from the timeline (shot sfx dicts) into sound-design/sfx.wav."""
import os, json, numpy as np, soundfile as sf
from synth import *
from sfx import LIBRARY
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def build(tl):
    buf = np.zeros((sec(tl["duration"] + 4), 2), np.float32)
    cues = []
    for s in tl["shots"]:
        dur = s["end"] - s["start"]
        for lt, name in s["sfx"].items():
            lt = float(lt)
            x = LIBRARY[name](dur - lt)
            if x.ndim == 1: x = stereo(x)
            # loops are cut to the shot and faded out at its end
            n = min(len(x), sec(dur - lt + 0.3))
            x = fade_io(x[:n], 0.0, min(0.6, (n / SR) * 0.3))
            place(buf, x, s["start"] + lt)
            cues.append((s["id"], round(s["start"] + lt, 2), name))
    return buf[: sec(tl["duration"])], cues

if __name__ == "__main__":
    tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
    buf, cues = build(tl)
    os.makedirs(os.path.join(ROOT, "sound-design"), exist_ok=True)
    sf.write(os.path.join(ROOT, "sound-design", "sfx.wav"), buf, SR, subtype="PCM_24")
    json.dump(cues, open(os.path.join(ROOT, "sound-design", "cues.json"), "w"), indent=1)
    print("sfx", buf.shape, "peak", np.abs(buf).max(), len(cues), "cues")
