# Intrinsic-scatter reconstruction — Provenance

Gate: `P1-ISCATTER-REPRO-01`.

## This is a reconstruction, not the original

The original producing script (`intrinsic_scatter_comparison.py`) that generated
the paper's Table~\ref{tab:refit} intrinsic-scatter numbers is **genuinely lost**
— it is not in the imported `yukawa-sparc-fits` record. This gate holds a **2026
independent reconstruction** built from the paper's method description, under the
discipline of a pre-registration written before computing. It does **not** claim
to be, and must not be presented as, the original run. The external-evidence-only
gate `results/intrinsic-scatter/` is unchanged; it retains the lost-artifact
status and now points here for the backing reconstruction.

## Producing script and exact bare invocation

```text
python -m scripts.intrinsic_scatter_repro
```

`scripts/intrinsic_scatter_repro.py` reuses `scripts/nuisance_comparison.py`
(unmodified) for SPARC loading, the μ/d/i nuisance grids and priors, the kernels,
the RAR `nu`, and the kernel-scale grids. The **only** change is the noise model:
the error floor is replaced by a single global fitted fractional intrinsic
scatter per model, `σ_tot,i² = (e_V,i s)² + (f_int V_obs,i s)²`, `s = sin i0/sin i`.

Fixed configuration: see `derivations/p1-iscatter-repro/PREREGISTRATION.md`
(a0 grid `logspace(0.5e-10, 2.5e-10, 25)`; μ 41-pt / d,i 9-pt nuisance grids;
`f_int` bounded-Brent on `[1e-3, 0.5]`, `xatol=1e-4`; AIC/k counting).

## Input data files

- `data/MassModels_Lelli2016c.mrt` (SPARC rotation curves).
- `data/SPARC_Lelli2016c.mrt` (Table 1: distance/inclination priors, quality flag).

## Outputs (this gate only)

| Path | Content |
|---|---|
| `raw/iscatter_repro.csv` | Per-galaxy `-2 ln L`, `χ²/pt`, `B>0` flags for all three models (the reconstruction's own primary record; legitimately byte-preserved because it was produced now — a 2026 reconstruction). |
| `regen/summary.csv`, `regen/summary.txt` | Per-model `-2 ln L`, `k`, `AIC`, `dAIC` vs RAR, fitted `f_int`, fitted `a0`, median `χ²/pt`. |

## Comparison to the paper

The blind reconstruction values were computed first and only afterward compared
to the paper — see `COMPARISON.md` and `GATES.md` `P1-ISCATTER-REPRO-01` for the
outcome and its effect on `P1-CL-007`.
