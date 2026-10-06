"""Timeline: turns the shot list + measured narration durations into absolute times.

Writes build/timeline.json: shots with start/end (picture), transitions, and
each narration line's absolute start/end — the single source of truth for the
picture render, the music/sfx cue sheet and the captions.
"""
import os, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "source", "script"))
from script import SHOTS, ACTS, TAIL_SCALE

FPS = 24

def build(lines_meta, fps=FPS, shots=SHOTS):
    t = 0.0
    out = []
    prev_trans = ("cut", 0.0)
    for s in shots:
        kind, d = prev_trans
        overlap = d if kind == "dissolve" else 0.0
        start = t - overlap
        tl = start + s["lead"]
        lines = []
        for i, ln in enumerate(s["lines"]):
            key = f"{s['id']}_{i:02d}"
            dur = lines_meta[key]["dur"]
            lines.append(dict(key=key, text=ln["text"], start=round(tl, 3), end=round(tl + dur, 3)))
            tl += dur + ln["pause"]
        narr_end = tl + s["tail"] * TAIL_SCALE if s["lines"] else start
        end = max(start + s["min_dur"], narr_end)
        # snap to frames
        start_f = int(round(start * fps)); end_f = int(round(end * fps))
        tk, td = (s["trans"].split(":") + ["0"])[:2]; td = float(td)
        out.append(dict(id=s["id"], act=s["act"], act_name=ACTS[s["act"]], scene=s["scene"], params=s["params"],
                        start=start_f / fps, end=end_f / fps, start_f=start_f, end_f=end_f,
                        trans=tk, trans_dur=td, lines=lines, sfx=s.get("sfx", {}), notes=s.get("notes", "")))
        t = end_f / fps
        prev_trans = (tk, td)
    return dict(fps=fps, duration=t, frames=int(round(t * fps)), shots=out)

def frame_lookup(tl, frame):
    """Return list of (shot, local_t, weight) contributing to a frame (1 or 2 entries)."""
    fps = tl["fps"]; T = frame / fps
    res = []
    shots = tl["shots"]
    for k, s in enumerate(shots):
        if s["start_f"] <= frame < s["end_f"]:
            lt = T - s["start"]
            w = 1.0
            # dissolve: overlap with the next shot
            if s["trans"] == "dissolve" and k + 1 < len(shots):
                n = shots[k + 1]
                if T >= n["start"]:
                    a = (T - n["start"]) / max(1e-6, s["trans_dur"])
                    w = 1 - a
            res.append((s, lt, w))
        elif s["trans"] == "dissolve" and k + 1 < len(shots) and shots[k+1]["start_f"] <= frame < s["end_f"]:
            pass
    # dissolve: the next shot also contributes before its own start_f? No: next.start == this.end - d, so both match.
    if len(res) == 2:
        (s0, lt0, w0), (s1, lt1, w1) = res
        res = [(s0, lt0, w0), (s1, lt1, 1 - w0)]
    return res

def dip_weight(s, lt):
    """Black dip at the end (fade out over trans_dur/2) and at the start of shots preceded by a dip."""
    w = 1.0
    if s["trans"] == "dip":
        d = s["trans_dur"] / 2
        rem = s["end"] - s["start"] - lt
        if rem < d: w *= max(0.0, rem / d)
    if s.get("dip_in", 0) > 0:
        d = s["dip_in"] / 2
        if lt < d: w *= max(0.0, lt / d)
    return w

def main():
    meta = json.load(open(os.path.join(ROOT, "voice", "lines.json")))
    tl = build(meta)
    # annotate dip-in for shots that follow a dip
    for k in range(1, len(tl["shots"])):
        p = tl["shots"][k - 1]
        tl["shots"][k]["dip_in"] = p["trans_dur"] if p["trans"] == "dip" else 0.0
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    json.dump(tl, open(os.path.join(ROOT, "build", "timeline.json"), "w"), indent=1)
    print(f"{len(tl['shots'])} shots, {tl['frames']} frames, {tl['duration']/60:.2f} min")
    for s in tl["shots"]:
        print(f"{s['id']} {s['start']:7.2f} - {s['end']:7.2f}  {s['scene']:12s} {s['params']}")

if __name__ == "__main__":
    main()
