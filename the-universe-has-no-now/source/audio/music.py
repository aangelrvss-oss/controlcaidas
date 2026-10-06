"""Procedural score. Reads build/timeline.json for act boundaries and writes music/score.wav (48 kHz stereo).

Identity: a slow, breathing pad built from detuned sines; a celesta-like pluck motif
(the 'two clocks' motif: two notes a fifth apart, repeated); sub drones; glass shimmer
for the quantum act; a tritone for the clash; near-silence for the unknown.
"""
import os, sys, json, math, numpy as np, soundfile as sf
from synth import *

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def note(n, octv):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    return 440.0 * 2 ** ((names[n] + (octv - 4) * 12) / 12)

CHORDS = {
    "Am9": [("A", 2), ("E", 3), ("B", 3), ("C", 4)], "Fmaj7": [("F", 2), ("C", 3), ("E", 3), ("A", 3)],
    "C": [("C", 3), ("G", 3), ("E", 4)], "Gadd2": [("G", 2), ("D", 3), ("A", 3), ("B", 3)],
    "Dm": [("D", 2), ("A", 2), ("F", 3), ("D", 4)], "Bb": [("A#", 2), ("F", 3), ("D", 4)], "F": [("F", 2), ("C", 3), ("A", 3)],
    "Csus": [("C", 3), ("G", 3), ("D", 4)], "Em": [("E", 2), ("B", 2), ("G", 3)], "E5": [("E", 2), ("B", 2), ("E", 3)],
    "Edim": [("E", 2), ("A#", 2), ("G", 3)], "Ahigh": [("A", 4), ("E", 5)], "Cmaj": [("C", 3), ("G", 3), ("E", 4), ("B", 4)],
}

def pad_chord(buf, chord, t0, t1, gain=0.12, bright=0.6, attack=3.0, release=4.0, seed=0, pan_spread=0.5):
    n = sec(t1 - t0 + release)
    env = np.ones(n, np.float32)
    a = sec(attack); r = sec(release)
    env[:a] = np.linspace(0, 1, a) ** 1.5; env[n - r:] = np.linspace(1, 0, r) ** 1.2
    for k, (nm, oc) in enumerate(chord):
        x = pad_voice(note(nm, oc), n, bright=bright, seed=seed + k) * env
        x = lowpass(x, 900 + 1800 * bright)
        place(buf, stereo(x, width=0.5, pan=(-pan_spread + 2 * pan_spread * k / max(1, len(chord) - 1))), t0, gain)

def drone(buf, freq, t0, t1, gain=0.15, attack=4.0, release=4.0, seed=0):
    n = sec(t1 - t0 + release)
    env = np.ones(n, np.float32); a = sec(attack); r = sec(release)
    env[:a] = np.linspace(0, 1, a) ** 2; env[n - r:] = np.linspace(1, 0, r)
    x = (sine(freq, n) * 0.8 + sine(freq * 2, n) * 0.25 + sine(freq * 3.01, n) * 0.08) * env
    x = x * (1 + 0.08 * np.sin(2 * np.pi * 0.11 * t_axis(n)))
    place(buf, stereo(x), t0, gain)

def motif(buf, t0, root=("A", 4), gain=0.22, spacing=0.9, decay=2.4, seed=0):
    """the two-clocks motif: root, fifth, root (octave up), fifth — slow."""
    seq = [(root[0], root[1]), ("E" if root[0] == "A" else "A", root[1]), (root[0], root[1] + 1), ("E" if root[0] == "A" else "A", root[1])]
    for k, (nm, oc) in enumerate(seq):
        x = pluck(note(nm, oc), sec(decay + 0.5), decay=decay, bright=0.5, seed=seed + k)
        place(buf, stereo(x, pan=-0.25 if k % 2 == 0 else 0.25), t0 + k * spacing, gain)

def shimmer(buf, t0, t1, notes, gain=0.05, rate=5.0, seed=0):
    n = sec(t1 - t0); t = t_axis(n)
    env = np.sin(np.pi * np.clip(t / (t1 - t0), 0, 1)) ** 0.7
    rng = np.random.default_rng(seed)
    for k, (nm, oc) in enumerate(notes):
        trem = 0.5 + 0.5 * np.sin(2 * np.pi * (rate + rng.uniform(-1, 1)) * t + rng.uniform(0, 6))
        x = sine(note(nm, oc), n) * trem * env
        place(buf, stereo(x, pan=rng.uniform(-0.7, 0.7)), t0, gain)

def glass_rain(buf, t0, t1, scale, gain=0.12, density=1.6, seed=0):
    rng = np.random.default_rng(seed); t = t0
    while t < t1:
        nm, oc = scale[rng.integers(0, len(scale))]
        x = pluck(note(nm, oc), sec(2.0), decay=1.2, bright=0.8, seed=int(t * 10))
        place(buf, stereo(x, pan=rng.uniform(-0.8, 0.8)), t, gain * rng.uniform(0.5, 1.0))
        t += rng.exponential(1.0 / density)

def heartbeat_pulse(buf, t0, t1, period=2.0, gain=0.25, freq=48.0):
    t = t0
    while t < t1:
        n = sec(0.6); tt = t_axis(n)
        x = sine(freq, n) * np.exp(-tt * 9)
        place(buf, stereo(fade_io(x, 0.003, 0.1)), t, gain); t += period

def build(tl):
    acts = {}
    for s in tl["shots"]:
        a = s["act"]; acts.setdefault(a, [s["start"], s["end"]]); acts[a][1] = s["end"]
    shot = {s["id"]: s for s in tl["shots"]}
    D = tl["duration"] + 6.0
    buf = np.zeros((sec(D), 2), np.float32)
    # ---- Act I: silence, then a single drone and the motif
    a1 = acts[1]; s02 = shot["S02"]["start"]; s05 = shot["S05"]["start"]
    drone(buf, note("A", 1), s02 + 0.5, a1[1], gain=0.11, attack=6)
    motif(buf, s02 + 1.5, gain=0.16)
    motif(buf, shot["S03"]["start"] + 1.0, gain=0.10, spacing=1.1)
    pad_chord(buf, CHORDS["Am9"], s05, shot["S08"]["start"] + 2, gain=0.07, bright=0.35, attack=5)
    pad_chord(buf, CHORDS["Fmaj7"], shot["S08"]["start"] + 2, shot["S10"]["start"] + 1, gain=0.08, bright=0.4)
    pad_chord(buf, CHORDS["Gadd2"], shot["S10"]["start"] + 1, a1[1], gain=0.08, bright=0.4)
    # ---- Act II: mystery — a slow cycle
    a2 = acts[2]; prog = ["Am9", "Fmaj7", "C", "Gadd2"]
    t = a2[0]; k = 0
    while t < a2[1]:
        pad_chord(buf, CHORDS[prog[k % 4]], t, min(t + 14, a2[1]), gain=0.09, bright=0.5, attack=4, release=5, seed=k)
        t += 14; k += 1
    drone(buf, note("A", 1), a2[0], a2[1], gain=0.08)
    heartbeat_pulse(buf, shot["S14"]["start"], shot["S16"]["end"], period=1.0, gain=0.10, freq=55)
    motif(buf, shot["S17"]["start"] + 1.0, gain=0.12)
    # ---- Act III: light — grandeur, rising
    a3 = acts[3]
    stages = ["S19", "S20", "S21", "S22", "S23", "S24"]; chords3 = ["C", "Gadd2", "Dm", "F", "Bb", "Cmaj"]
    for i, sid in enumerate(stages):
        s = shot[sid]
        pad_chord(buf, CHORDS[chords3[i]], s["start"], s["end"] + 0.5, gain=0.10 + 0.012 * i, bright=0.55 + 0.07 * i, attack=2.5, release=4, seed=10 + i)
    drone(buf, note("C", 1), shot["S21"]["start"], a3[1], gain=0.10)
    shimmer(buf, shot["S22"]["start"], a3[1], [("G", 5), ("C", 6), ("E", 6), ("D", 6)], gain=0.035, rate=4.0)
    glass_rain(buf, shot["S23"]["start"], shot["S24"]["start"], [("C", 5), ("E", 5), ("G", 5), ("D", 6), ("G", 6)], gain=0.08, density=1.2, seed=3)
    # ---- Act IV: gravity — grandiosity in D minor
    a4 = acts[4]
    prog4 = ["Dm", "Bb", "F", "Csus"]; t = a4[0]; k = 0
    while t < a4[1]:
        pad_chord(buf, CHORDS[prog4[k % 4]], t, min(t + 12, a4[1]), gain=0.12, bright=0.6, attack=3.5, release=5, seed=20 + k)
        t += 12; k += 1
    drone(buf, note("D", 1), a4[0] + 2, a4[1], gain=0.13)
    motif(buf, shot["S30"]["start"] + 1.0, root=("D", 4), gain=0.10, spacing=1.0)
    # ---- Act V: black hole — tension
    a5 = acts[5]
    drone(buf, note("E", 1), a5[0], a5[1], gain=0.16, attack=8)
    pad_chord(buf, CHORDS["E5"], shot["S32"]["start"], shot["S35"]["end"], gain=0.10, bright=0.35, attack=6, release=6, seed=30)
    pad_chord(buf, CHORDS["Edim"], shot["S34"]["start"], shot["S35"]["end"], gain=0.05, bright=0.3, attack=8, release=6, seed=31)
    heartbeat_pulse(buf, shot["S33"]["start"], shot["S35"]["end"], period=2.4, gain=0.18, freq=41)
    shimmer(buf, shot["S35"]["start"], shot["S35"]["end"], [("B", 5), ("C", 6)], gain=0.03, rate=7.0)
    # the fall: strip everything, leave the drone and a slow pulse that stretches
    t = shot["S36"]["start"]; per = 1.4
    while t < shot["S36"]["end"] - 2:
        heartbeat_pulse(buf, t, t + 0.1, period=10, gain=0.16, freq=41); per *= 1.25; t += per
    # ---- Act VI: quantum — abstract textures, no bass
    a6 = acts[6]
    glass_rain(buf, a6[0] + 1, a6[1], [("A", 5), ("B", 5), ("E", 6), ("F#", 6), ("A", 6), ("C#", 6)], gain=0.07, density=2.2, seed=6)
    shimmer(buf, a6[0], a6[1], [("E", 5), ("A", 5), ("B", 5), ("E", 6)], gain=0.045, rate=6.5, seed=7)
    pad_chord(buf, CHORDS["Ahigh"], shot["S40"]["start"], a6[1], gain=0.05, bright=0.9, attack=5, release=5, seed=40)
    # ---- Act VII: entanglement — two voices, alternating sides, sharing one note
    a7 = acts[7]
    pad_chord(buf, [("E", 3), ("B", 3)], a7[0], a7[1], gain=0.08, bright=0.5, attack=5, release=5, seed=50, pan_spread=0.0)
    for i in range(int((a7[1] - a7[0]) / 6)):
        t0 = a7[0] + i * 6
        x = pluck(note("A", 5 if i % 2 == 0 else 4), sec(3.0), decay=2.2, bright=0.5, seed=60 + i)
        place(buf, stereo(x, pan=-0.8 if i % 2 == 0 else 0.8), t0, 0.14)
        x = pluck(note("E", 5), sec(3.0), decay=2.2, bright=0.5, seed=70 + i)
        place(buf, stereo(x, pan=0.8 if i % 2 == 0 else -0.8), t0 + 0.0, 0.12)   # the partner answers at the same instant
    heartbeat_pulse(buf, shot["S44"]["start"], shot["S44"]["end"], period=1.5, gain=0.07, freq=55)
    # ---- Act VIII: two great theories — immensity, then the clash
    a8 = acts[8]
    pad_chord(buf, CHORDS["Dm"], shot["S47"]["start"], shot["S47"]["end"], gain=0.12, bright=0.55, attack=3, seed=80)
    drone(buf, note("D", 1), shot["S47"]["start"], shot["S49"]["end"], gain=0.13)
    shimmer(buf, shot["S48"]["start"], shot["S48"]["end"], [("A", 5), ("D", 6), ("F#", 6)], gain=0.04, rate=8.0, seed=81)
    pad_chord(buf, CHORDS["Bb"], shot["S49"]["start"], shot["S49"]["end"], gain=0.12, bright=0.6, attack=3, seed=82)
    s50 = shot["S50"]
    pad_chord(buf, CHORDS["Dm"], s50["start"], s50["start"] + 9, gain=0.12, bright=0.6, attack=3, release=3, seed=83)
    pad_chord(buf, [("G#", 2), ("D", 3), ("G#", 3)], s50["start"] + 3, s50["start"] + 11, gain=0.10, bright=0.7, attack=6, release=1.0, seed=84)  # tritone against D
    drone(buf, note("D", 1), s50["start"], s50["start"] + 11, gain=0.15, release=0.8)
    # ---- Act IX: the unknown — almost nothing
    a9 = acts[9]
    x = sine(note("A", 5), sec(a9[1] - a9[0])) * np.exp(-t_axis(sec(a9[1] - a9[0])) / 14.0)
    place(buf, stereo(fade_io(x, 0.5, 2.0), width=0.3), a9[0] + 1.0, 0.05)
    motif(buf, shot["S52"]["start"] + 0.5, gain=0.07, spacing=1.6, decay=3.0)
    pad_chord(buf, CHORDS["Am9"], shot["S53"]["start"], shot["S54"]["end"], gain=0.06, bright=0.35, attack=8, release=6, seed=90)
    drone(buf, note("A", 1), shot["S54"]["start"], shot["S54"]["end"], gain=0.07, attack=8)
    # ---- Final
    s55, s56, s57, s58 = shot["S55"], shot["S56"], shot["S57"], shot["S58"]
    motif(buf, s55["start"] + 1.0, gain=0.14)
    drone(buf, note("A", 1), s55["start"], s56["end"], gain=0.10)
    for i, ch in enumerate(["Am9", "Fmaj7", "C", "Gadd2", "Cmaj"]):
        t0 = s56["start"] + 2 + i * 4.4
        pad_chord(buf, CHORDS[ch], t0, t0 + 5.5, gain=0.10 + 0.02 * i, bright=0.5 + 0.08 * i, attack=2.5, release=4.5, seed=100 + i)
    shimmer(buf, s56["start"] + 8, s56["end"], [("E", 6), ("A", 6), ("C", 7)], gain=0.03, rate=5.0, seed=101)
    pad_chord(buf, CHORDS["Am9"], s58["start"], s58["end"] - 3, gain=0.07, bright=0.4, attack=4, release=3, seed=110)
    motif(buf, s58["start"] + 2.0, gain=0.09, spacing=1.3, decay=3.0)
    # reverb + gentle glue
    out = reverb(buf, size=3.2, mix=0.32)
    out = softclip(out, 1.2) * 0.9
    return out[: sec(tl["duration"])]

if __name__ == "__main__":
    tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
    out = build(tl)
    os.makedirs(os.path.join(ROOT, "music"), exist_ok=True)
    sf.write(os.path.join(ROOT, "music", "score.wav"), out, SR, subtype="PCM_24")
    print("score", out.shape, "peak", np.abs(out).max())
