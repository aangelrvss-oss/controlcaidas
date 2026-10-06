"""Generate STORYBOARD.md from the shot list + timeline (single source of truth)."""
import os, json, sys
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, os.path.join(ROOT, "source", "script"))
from script import SHOTS, ACTS
tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
T = {s["id"]: s for s in tl["shots"]}
MUSIC = {1: "near-silence → A1 drone + two-clocks motif (celesta), first pads", 2: "mystery: slow Am9–Fmaj7–C–Gadd2 cycle, heartbeat pulse",
         3: "grandeur: brighter pads rising stage by stage, shimmer, glass arpeggios", 4: "grandiosity: D minor pads, deep drone",
         5: "tension: E drone, power chord, diminished colour, slow 41 Hz pulse; stripped for the fall", 6: "abstract: glass rain, tremolo shimmer, no bass",
         7: "two voices answering from opposite sides, one shared note", 8: "immensity: Dm/Bb pads + drone; tritone builds and cuts",
         9: "almost silence: a single decaying A5 sine, sparse motif", 10: "the motif returns; pads swell on the pull-back; silence; soft credits"}
CAM = {"card": "static", "two_clocks": "slow push-in", "postulates": "static, elements animate", "ship_flash": "static (platform frame: ship travels)",
       "light_clock": "static; moving clock travels across", "minkowski": "static diagram; boost shears the grid", "gps": "Earth rotates, satellites orbit",
       "scale": "slow zoom-out within each stage; dissolves between stages", "gravity_grid": "slow yaw around the well", "lensing": "lens crosses the field",
       "clock_tower": "static", "blackhole": "see notes (ray-traced camera path)", "orbital": "cloud rotates", "double_slit": "static", "uncertainty": "static",
       "entangle": "static; particles separate", "split": "static halves; seam", "frontier": "static", "final_zoom": "continuous pull-back", "credits": "roll"}
out = ["# STORYBOARD — THE UNIVERSE HAS NO NOW", "", f"{len(SHOTS)} shots · {tl['duration']/60:.1f} min · 1920×1080 · 24 fps", "",
       "Durations are the final picture durations (narration-driven). Times are absolute film times.", ""]
act = None
for s in SHOTS:
    t = T[s["id"]]
    if s["act"] != act:
        act = s["act"]; out += [f"\n## ACT {act} — {ACTS[act]}", f"*Music:* {MUSIC[act]}", ""]
    out.append(f"### SHOT {s['id'][1:]}  ·  {t['start']:.1f}s → {t['end']:.1f}s")
    out.append(f"Duration: {t['end']-t['start']:.1f} sec")
    out.append("")
    out.append("Narration:")
    out += [f'> "{ln["text"]}"' for ln in s["lines"]] or ["> (none — silence)"]
    out.append("")
    out.append(f"Visual: `{s['scene']}` {json.dumps(s['params']) if s['params'] else ''}")
    if s.get("notes"): out.append(f"Notes: {s['notes']}")
    out.append(f"Camera: {CAM.get(s['scene'], '')}")
    sfx = ", ".join(f"{v} @{k}s" for k, v in s.get("sfx", {}).items())
    out.append(f"Sound: {sfx or 'score only'}")
    out.append(f"Transition out: {s['trans']}")
    out.append("")
open(os.path.join(ROOT, "STORYBOARD.md"), "w").write("\n".join(out))
print("STORYBOARD.md written", len(out), "lines")
