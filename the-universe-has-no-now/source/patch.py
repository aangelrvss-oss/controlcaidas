"""Re-render only the 600-frame segments that contain the given shots, then re-concatenate losslessly.
   python source/patch.py S31 S32 S33
Relies on the resumable segment layout of `nonow.render film` (build/segs/film/segNNN.mp4)."""
import os, sys, json, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHUNK = 600
ids = [a for a in sys.argv[1:] if not a.startswith("--")]
tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
S = {s["id"]: s for s in tl["shots"]}
segdir = os.path.join(ROOT, "build", "segs", "film")
affected = set()
for sid in ids:
    s = S[sid]
    for k in range(s["start_f"] // CHUNK, (s["end_f"] - 1) // CHUNK + 1): affected.add(k)
for k in sorted(affected):
    p = os.path.join(segdir, f"seg{k:03d}.mp4")
    if os.path.exists(p): os.remove(p); print("dropped", os.path.basename(p))
env = dict(os.environ, LD_LIBRARY_PATH="/root/lib")
subprocess.run([sys.executable, "-m", "nonow.render", "film", "--out", os.path.join(ROOT, "build", "film_video.mp4"), "--crf", "18",
                "--workers", "4", "--chunk", str(CHUNK), "--tag", "film"], cwd=os.path.join(ROOT, "source", "render"), env=env, check=True)
print("patched", ids)
