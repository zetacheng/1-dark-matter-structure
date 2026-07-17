# Nuisance-comparison gate — Provenance

Gate: `P1-NUISANCE-01`. Source repository: `zetacheng/yukawa-sparc-fits`,
commit `fd3b2b615194ed076df3d45cbe97fd0f2e4f2452`, branch
`claude/repo-setup-rerun-q0wws6`.

| Original path (source repo) | Destination path | Transfer | Transformation |
|---|---|---|---|
| `results/nuisance_comparison.csv` | `results/nuisance/raw/nuisance_comparison.csv` | Copied byte-for-byte (sha256 `bd89817b…`) | None |

## Producing script and exact bare invocations

```text
cd scripts
python nuisance_comparison.py 6    # error floor 6 km/s -> a0 = 1.046e-10
python nuisance_comparison.py 3    # error floor 3 km/s -> a0 = 1.279e-10
```

**The committed `raw/nuisance_comparison.csv` is the error-floor-3 run**
(verified: the refactored script at `EF=3` reproduces it byte-for-byte;
`EF=6` does not). The script overwrites a single output filename, so the raw
artifact records whichever floor was run last in the source repository (floor
3). Both floors are reproducible from the same script.

Three models (RAR single-`a0`, Yukawa, NFW) with per-galaxy nuisances
marginalized by MAP: `mu` (lognormal 0.1 dex), distance factor and inclination
with Gaussian priors from SPARC Table 1 (`e_D/D`, `e_Inc`); fixed `rmin = 0`;
error floor is the CLI argument.

## Input data files

- `data/MassModels_Lelli2016c.mrt`.
- `data/SPARC_Lelli2016c.mrt` (Table 1: distance/inclination priors, quality flag).

## Headline numbers (reproduced 2026-07-16, exact)

- Floor 6 (all 175): `a0` = **1.046e-10 m/s²**; total AIC RAR **26688** /
  Yukawa **36347** / NFW **24596**.
- Floor 3 (all 175): `a0` = **1.279e-10 m/s²**; total AIC RAR **29238** /
  Yukawa **49102** / NFW **24984**.

## Distinction from the intrinsic-scatter comparison (important)

This is the **error-floor** comparison. The paper's headline in-sample
`dAIC` values (RAR 0 / Yukawa **+4859** / NFW **−1614**) and the fitted
intrinsic-scatter fractions `f_int` (0.050 / 0.156 / 0.034) are from the
**intrinsic-scatter likelihood** variant (`intrinsic_scatter_comparison.py`),
which is **absent** from the imported record. See
`results/intrinsic-scatter/PROVENANCE.md` and `GATES.md` `P1-ISCATTER-01`.
