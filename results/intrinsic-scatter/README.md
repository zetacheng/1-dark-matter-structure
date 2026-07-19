# Intrinsic-scatter three-model comparison

Gate: `P1-ISCATTER-01`.

## Scientific question

Under a global intrinsic-scatter likelihood (no error floor), with each model
carrying a fitted intrinsic-scatter fraction `f_int`, how do RAR single-`a0`,
Yukawa, and NFW compare — in sample and on held-out galaxies?

## Status — provenance gap (no artifact imported)

The producing script `intrinsic_scatter_comparison.py` (and the held-out
`heldout_validation.py`) named in the paper changelog are **absent** from the
imported `yukawa-sparc-fits` record. `raw/` is intentionally empty. The paper's
headline numbers for this gate — in-sample `dAIC` RAR 0 / Yukawa +4859 / NFW
−1614, fitted `f_int` 0.050 / 0.156 / 0.034, held-out `Δ(−2 ln L) = −4207`,
single-`a0` = 9.58e-11 — back claims `P1-CL-007` and part of `P1-CL-008`, which
are recorded `SUPPORTED` (reviewer-reproduced) but are **not reproducible in
this repository**. See `PROVENANCE.md`. The present, related error-floor
comparison is `P1-NUISANCE-01`.

## Required follow-up

Import the intrinsic-scatter and held-out scripts and their raw outputs, then
add a regression anchor. Tracked in `HANDOFF.md` and `MIGRATION.md`.
