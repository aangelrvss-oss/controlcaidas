"""Re-render selected shots and splice them into build/film_video.mp4 without re-rendering the whole film.
   python source/patch.py S31 S32 S33 [--workers 4]
Clips are rendered with nonow.render (same settings), then the master is rebuilt with ffmpeg's concat
filter (one re-encode at CRF 18)."""
import os, sys, json, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ids = [a for a in sys.argv[1:] if not a.startswith("--")]
tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
S = {s["id"]: s for s in tl["shots"]}
fps = tl["fps"]
# group consecutive shots into contiguous frame ranges (dissolve overlaps are handled by the renderer)
ranges = []
for sid in ids:
    s = S[sid]; f0, f1 = s["start_f"], s["end_f"]
    if ranges and f0 <= ranges[-1][1]: ranges[-1][1] = max(ranges[-1][1], f1)
    else: ranges.append([f0, f1])
clips = []
for k, (f0, f1) in enumerate(ranges):
    out = os.path.join(ROOT, "build", "segs", f"patch{k:02d}.mp4")
    env = dict(os.environ, LD_LIBRARY_PATH="/root/lib")
    subprocess.run([sys.executable, "-m", "nonow.render", "frames", "--from", str(f0), "--to", str(f1), "--out", out, "--crf", "18"],
                   cwd=os.path.join(ROOT, "source", "render"), env=env, check=True)
    clips.append((f0, f1, out))
master = os.path.join(ROOT, "build", "film_video.mp4")
inputs = ["-i", master]; parts = []; cur = 0; n = 0
for f0, f1, clip in clips:
    if f0 > cur: parts.append(f"[0:v]trim=start_frame={cur}:end_frame={f0},setpts=PTS-STARTPTS[p{n}]"); n += 1
    inputs += ["-i", clip]; parts.append(f"[{len(inputs)//2 - 1 + 0}:v]setpts=PTS-STARTPTS[p{n}]"); n += 1
    cur = f1
parts.append(f"[0:v]trim=start_frame={cur},setpts=PTS-STARTPTS[p{n}]"); n += 1
fc = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
out = os.path.join(ROOT, "build", "film_video_patched.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", str(fps), "-movflags", "+faststart", out], check=True)
os.replace(out, master); print("patched", ids, "->", master)
