"""Pipeline consistency: timeline, narration, captions, cue sheet."""
import os, sys, json, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "source", "script"))

def load():
    return json.load(open(os.path.join(ROOT, "build", "timeline.json")))

def test_timeline_is_contiguous_and_in_range():
    tl = load(); shots = tl["shots"]
    for a, b in zip(shots, shots[1:]):
        if a["trans"] == "dissolve": assert abs(b["start"] - (a["end"] - a["trans_dur"])) < 1 / tl["fps"] + 1e-6
        else: assert abs(b["start"] - a["end"]) < 1e-6
    assert 8 * 60 <= tl["duration"] <= 12 * 60
    assert 40 <= len(shots) <= 90

def test_every_line_has_audio_and_fits_its_shot():
    tl = load()
    for s in tl["shots"]:
        for ln in s["lines"]:
            p = os.path.join(ROOT, "voice", "lines", ln["key"] + ".wav")
            assert os.path.exists(p), ln["key"]
            assert s["start"] <= ln["start"] and ln["end"] <= s["end"] + 1e-6

def test_narration_lines_do_not_overlap():
    tl = load(); lines = [ln for s in tl["shots"] for ln in s["lines"]]
    for a, b in zip(lines, lines[1:]): assert a["end"] <= b["start"] + 1e-6

def test_captions_valid_and_monotonic():
    srt = open(os.path.join(ROOT, "captions.srt")).read().strip().split("\n\n")
    prev = -1.0
    for block in srt:
        idx, times, *text = block.split("\n")
        m = re.match(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)", times)
        assert m, times
        a = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) + int(m[4]) / 1000
        b = int(m[5]) * 3600 + int(m[6]) * 60 + int(m[7]) + int(m[8]) / 1000
        assert a < b and a >= prev - 1e-3; prev = b
        assert all(len(t) <= 90 for t in text)
    vtt = open(os.path.join(ROOT, "captions.vtt")).read()
    assert vtt.startswith("WEBVTT")

def test_sfx_cues_reference_known_sounds():
    sys.path.insert(0, os.path.join(ROOT, "source", "audio"))
    from script import SHOTS
    from sfx import LIBRARY
    for s in SHOTS:
        for name in s.get("sfx", {}).values(): assert name in LIBRARY, name
