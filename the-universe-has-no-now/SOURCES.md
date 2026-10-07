# SOURCES

Primary and institutional sources used to write and check the narration, the on-screen values
and the simulations. Each claim in the film is tagged in `docs/science-matrix.md`.

## Special relativity
- A. Einstein, "Zur Elektrodynamik bewegter Körper", *Annalen der Physik* 17, 891 (1905). English: *On the Electrodynamics of Moving Bodies* — the two postulates, relativity of simultaneity (train/embankment argument), time dilation, length contraction.
- E. F. Taylor & J. A. Wheeler, *Spacetime Physics*, 2nd ed., W. H. Freeman (1992) — Minkowski diagrams, light cones, hyperbolic rotation (boost) of simultaneity lines.
- OpenStax *University Physics III*, ch. 5 "Relativity" (LibreTexts) — Lorentz transformation, worked examples for simultaneity. https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_(OpenStax)/University_Physics_III_-_Optics_and_Modern_Physics_(OpenStax)/05%3A__Relativity
- Wikipedia, "Relativity of simultaneity", "Time dilation", "Special relativity" (used for cross-checking formulas and the GPS numbers, not as primary sources).

## Experimental tests of time dilation
- C. W. Chou, D. B. Hume, T. Rosenband, D. J. Wineland, "Optical Clocks and Relativity", *Science* 329, 1630 (2010) — Al⁺ optical clocks: time dilation at < 10 m/s and gravitational dilation for Δh = 33 cm; δf/f = gΔh/c² ≈ 1.1 × 10⁻¹⁶ per metre. https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=905055
- J. C. Hafele & R. E. Keating, "Around-the-World Atomic Clocks", *Science* 177, 166/168 (1972).
- N. Ashby, "Relativity in the Global Positioning System", *Living Reviews in Relativity* 6, 1 (2003) — satellite clocks: −7 µs/day (velocity) + 45 µs/day (gravitational potential) ≈ +38 µs/day net.
- NIST, "Putting Einstein to the Test With the World's Most Accurate Clocks" (Taking Measure blog) — the 38 µs/day figure and the ~10 km/day positioning error if uncorrected. https://www.nist.gov/blogs/taking-measure/putting-einstein-test-worlds-most-accurate-clocks

## General relativity and black holes
- A. Einstein, "Die Feldgleichungen der Gravitation", *Sitzungsber. Preuss. Akad. Wiss.* (1915), 844–847.
- K. Schwarzschild, "Über das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie", *Sitzungsber. Preuss. Akad. Wiss.* (1916), 189–196 — the metric used by the film's ray tracer.
- C. W. Misner, K. S. Thorne, J. A. Wheeler, *Gravitation*, W. H. Freeman (1973) — photon orbits in Schwarzschild: photon sphere r = 3M, critical impact parameter b = 3√3 M; "mass tells spacetime how to curve, spacetime tells mass how to move" (Wheeler's phrasing).
- J.-P. Luminet, "Image of a spherical black hole with thin accretion disk", *Astron. Astrophys.* 75, 228 (1979) — first computed image; Doppler/gravitational shift of a Keplerian thin disk (the g-factor used in `bh.py`).
- N. I. Shakura & R. A. Sunyaev, "Black holes in binary systems. Observational appearance", *Astron. Astrophys.* 24, 337 (1973) — thin-disk radial emission profile ∝ r⁻³(1 − √(r_in/r)).
- O. James, E. von Tunzelmann, P. Franklin, K. S. Thorne, "Gravitational lensing by spinning black holes in astrophysics, and in the movie Interstellar", *Class. Quantum Grav.* 32, 065001 (2015) — what makes a black-hole image recognisable: lensed far-side arcs, photon ring, Doppler asymmetry.
- Event Horizon Telescope Collaboration, "First M87 Event Horizon Telescope Results. I–VI", *ApJ Letters* 875 (2019) — ring diameter 42 ± 3 µas; shadow diameter ≈ 2√27 GM/c² ≈ 5.2 r_s. https://eventhorizontelescope.org/press-release-april-10-2019-astronomers-capture-first-image-black-hole
- Event Horizon Telescope Collaboration, "First Sagittarius A* Event Horizon Telescope Results. I", *ApJ Letters* 930, L12 (2022) — ring diameter 51.8 ± 2.3 µas. https://eventhorizontelescope.org/publications/first-sagittarius-event-horizon-telescope-results-i-shadow-supermassive-black-hole
- LIGO Scientific Collaboration & Virgo Collaboration, "Observation of Gravitational Waves from a Binary Black Hole Merger", *Phys. Rev. Lett.* 116, 061102 (2016) — GW150914, detected 14 September 2015.
- P. Schneider, J. Ehlers, E. E. Falco, *Gravitational Lenses*, Springer (1992) — point-mass lens equation β = θ − θ_E²/θ used in `lensing.py`.

## Quantum mechanics
- E. Schrödinger, "Quantisierung als Eigenwertproblem", *Annalen der Physik* 79, 361 (1926) — hydrogen eigenfunctions sampled in `orbital.py` (standard closed forms, e.g. Griffiths, *Introduction to Quantum Mechanics*, 3rd ed., 2018, Table 4.7).
- W. Heisenberg, "Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik", *Z. Phys.* 43, 172 (1927); E. H. Kennard (1927) for Δx·Δp ≥ ħ/2.
- R. P. Feynman, R. B. Leighton, M. Sands, *The Feynman Lectures on Physics*, Vol. III, ch. 1 "Quantum Behavior" — two-slit interference with single particles.
- X. Fan, T. G. Myers, B. A. D. Sukra, G. Gabrielse, "Measurement of the Electron Magnetic Moment", *Phys. Rev. Lett.* 130, 071801 (2023) — g/2 = 1.001 159 652 180 59 (13); agreement with QED at the ~10⁻¹² level given an independent α. https://doi.org/10.1103/PhysRevLett.130.071801

## Entanglement and non-signalling
- J. S. Bell, "On the Einstein Podolsky Rosen paradox", *Physics* 1, 195 (1964).
- A. Aspect, J. Dalibard, G. Roger, "Experimental Test of Bell's Inequalities Using Time-Varying Analyzers", *Phys. Rev. Lett.* 49, 1804 (1982).
- B. Hensen et al., "Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres", *Nature* 526, 682 (2015); also Giustina et al. and Shalm et al., *PRL* 115 (2015).
- The Nobel Prize in Physics 2022 — popular science background (Aspect, Clauser, Zeilinger). https://www.nobelprize.org/prizes/physics/2022/popular-information/
- G. C. Ghirardi, A. Rimini, T. Weber, "A general argument against superluminal transmission through the quantum mechanical measurement process", *Lett. Nuovo Cimento* 27, 293 (1980) — the no-communication theorem; also P. Eberhard & R. Ross (1989).
- Stanford Encyclopedia of Philosophy, "Bell's Theorem" and "Quantum Entanglement and Information" — for the precise wording of what entanglement does and does not allow.

## Quantum gravity: status of the field
- M. H. Goroff & A. Sagnotti, "The ultraviolet behavior of Einstein gravity", *Nucl. Phys. B* 266, 709 (1986) — two-loop non-renormalisability of perturbative quantum gravity.
- C. P. Burgess, "Quantum Gravity in Everyday Life: General Relativity as an Effective Field Theory", *Living Rev. Relativ.* 7, 5 (2004) — why the two theories coexist at ordinary energies.
- S. Weinstein & D. Rickles, "Quantum Gravity", *Stanford Encyclopedia of Philosophy* (2024) — overview of string theory, loop quantum gravity and emergence as research programmes without confirmed predictions.
- arXiv:2501.07614, "Does Quantum Gravity Happen at the Planck Scale?" (2025) — a cautionary survey used to keep the film's claims about the Planck scale modest.
- M. Van Raamsdonk, "Building up spacetime with quantum entanglement", *Gen. Relativ. Gravit.* 42, 2323 (2010) — emergence of geometry from entanglement (presented as speculation).

## Astronomical scale values
- Light-travel times: Moon 1.28 s, Sun 499 s (8.3 min), Neptune ≈ 4.1 h, Voyager 1 ≈ 23 h (NASA/JPL Voyager mission status, 2025); Proxima Centauri 4.24 ly; Milky Way disc ≈ 100 000 ly; GN-z11 light-travel ≈ 13.4 Gyr; CMB 13.8 Gyr (Planck 2018 cosmological parameters, *A&A* 641, A6, 2020).
- Earth circumference 40 075 km (WGS 84); c = 299 792 458 m/s (SI definition).
