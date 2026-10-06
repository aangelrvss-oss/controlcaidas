# THE UNIVERSE HAS NO NOW
### What relativity and quantum mechanics reveal about reality

A faceless, cinematic science film (≈11.5 min, 1920×1080, 24 fps, stereo −14 LUFS) produced autonomously
and entirely from code: every frame is rendered by a custom Python renderer (including a Schwarzschild
black-hole ray tracer), the narration is synthesised locally, the score and sound design are procedural.

**Deliverables**

| File | What |
|---|---|
| `film.mp4` | the film (H.264 / AAC 48 kHz) |
| `trailer.mp4` | 45-second standalone trailer |
| `short-01.mp4` … `short-03.mp4` | three 9:16 vertical cuts with burned-in captions |
| `captions.srt`, `captions.vtt` | sentence-accurate captions |
| `thumbnail.png` | 1280×720 YouTube thumbnail (master in `thumbnail/`) |
| `index.html` | local landing page (trailer, film, synopsis, method, credits, sources) |
| `STORYBOARD.md` | every shot: duration, narration, visual, camera, sound, transition |
| `SOURCES.md`, `docs/science-matrix.md` | references and a claim-by-claim confidence matrix |
| `BUILD.md`, `Makefile`, `source/`, `tests/` | full reproducible pipeline |
| `docs/QC-REPORT.md` | the quality audit and the self-critique iteration |

**Structure** — Act I The Same Moment · II Time Is Not What You Think · III Light · IV Gravity Rewrites the
Stage · V The Edge of the Black Hole · VI Then Quantum Physics Arrived · VII Entanglement · VIII Two Great
Theories · IX The Unknown · Finale.

**Honesty note** — created: all picture, voice, music, sound, captions, trailer, shorts, thumbnail, page,
tests. Not possible in this environment: external generative image/video/voice services (the sandbox's
egress policy blocks their download CDNs), so none were used. Resolution is 1080p (CPU-only container;
the renderer is resolution-independent and can be run at 4K with `--scale 2`).

Run `make all` to rebuild (see `BUILD.md`).
