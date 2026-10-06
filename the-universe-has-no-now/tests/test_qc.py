"""Technical QC of the final deliverables (run after `make film`)."""
import os, json, subprocess, pytest, numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILM = os.path.join(ROOT, "film.mp4")

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path], capture_output=True, text=True).stdout
    return json.loads(out)

@pytest.mark.skipif(not os.path.exists(FILM), reason="film.mp4 not built")
def test_film_container_and_streams():
    j = probe(FILM)
    v = next(s for s in j["streams"] if s["codec_type"] == "video"); a = next(s for s in j["streams"] if s["codec_type"] == "audio")
    assert v["codec_name"] == "h264" and v["width"] == 1920 and v["height"] == 1080
    assert v["r_frame_rate"] in ("24/1", "24000/1000")
    assert a["codec_name"] == "aac" and int(a["sample_rate"]) == 48000 and a["channels"] == 2
    dur = float(j["format"]["duration"]); assert 8 * 60 <= dur <= 12 * 60
    assert os.path.getsize(FILM) < 100 * 1024 * 1024   # GitHub file limit

@pytest.mark.skipif(not os.path.exists(FILM), reason="film.mp4 not built")
def test_film_loudness():
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", FILM, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = m[m.rfind("Summary:"):]
    I = float(tail.split("I:")[1].split("LUFS")[0]); tp = float(tail.split("Peak:")[1].split("dBFS")[0])
    assert -15.0 <= I <= -13.0, I
    assert tp <= -1.0, tp

@pytest.mark.skipif(not os.path.exists(FILM), reason="film.mp4 not built")
def test_no_frozen_or_black_runs_inside_shots():
    """Sample 1 fps; flag runs of identical frames longer than 3 s (outside intentional cards/credits) and
    completely black frames outside the dips."""
    tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", FILM, "-vf", "fps=1,scale=96:54", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    fr = np.frombuffer(out, np.uint8).reshape(-1, 54, 96).astype(np.float32)
    means = fr.mean((1, 2)); diffs = np.abs(np.diff(fr, axis=0)).mean((1, 2))
    frozen = 0
    for i, d in enumerate(diffs):
        t = i + 1
        shot = next((s for s in tl["shots"] if s["start"] <= t < s["end"]), None)
        if shot is None or shot["scene"] in ("card", "credits"): continue
        frozen = frozen + 1 if d < 0.05 else 0
        assert frozen < 4, f"frozen picture around t={t}s in {shot['id']}"
        if means[i] < 0.5:
            near_dip = (t - shot["start"] < 1.6) or (shot["end"] - t < 1.6)
            assert near_dip, f"black frame at t={t}s inside {shot['id']}"

@pytest.mark.parametrize("name,w,h,lo,hi", [("trailer.mp4", 1920, 1080, 30, 60), ("short-01.mp4", 1080, 1920, 20, 45),
                                           ("short-02.mp4", 1080, 1920, 20, 45), ("short-03.mp4", 1080, 1920, 20, 45)])
def test_secondary_deliverables(name, w, h, lo, hi):
    p = os.path.join(ROOT, name)
    if not os.path.exists(p): pytest.skip(name + " not built")
    j = probe(p); v = next(s for s in j["streams"] if s["codec_type"] == "video")
    assert v["width"] == w and v["height"] == h
    assert lo <= float(j["format"]["duration"]) <= hi
