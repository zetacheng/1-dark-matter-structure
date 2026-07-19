# Comparison — reconstruction vs paper v16.4 (`P1-ISCATTER-REPRO-01`)

Opened **after** the blind reconstruction was computed and committed
(`9fcfd5a`). Paper values from `paper/yukawa_sparc_paper_v164.tex`
Table~\ref{tab:refit} and Section~\ref{sec:refit}; `a0` intrinsic-scatter value
from claim `P1-CL-008`. Tolerances are the pre-registered bands
(`derivations/p1-iscatter-repro/PREREGISTRATION.md` §8), fixed before computing.

| Quantity | Paper v16.4 | Reconstruction | |diff| | Pre-registered tolerance | Within? |
|---|---|---|---|---|---|
| `dAIC` RAR (reference) | 0 | 0 | 0 | — | — |
| `dAIC` Yukawa vs RAR | **+4859** | **+4857** | 2 | max(±200, ±8%) = ±389; sign+order | **YES** |
| `dAIC` NFW vs RAR | **−1614** | **−1621** | 7 | max(±200, ±8%) = ±200; sign+order | **YES** |
| `f_int` RAR | 0.050 | 0.0515 | 0.0015 | max(±0.02, ±20%) = ±0.02 | **YES** |
| `f_int` Yukawa | 0.156 | 0.1577 | 0.0017 | max(±0.02, ±20%) = ±0.031 | **YES** |
| `f_int` NFW | 0.034 | 0.0330 | 0.0010 | max(±0.02, ±20%) = ±0.02 | **YES** |
| `a0` (m/s²) | 9.58e-11 | 9.777e-11 | +2.1% | one grid step ≈ ±7% | **YES** |
| median χ²/pt RAR | 0.83 | 0.840 | 0.010 | ±0.10 | **YES** |
| median χ²/pt Yukawa | 0.75 | 0.740 | 0.010 | ±0.10 | **YES** |
| median χ²/pt NFW | 0.65 | 0.647 | 0.003 | ±0.10 | **YES** |

## Outcome: REPRODUCED

Every pre-registered quantity is within its pre-registered tolerance, with
matching sign and order of magnitude. The paper's headline three-model
intrinsic-scatter comparison — RAR single-`a0` decisively beating the
2×175-parameter Yukawa kernel (`dAIC ≈ +4.9k`) while NFW keeps a moderate edge
(`dAIC ≈ −1.6k`) — is reconstructed independently of the lost original script.

Per the pre-registered outcome rule (§9): `P1-ISCATTER-REPRO-01` passes;
`P1-CL-007` is now backed in-repo by this reconstruction (kept `SUPPORTED`, since
this reconstruction is not itself an independent reviewer re-run — the reviewer
may raise it to `VERIFIED`). The lost-artifact gate `results/intrinsic-scatter/`
stays external-evidence-only, pointing here.

## Honest caveat on the strength of "independent"

The agreement is very tight (`dAIC` within 2 and 7 units on values of thousands;
`f_int` within 0.002). This is expected and does **not** indicate leakage — no
paper value appears anywhere in the reconstruction code. It is tight because, as
instructed, the reconstruction **reuses `nuisance_comparison.py`** (the same
author's codebase: same SPARC parser, same μ/d/i nuisance grids and priors, same
kernel implementations, same RAR `nu`), changing only the likelihood's noise
model. The independence is therefore at the level of the **intrinsic-scatter
likelihood substitution and the fitting driver**, not a clean-room
reimplementation of the whole pipeline. A shared bug in the reused machinery
would be reproduced, not caught. This reconstruction confirms that the paper's
`dAIC`/`f_int`/`a0` follow from the stated method applied to that shared
machinery; it does not independently re-derive the SPARC handling or nuisance
treatment. That is exactly the scope the task specified ("reuse the verified
machinery; change the noise model"), recorded here so the reviewer weights the
result correctly.

## Reproduce

```text
python -m scripts.intrinsic_scatter_repro    # ~7 min, writes results/intrinsic-scatter-repro/
```
Regression anchor (`tests/test_regression_iscatter_repro.py`) exercises the real
`rar_gal_is`/`kern_gal_is` on a few galaxies against the committed
`raw/iscatter_repro.csv` with stated tolerances.
