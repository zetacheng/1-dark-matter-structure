# Pre-registration — intrinsic-scatter three-model reconstruction (`P1-ISCATTER-REPRO-01`)

**Written before any reconstruction code was run or any result inspected.**
Every choice below is fixed from paper `paper/yukawa_sparc_paper_v164.tex`
Section~\ref{sec:refit} ("Kernel, nuisances, and likelihood") and
`CONVENTIONS.md`. The producing script of the original result
(`intrinsic_scatter_comparison.py`) is genuinely lost; this is a **2026
independent reconstruction**, not the original run.

**Blinding.** The paper's numeric results (the Table~\ref{tab:refit} `dAIC`,
`f_int`, `a0`, and `χ²/pt` values) are **not** written into the script, the
tests, the docstrings, or any tolerance below, and agreement is **not**
inspected until Task 3. The tolerances here are derived from this method's own
grid/optimization precision, not chosen to admit any target value. If the
reconstruction disagrees, that is recorded as a result about the paper.

## 1. Model / kernel (fixed)

Radial-acceleration-relation (RAR) response, single global `a0` shared by all
175 galaxies:
```
g_pred = g_bar / (1 - exp(-sqrt(g_bar / a0)))
g_bar(r) = (V_gas^2 + mu (V_disk^2 + V_bul^2)) / r
```
Reuse `scripts/nuisance_comparison.py`: `nu()`, `yuk()`, `nfw()` and the RAR
`g_pred` construction are already implemented and verified there. The Yukawa
kernel `(1 - exp(-2 m r))/r` and NFW kernel `(ln(1+x) - x/(1+x))/r` are fitted
under the **same** nuisance structure, each with its own per-galaxy `(m,B)` /
`(r_s,B)` and its own global `f_int`.

## 2. Nuisances (fixed — reused verbatim from `nuisance_comparison.py`)

Per galaxy, MAP over three nuisance grids:
- **`mu`** (stellar rescaling): lognormal 0.1 dex about fiducial `Upsilon*`.
  Grid `MUG = 10**linspace(-0.4, 0.4, 41)` (0.02 dex); penalty `PMU = (log10 mu / 0.1)^2`.
- **`d = D/D0`** (distance): Gaussian width `sd = max(e_D/D0, 0.01)`.
  Grid `linspace(max(0.2, 1-3 sd), 1+3 sd, 9)`; penalty `((d-1)/sd)^2`.
  Scalings `r -> d r`, `V_bar^2 -> d V_bar^2`.
- **`i`** (inclination): Gaussian width `si = max(e_i, 0.5)`.
  Grid `clip(linspace(i0-3 si, i0+3 si, 9), 10, 90)`; penalty `((i-i0)/si)^2`.
  Rescaling `s = sin(i0)/sin(i)`, applied to the observed velocities
  (`V_obs -> V_obs s`, `e_V -> e_V s`).

Priors from SPARC Table 1 (`data/SPARC_Lelli2016c.mrt`): `e_D/D0`, `e_i`.

## 3. Likelihood — THE substitution (fixed)

Replace the error floor with a single **global fitted fractional intrinsic
scatter** per model. No error floor. With `s = sin(i0)/sin(i)`:
```
sigma_tot,i^2 = (e_V,i * s)^2 + (f_int * V_obs,i * s)^2
-2 lnL = sum_points [ (V_obs,i*s - V_pred,i)^2 / sigma_tot,i^2 + ln(2*pi*sigma_tot,i^2) ]
         + mu-prior + d-prior + i-prior       (per-galaxy MAP objective)
```
The Gaussian normalization term `ln(2*pi*sigma_tot^2)` is **retained** (it
penalizes inflating `f_int`). Noise is attached to the **observed** velocities.
`f_int` is **global** (shared across all 175 galaxies) and each of RAR / Yukawa
/ NFW carries its **own** `f_int`; per-galaxy kernel parameters are retained.

Note: `sigma_tot` depends on `V_obs` (not `V_pred`), so for fixed `f_int` the
Yukawa/NFW amplitude `B` is still the solution of a linear WLS at each kernel
scale — the reused `nuisance_comparison.py` inner machinery applies unchanged
except the `sigma` array is recomputed from `f_int` instead of the floor.

## 4. `f_int` optimization (fixed)

`f_int` is fitted by bounded 1-D minimization of the total `-2 lnL` (summed
over galaxies at their per-galaxy MAP):
`scipy.optimize.minimize_scalar(method="bounded", bounds=(1e-3, 0.5), options={"xatol": 1e-4})`.
- **RAR:** joint with `a0`. For each `a0` on the grid below, optimize `f_int`;
  select the `a0` (and its `f_int`) minimizing the total `-2 lnL`.
- **Yukawa, NFW:** optimize their own `f_int` (no `a0`).

Bounds `[0.001, 0.5]` chosen to bracket any plausible fractional velocity
scatter (0.1%–50%) **without** targeting a specific value. Deterministic (Brent).

## 5. `a0` grid (fixed — reused)

`a0_grid = logspace(0.5e-10, 2.5e-10, 25)` (as in `nuisance_comparison.py`).
Step factor `5^(1/24) ≈ 1.070` → ≈7.0% per step. Kernel scale grids reused:
`m_grid = logspace(0.00125, 0.5, 140)`, `rs_grid = logspace(0.5, 200, 80)`.

## 6. AIC / parameter counting (fixed, per `CONVENTIONS.md`)

`AIC = (-2 lnL) + 2k`, `k` = parameters free at the optimum. `dAIC` quoted
relative to the single-`a0` RAR model. With `n = 175`:
- Common per-galaxy nuisances `mu, d, i`: `3n`, present in all three models →
  **cancel** in every `dAIC`.
- **RAR:** `k_R = 3n + 1 (a0) + 1 (f_int_R)`.
- **Yukawa:** `k_Y = 3n + n (m) + #{B_Y>0} + 1 (f_int_Y)`.
- **NFW:** `k_N = 3n + n (r_s) + #{B_N>0} + 1 (f_int_N)`.
`B` counted where non-zero at the optimum (as in `nuisance_comparison.model_aics`).
The global `f_int` (+1 each) cancels between any alternative and RAR, so `dAIC`
depends only on `Δ(-2 lnL)` and the per-galaxy kernel-parameter counts; the
`a0` (+1) is RAR-specific. `median χ²/pt` per galaxy = `Σ((V_obs*s - V_pred)/σ_tot)^2 / N`
at the MAP.

## 7. Sample (fixed)

All **175** SPARC galaxies matched between `MassModels_Lelli2016c.mrt` and Table 1
(the paper's three-model Table is the all-175 set; `nuisance_comparison.py`
already matches 175).

## 8. Pre-registered pass/fail tolerances (fixed; justified by method precision)

Each band is an estimate of *this reconstruction's* numerical precision, written
without reference to the paper values.

| Quantity | Tolerance | Justification (method precision, not target-fitting) |
|---|---|---|
| `dAIC` (each of Y, N vs RAR) | within **max(±200 absolute, ±8% relative)**, **and sign + order of magnitude must match** | `a0` grid step ≈7% moves RAR's `-2 lnL` by the profile curvature × step; grid-MAP nuisances add a staircase (~±10 units total, per the paper's own methodological note); `k`-counting of `B` where `>0` vs a flat `2n` differs by O(tens). The absolute floor covers the small-|dAIC| model; the relative band covers the large one. |
| `f_int` (each ×3) | within **max(±0.02 absolute, ±20% relative)** | dominant uncertainty is the finite `mu`/`d`/`i` grid resolution shifting the joint optimum; the `minimize_scalar` `xatol=1e-4` is negligible by comparison. |
| `a0` | within **one grid step (≈±7%)** | `a0` resolved on the 25-point log grid; a finer/continuous profile could shift it by up to one step. |
| median `χ²/pt` (each ×3) | within **±0.10 absolute** | median over 175 galaxies is robust; grid-MAP nuisance quantization perturbs individual `χ²/pt` by small amounts. |

## 9. Outcome rule (pre-committed; acted on only in Task 3)

- **Reproduced** — all quantities within tolerance → `P1-ISCATTER-REPRO-01`
  passes; `P1-CL-007` moves from external-evidence-only to `SUPPORTED` backed by
  the reconstruction.
- **Close but outside band** — same sign/order, deviation outside tolerance →
  record both numbers; report the disagreement and any candidate convention
  explanation **separately**; `P1-CL-007` stays `SUPPORTED` with the deviation
  noted; do **not** silently adopt a reconciling convention.
- **Refuted** — wrong sign or order of magnitude → finding about the paper;
  `P1-CL-007` → `INCONCLUSIVE`/`FAILED` as the numbers dictate, both values on
  record, flagged for the PI. Reported plainly, not tuned away.

## 10. Provenance

Reconstruction artifacts go to `results/intrinsic-scatter-repro/` (new gate),
**not** `results/intrinsic-scatter/raw/` (which stays external-evidence-only —
the original artifact is lost). Reconstruction script:
`scripts/intrinsic_scatter_repro.py`, run bare as
`python -m scripts.intrinsic_scatter_repro`.
