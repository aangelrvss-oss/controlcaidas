"""captions.srt / captions.vtt from the timeline (sentence-level synthesis gives exact cue timing)."""
import os, json, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def split_cue(text, start, end, maxlen=84):
    if len(text) <= maxlen: return [(start, end, text)]
    # split at the best punctuation near the middle
    cands = [m.end() for m in re.finditer(r"[,;:.]\s", text)]
    mid = len(text) / 2
    if cands:
        cut = min(cands, key=lambda c: abs(c - mid))
    else:
        sp = [m.start() for m in re.finditer(r"\s", text)]; cut = min(sp, key=lambda c: abs(c - mid)) + 1
    a, b = text[:cut].strip(), text[cut:].strip()
    tm = start + (end - start) * len(a) / len(text)
    return split_cue(a, start, tm, maxlen) + split_cue(b, tm, end, maxlen)

def fmt(t, vtt=False):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", "," if not vtt else ".")

def build(tl):
    cues = []
    for s in tl["shots"]:
        for ln in s["lines"]:
            cues += split_cue(ln["text"], ln["start"], ln["end"] + 0.15, 84)
    # avoid overlaps
    for i in range(len(cues) - 1):
        if cues[i][1] > cues[i + 1][0]: cues[i] = (cues[i][0], cues[i + 1][0] - 0.02, cues[i][2])
    return cues

if __name__ == "__main__":
    tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
    cues = build(tl)
    srt = "".join(f"{i+1}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues))
    vtt = "WEBVTT\n\n" + "".join(f"{fmt(a, True)} --> {fmt(b, True)}\n{t}\n\n" for a, b, t in cues)
    open(os.path.join(ROOT, "captions.srt"), "w").write(srt); open(os.path.join(ROOT, "captions.vtt"), "w").write(vtt)
    os.makedirs(os.path.join(ROOT, "subtitles"), exist_ok=True)
    open(os.path.join(ROOT, "subtitles", "captions.srt"), "w").write(srt); open(os.path.join(ROOT, "subtitles", "captions.vtt"), "w").write(vtt)
    print(len(cues), "cues")
