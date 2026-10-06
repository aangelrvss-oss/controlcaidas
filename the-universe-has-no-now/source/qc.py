"""Automated QC of film.mp4 → docs/QC-REPORT.md (technical facts; the editorial critique is written by hand)."""
import os, json, subprocess, numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILM = os.path.join(ROOT, "film.mp4")
tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
def sh(cmd): return subprocess.run(cmd, capture_output=True, text=True)
probe = json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", FILM]).stdout)
v = next(s for s in probe["streams"] if s["codec_type"] == "video"); a = next(s for s in probe["streams"] if s["codec_type"] == "audio")
loud = sh(["ffmpeg", "-hide_banner", "-i", FILM, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
loud = loud[loud.rfind("Summary:"):]
# per-second luminance + motion
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", FILM, "-vf", "fps=2,scale=96:54", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.float32)
lum = fr.mean((1, 2)); mot = np.r_[0, np.abs(np.diff(fr, axis=0)).mean((1, 2))]
# per-second audio RMS (narration audibility check)
araw = subprocess.run(["ffmpeg", "-v", "error", "-i", FILM, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
au = np.frombuffer(araw, np.int16).astype(np.float32) / 32768
sec = len(au) // 8000; rms = np.array([np.sqrt(np.mean(au[i*8000:(i+1)*8000] ** 2) + 1e-12) for i in range(sec)])
rows = []
for s in tl["shots"]:
    i0, i1 = int(s["start"] * 2), int(s["end"] * 2)
    l = lum[i0:i1]; m = mot[i0 + 1:i1]
    r = rms[int(s["start"]):max(int(s["start"]) + 1, int(s["end"]))]
    rows.append((s["id"], s["scene"], s["end"] - s["start"], l.mean() if len(l) else 0, l.min() if len(l) else 0, m.mean() if len(m) else 0, 20 * np.log10(r.mean() + 1e-9)))
out = ["# QC REPORT — technical audit", "", f"Generated from `film.mp4` ({os.path.getsize(FILM)/2**20:.1f} MB).", "",
       "## Container", f"- video: {v['codec_name']} {v['width']}×{v['height']} @ {v['r_frame_rate']} fps, {v.get('pix_fmt')}",
       f"- audio: {a['codec_name']} {a['sample_rate']} Hz, {a['channels']} ch", f"- duration: {float(probe['format']['duration']):.2f} s", "",
       "## Loudness (EBU R128)", "```", loud.strip(), "```", "",
       "## Per-shot picture and sound statistics", "mean/min luminance (0–255, 96×54 proxy), mean frame-to-frame motion, mean audio level (dBFS RMS)", "",
       "| shot | scene | dur s | lum mean | lum min | motion | audio dBFS |", "|---|---|---|---|---|---|---|"]
flags = []
for sid, sc, d, lm, lmin, mo, db in rows:
    out.append(f"| {sid} | {sc} | {d:.1f} | {lm:.1f} | {lmin:.1f} | {mo:.2f} | {db:.1f} |")
    if mo < 0.08 and sc not in ("card", "credits"): flags.append(f"{sid}: low motion ({mo:.2f})")
    if db < -45: flags.append(f"{sid}: very quiet audio ({db:.1f} dBFS)")
out += ["", "## Automatic flags", *(["- " + f for f in flags] or ["- none"])]
os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
open(os.path.join(ROOT, "docs", "QC-REPORT.md"), "w").write("\n".join(out)); print("\n".join(out[-len(flags) - 2:]))
