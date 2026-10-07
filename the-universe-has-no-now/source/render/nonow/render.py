"""Frame renderer / CLI.

  python -m nonow.render still  --t 12.5 --out x.png [--scale 0.5]
  python -m nonow.render shot   --id S31 --out build/prev/S31.mp4 [--scale 0.5] [--fps 12]
  python -m nonow.render film   --out build/film_video.mp4 [--workers 4] [--scale 1]
  python -m nonow.render frames --from 0 --to 100 --out seg.mp4
"""
import os, sys, json, argparse, subprocess, time, math, importlib
import numpy as np
from multiprocessing import Pool
from .core import finish, P
from . import timeline as TL

ROOT = TL.ROOT
W0, H0 = 1920, 1080

class Ctx:
    def __init__(self, W, H, fps, aspect="16:9"):
        self.W, self.H, self.fps = W, H, fps
        self.cache = {}
        self.vertical = H > W

_SCENES = {}
def scene_fn(name):
    if name not in _SCENES:
        mod = importlib.import_module(f"nonow.scenes.{name}")
        _SCENES[name] = mod.render
    return _SCENES[name]

def render_shot_frame(ctx, shot, lt):
    fn = scene_fn(shot["scene"])
    dur = shot["end"] - shot["start"]
    return fn(ctx, lt, dur, shot["params"], shot)

def render_frame(ctx, tl, frame):
    parts = TL.frame_lookup(tl, frame)
    H, W = ctx.H, ctx.W
    acc = np.zeros((H, W, 3), np.float32)
    seed = frame
    bs, vig = 0.35, 0.4
    for shot, lt, w in parts:
        if w <= 0: continue
        f = render_shot_frame(ctx, shot, lt)
        f = f * (w * TL.dip_weight(shot, lt))
        acc += f
        bs = shot["params"].get("bloom", 0.35); vig = shot["params"].get("vignette", 0.4)
    return finish(acc, seed=seed, bloom_strength=bs, vig=vig)

def ffmpeg_writer(path, W, H, fps, crf=17, preset="medium"):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-an", "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", path]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

def _render_range(args):
    tl, f0, f1, out, scale, fps_out, crf = args
    W, H = int(W0 * scale) // 2 * 2, int(H0 * scale) // 2 * 2
    if tl.get("vertical"): W, H = int(1080 * scale) // 2 * 2, int(1920 * scale) // 2 * 2
    ctx = Ctx(W, H, tl["fps"])
    step = max(1, int(round(tl["fps"] / fps_out)))
    p = ffmpeg_writer(out, W, H, fps_out, crf=crf)
    t0 = time.time(); n = 0
    for fr in range(f0, f1, step):
        img = render_frame(ctx, tl, fr)
        p.stdin.write(img.tobytes()); n += 1
        if n % 50 == 0:
            el = time.time() - t0
            print(f"[{os.path.basename(out)}] {n}/{(f1-f0)//step} frames, {el/n:.2f}s/frame, eta {el/n*((f1-f0)//step-n)/60:.1f} min", flush=True)
    p.stdin.close(); p.wait()
    return out

def load_tl(path=None):
    return json.load(open(path or os.path.join(ROOT, "build", "timeline.json")))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["still", "shot", "film", "frames"])
    ap.add_argument("--t", type=float, default=0.0); ap.add_argument("--id"); ap.add_argument("--out")
    ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--fps", type=float, default=None)
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--from", dest="f0", type=int, default=0)
    ap.add_argument("--to", dest="f1", type=int, default=None); ap.add_argument("--timeline", default=None)
    ap.add_argument("--crf", type=int, default=17); ap.add_argument("--chunk", type=int, default=600); ap.add_argument("--tag", default="film"); ap.add_argument("--lt", type=float, default=None,
                    help="for still: local time inside --id shot")
    a = ap.parse_args()
    tl = load_tl(a.timeline)
    fps_out = a.fps or tl["fps"]
    if a.mode == "still":
        W, H = int(W0 * a.scale) // 2 * 2, int(H0 * a.scale) // 2 * 2
        if tl.get("vertical"): W, H = int(1080 * a.scale) // 2 * 2, int(1920 * a.scale) // 2 * 2
        ctx = Ctx(W, H, tl["fps"])
        if a.id:
            shot = next(s for s in tl["shots"] if s["id"] == a.id)
            fr = int(round((shot["start"] + (a.lt or 0.0)) * tl["fps"]))
        else:
            fr = int(round(a.t * tl["fps"]))
        t0 = time.time(); img = render_frame(ctx, tl, fr)
        from PIL import Image; Image.fromarray(img).save(a.out); print("saved", a.out, f"{time.time()-t0:.2f}s")
    elif a.mode == "shot":
        shot = next(s for s in tl["shots"] if s["id"] == a.id)
        _render_range((tl, shot["start_f"], shot["end_f"], a.out, a.scale, fps_out, a.crf))
    elif a.mode == "frames":
        _render_range((tl, a.f0, a.f1 or tl["frames"], a.out, a.scale, fps_out, a.crf))
    else:
        # resumable chunked render: ~chunk frames per segment, written to .part and renamed when complete
        N = a.f1 or tl["frames"]; chunk = a.chunk
        bounds = list(range(a.f0, N, chunk)) + [N]
        segdir = os.path.join(ROOT, "build", "segs", a.tag); os.makedirs(segdir, exist_ok=True)
        jobs = []; segs = []
        for i in range(len(bounds) - 1):
            seg = os.path.join(segdir, f"seg{i:03d}.mp4"); segs.append(seg)
            if os.path.exists(seg) and _complete(seg, bounds[i + 1] - bounds[i], fps_out, tl["fps"]):
                continue
            jobs.append((tl, bounds[i], bounds[i + 1], seg + ".part.mp4", a.scale, fps_out, a.crf))
        print(f"{len(segs)} segments, {len(jobs)} to render", flush=True)
        if jobs:
            with Pool(a.workers) as pool:
                for done in pool.imap_unordered(_render_range, jobs):
                    os.replace(done, done.replace(".part.mp4", ""))
                    print("completed", os.path.basename(done), flush=True)
        lst = os.path.join(segdir, "list.txt")
        open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", a.out], check=True)
        print("wrote", a.out)

def _complete(path, nframes, fps_out, fps):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets",
                              "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
        step = max(1, int(round(fps / fps_out)))
        return int(out) == len(range(0, nframes, step))
    except Exception:
        return False

if __name__ == "__main__":
    main()
