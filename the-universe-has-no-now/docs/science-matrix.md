# Science claim matrix

Confidence levels: **established** (textbook, repeatedly confirmed), **well-supported** (strong evidence, standard interpretation),
**active research** (serious but unconfirmed), **speculative**. Every narrated claim is listed with the shot where it appears.

| Shot | Claim (as narrated / shown) | Confidence | Source / reasoning |
|---|---|---|---|
| S04 | A universal "now" shared by everyone is, strictly, not true | established | Relativity of simultaneity (Einstein 1905; Lorentz transformation t′ = γ(t − vx/c²)) |
| S06 | Laws of physics identical in every inertial frame; c the same for all observers | established | Einstein's two postulates (1905); c fixed by SI definition |
| S08–S10 | Light from the ship's midpoint reaches both walls together on board, the back wall first from the platform; neither frame is wrong | established | Einstein's train/embankment argument; both arrival times computed on screen from the same c |
| S12 | Moving clocks tick slowly, moving rulers are shorter (γ = 1.25 at 0.6c) | established | Lorentz transformation; light-clock derivation (Lewis & Tolman 1909; Langevin) |
| S13–S15 | Spacetime diagram; light at 45°; light cones; "elsewhere" has no frame-independent before/after | established | Minkowski 1908; Taylor & Wheeler |
| S16 | Changing velocity tilts the slice called "the present"; distant simultaneous events can swap order (t′(A) = +1.98 s, t′(B) = −1.98 s at v = 0.55c, x = ±3 ls) | established | Direct Lorentz calculation (checked in `tests/test_physics.py`) |
| S17 | GPS satellite clocks run ≈ +38 µs/day (−7 velocity, +45 gravity); uncorrected error ≈ 10 km/day | established | Ashby 2003; NIST |
| S19–S23 | Light-crossing times: atom ~3×10⁻¹⁹ s; human ~6 ns; Earth 7.5 laps/s (0.134 s/lap); Moon 1.3 s; Sun 8.3 min; Neptune ~4.1 h; Voyager ~23 h; Proxima 4.2 yr; galaxy ~100 000 yr; oldest light 13.8 Gyr | established | d / c with standard distances (SOURCES.md) |
| S24 | Every sky image is a superposition of different pasts; no single "now" to look at | established | Finite c + relativity of simultaneity |
| S26–S28 | Gravity as spacetime geometry; orbits as geodesics (as straight as possible) | established | Einstein 1915; geodesic equation. The grid is an *embedding diagram* (a pedagogical picture), labelled as geometry not as a literal sheet |
| S27 | Gμν + Λgμν = (8πG/c⁴)Tμν | established | Einstein field equations |
| S29 | Light bends; galaxies behind clusters become arcs and rings | established | Eddington 1919; Einstein ring lensing. Shown with the point-mass lens equation (exact for a point mass; clusters are extended, so real arcs differ in detail) |
| S30 | Clocks deeper in a gravitational well run slower; measured for Δh = 33 cm in 2010 | established | Chou et al., *Science* 2010 (4.1 ± 1.6 × 10⁻¹⁷ shift). On-screen rate difference is exaggerated and labelled as such |
| S31 | Event horizon: a boundary from which no path leads out, not even for light | established | Schwarzschild solution; r_s = 2GM/c² |
| S32 | "This image is computed, not painted; every pixel is a path of light traced through Schwarzschild geometry" | established (method) | `bh.py`: null geodesics from the Binet equation u″ + u = 3Mu²; validated b_crit = 3√3 M (test). The disk is a *simplified* thin Keplerian disk with a Shakura–Sunyaev profile; no spin (Kerr) and no radiative transfer |
| S33 | Far side of the disk is lensed over and under the hole | established | Luminet 1979; James et al. 2015 |
| S34 | Approaching side brighter and bluer (Doppler beaming + gravitational redshift) | established | g = √(1 − 3M/r)/(1 − Ω L_z); intensity ∝ g³ (Luminet 1979) |
| S35 | Photon ring; EHT ring around M87* (2019) and Sgr A* (2022); shadow ≈ 5.2 r_s | established | EHT 2019, 2022; shadow diameter 2√27 GM/c². Note: the EHT image resolves the lensed emission ring, with the thin photon ring unresolved inside it |
| S36 | A distant observer sees a falling clock slow and (asymptotically) stop; the faller notices nothing special at the crossing | established | Gravitational redshift √(1 − 2M/r) for static observers; equivalence principle. On screen the rate shown is the static-observer factor, a simplification of the full infall Doppler factor |
| S38–S39 | Electrons are not planets; described by |ψ|² clouds; nodal surfaces | established | Schrödinger 1926; clouds are random samples of the exact hydrogen |ψ_nlm|² (1s, 2p_z, 3d_z²) |
| S40 | Superposition; single detections build interference; probabilities = |ψ₁ + ψ₂|² | established | Feynman Lectures III; Tonomura et al. 1989 (single-electron build-up) |
| S41 | Δx·Δp ≥ ħ/2 is a property of waves (Fourier pair), not of instruments | established | Kennard 1927 |
| S43–S44 | Entangled pair outcomes individually random, correlated beyond any local hidden-variable model (Bell) | established | Bell 1964; Aspect 1982; loophole-free tests 2015; Nobel 2022. The on-screen curve −cos θ vs the linear bound is the standard singlet correlation vs the CHSH/Bell linear local bound at aligned/mis-aligned settings |
| S45 | Nothing travels between them; no choice of outcome → no message; nothing faster than light | established | No-communication theorem (Ghirardi–Rimini–Weber 1980) |
| S47 | GR predicted light bending, clock slowing, black holes, gravitational waves (2015) | established | Eddington 1919; Pound–Rebka 1960; EHT; LIGO GW150914 |
| S48 | QFT predicts the electron g-factor to twelve decimal places | well-supported | Fan et al. 2023: g/2 measured to 1.3 × 10⁻¹³; theory–experiment agreement at the 10⁻¹² level given α; the film says "twelve decimal places" |
| S49 | Different ontologies: dynamic spacetime vs fixed background with uncertain fields | established (as description) | Standard formulations; QFT in curved spacetime is a partial bridge, not mentioned to keep the point crisp |
| S50 | Quantising gravity perturbatively yields non-renormalisable infinities; harmless at ordinary energies (effective theory); fails at black-hole centres and the first instant | established / well-supported | Goroff–Sagnotti 1986; Burgess 2004. "Stop making predictions" refers to the breakdown of the effective description, phrased carefully |
| S52 | String theory, loop quantum gravity, emergent spacetime | active research / speculative | Presented with an explicit ACTIVE RESEARCH tag; none has a confirmed prediction |
| S53 | None has made a confirmed prediction; they are not established physics | established (status) | SEP "Quantum Gravity" 2024 |
| S54 | Summary thesis | established | as above |

## Known simplifications (deliberate, labelled where visible)
- Black hole: Schwarzschild (non-rotating), thin opaque disk, no radiative transfer, no spin-induced asymmetry. Camera orbits are not geodesic.
- Lensing scene: point-mass lens; real cluster lenses are extended mass distributions.
- Gravity grid: an embedding/"rubber sheet" picture, labelled as geometry rather than as a literal mechanism, used only for the geodesic intuition.
- GPS: the ±7/45 µs numbers are rounded daily averages for the nominal GPS orbit.
- Light clock speed 0.6c and Minkowski boost 0.55c are illustrative choices.
- Entanglement scene: outcomes displayed for aligned settings (perfect anti-correlation); the Bell curve inset carries the angle dependence.
