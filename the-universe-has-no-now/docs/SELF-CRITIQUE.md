# Self-critique and the iteration pass

The first full cut was watched (as frame tiles, stills and automatic measurements — this environment has no
speakers) with six hats on. What each one said, and what was changed before the final cut.

## Director — does it have personality?
Yes: one typographic voice (Inter, tracked caps for labels, mono for measured values, serif for equations),
one palette (amber = time/gravity, cyan = light/quantum, violet = the open question), black silences at act
boundaries, and a recurring two-note "clock" motif. The human moments (observers on the curved horizon,
the figure crossed by the light pulse, the astronaut drifting to the horizon, the figure before the signal
screen) are silhouettes, never presenters. **Changed:** the two observers in the wide opening shot and the three
observers in the postulates shot were nearly invisible (black on black); they are now rim-lit.

## Editor — are there shots that could go?
The cut is narration-driven, so no shot overstays its sentence. Pauses were tightened globally (×0.75) and six
sentences were cut after the first timing pass (the first assembly ran 12.5 min; the final is 11.6). The scale
act could lose the human-body stage without harm; it was kept because it is the only quiet, human-sized beat in
the act. The credits were shortened from 22 to 17 s.

## Scientist — any misleading simplification?
- The "rubber-sheet" grid is an embedding diagram; the narration never calls it a mechanism and the orbit shot
  says "as straight as it can through a geometry that is bent".
- The black hole is Schwarzschild, thin-disk, no radiative transfer. The on-screen caption says exactly that.
- The falling clock uses the static-observer redshift factor, not the full infall Doppler factor; the narration
  only claims the qualitative behaviour (slows, seems to stop), which is correct.
- The entanglement shot shows aligned-setting anti-correlations; the Bell inset carries the angle dependence.
- "Twelve decimal places" for the electron g-factor is defensible (Fan et al. 2023 vs. QED with independent α).
**Changed:** nothing in the physics; the claim matrix was extended with the simplifications list.

## Viewer — would I get bored?
The longest single idea is the black hole (≈80 s across six shots). It earns it: the camera moves, the labels
change, and the human figure arrives at the end. The weakest stretch is Act VIII's split screen (≈50 s of two
grids). It is carried by the narration and the tritone build. A future pass could add one more image there
(e.g. a Feynman diagram or the LHC event display).

## Designer — are there memorable images?
The Einstein ring forming from arcs, the Minkowski boost with the tilting present, the ray-traced far-side
arcs over the shadow, the two-slit detections resolving into fringes, the crossed-out "MESSAGE ?".
**Changed:** the accretion disk was grey-beige in the first cut (peak temperature too high); the colour
temperature profile was lowered (T_peak 4800 → 3800 K) so the disk reads amber with a blue-white approaching
side and deep-orange receding side, as the narration describes.

## Engineer — can it be reproduced?
`make all` rebuilds everything from `script.py`; every intermediate is cached and the picture render is
resumable in 600-frame segments (the container restarted once mid-render; the resumable design was added then).
Tests pin the physics (b_crit = 3√3 M, 4M/b deflection, orbital normalisation, on-screen Lorentz values) and
the deliverables (container, loudness, frozen/black-frame scan).

## Audio — measured, not heard
The mix is −14.2 LUFS integrated, LRA 5.7 LU; true peak was pushed to 0.3 dBFS by the AAC encode in the first
cut, so the loudnorm ceiling was lowered to −2.5 dBTP before the final mux. Narration sits ≈ 9–11 LU above the
score under speech (ducking) and the score rises in the silences.

## Known weaknesses that remain
- The voice is a small open-source TTS model (Kokoro-82M). It is clean and well paced but a human narrator — or
  a premium TTS — would add more intention; the sandbox's network policy blocked the only premium voice service
  available (its download CDN is denied), so it was not used.
- 1080p, not 4K: a CPU-only container; the renderer is resolution-independent.
- The "human" element is silhouettes only; no generated imagery was available, and that is a deliberate,
  consistent choice rather than a stylistic afterthought.
