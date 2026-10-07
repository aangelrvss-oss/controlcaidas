"""Three vertical (9:16) social cuts from the finished film: 16:9 picture centred, title above, burned-in captions below.
Each has a hook (title), development (the segment) and payoff (closing line)."""
import os, sys, json, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
S = {s["id"]: s for s in tl["shots"]}
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"; FONT2 = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
CUTS = [
 ("short-01", "The ship that broke 'now'", "Simultaneity depends on how you move.", S["S08"]["start"], S["S10"]["end"] - 0.3),
 ("short-02", "This black hole is computed, not painted", "Light paths traced through Einstein's geometry.", S["S32"]["start"], S["S34"]["end"]),
 ("short-03", "Entanglement can't send a message", "Correlation is not communication.", S["S44"]["start"] + 5.0, S["S45"]["end"] - 0.5),
]
def esc(s): return s.replace("'", "’").replace(":", "\\:").replace(",", "\\,")
def cues_for(a, b):
    out = []
    for s in tl["shots"]:
        for ln in s["lines"]:
            if ln["end"] > a and ln["start"] < b:
                out.append((max(0.0, ln["start"] - a), min(b - a, ln["end"] - a + 0.2), ln["text"]))
    return out
def wrap(t, n=34):
    words = t.split(); lines = []; cur = ""
    for w in words:
        if len(cur) + len(w) + 1 > n: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur); return "\n".join(lines)
for name, hook, payoff, a, b in CUTS:
    dur = b - a
    assert 20 <= dur <= 45, (name, dur)
    vf = [f"trim=start={a}:end={b},setpts=PTS-STARTPTS", "scale=1080:608", "pad=1080:1920:0:656:color=0x05060a"]
    vf.append(f"drawtext=fontfile={FONT}:text='{esc(wrap(hook, 24))}':fontcolor=0xEBEAE6:fontsize=66:x=(w-text_w)/2:y=330:line_spacing=12")
    vf.append(f"drawtext=fontfile={FONT2}:text='THE UNIVERSE HAS NO NOW':fontcolor=0x8C8E96:fontsize=28:x=(w-text_w)/2:y=250")
    for (c0, c1, txt) in cues_for(a, b):
        vf.append(f"drawtext=fontfile={FONT2}:text='{esc(wrap(txt))}':fontcolor=0xF5B45A:fontsize=46:x=(w-text_w)/2:y=1380:line_spacing=12:enable='between(t,{c0:.2f},{c1:.2f})'")
    vf.append(f"drawtext=fontfile={FONT2}:text='{esc(payoff)}':fontcolor=0xEBEAE6:fontsize=40:x=(w-text_w)/2:y=1620:enable='gte(t,{dur-6:.2f})'")
    af = f"atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={dur-1.0}:d=1.0"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, "build", "film_master.mp4"), "-vf", ",".join(vf), "-af", af,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", os.path.join(ROOT, name + ".mp4")], check=True)
    print(name, f"{dur:.1f}s")
