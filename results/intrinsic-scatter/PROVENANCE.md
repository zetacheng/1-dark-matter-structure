# Intrinsic-scatter comparison gate — Provenance

Gate: `P1-ISCATTER-01`. Status: **artifact NOT imported — provenance gap.**

## What this gate covers

The paper's headline three-model comparison uses a **global intrinsic-scatter
likelihood** (no error floor): each model carries a fitted intrinsic-scatter
fraction `f_int`, and the models are compared by total AIC. The paper (v16.3,
Sec. "A single-acceleration-scale refit") and its abstract report:

- in-sample `dAIC`: RAR single-`a0` **0** / Yukawa **+4859** / NFW **−1614**;
- fitted `f_int`: **0.050 / 0.156 / 0.034** (RAR / Yukawa / NFW);
- single-`a0` under the intrinsic-scatter likelihood: `a0 = 9.58e-11 m/s²`;
- held-out 5-fold: RAR beats refitted Yukawa out of sample by
  `Δ(−2 ln L) = −4207`.

These are claims `P1-CL-007` and part of `P1-CL-008`.

## The gap

The producing script named in the paper changelog —
`intrinsic_scatter_comparison.py` — is **not present** in the imported
`yukawa-sparc-fits` record (commit `fd3b2b6…`, which contains only
`nuisance_comparison.py`, the error-floor variant). The held-out validation
(`heldout_validation.py`) is likewise absent. No raw CSV for this gate exists
in the source repository, so `raw/` here is intentionally empty.

Consequently these numbers are recorded as `SUPPORTED` (the independent
reviewer reproduced them on a clean environment, per the PI hand-off) but are
**not independently reproducible inside this repository**. The error-floor
comparison (`P1-NUISANCE-01`) is present and gives different numbers
(Yukawa `+9660` at floor 6), confirming the intrinsic-scatter and error-floor
likelihoods are distinct and must not be conflated.

## Required follow-up (tracked)

Import `intrinsic_scatter_comparison.py` (and `heldout_validation.py`,
`a0_profile_likelihood.py`, `rc_floor.py`) from the later `yukawa-sparc-fits`
state that produced paper v13–v16, add the raw outputs here, and add a
regression anchor. Tracked in `HANDOFF.md` and `MIGRATION.md`.
