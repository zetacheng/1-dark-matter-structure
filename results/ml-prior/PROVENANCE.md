# M/L-prior gate — Provenance

Gate: `P1-MLPRIOR-01`. Source repository: `zetacheng/yukawa-sparc-fits`,
commit `fd3b2b615194ed076df3d45cbe97fd0f2e4f2452`, branch
`claude/repo-setup-rerun-q0wws6`.

| Original path (source repo) | Destination path | Transfer | Transformation |
|---|---|---|---|
| `results/ml_prior_lognormal.csv` | `results/ml-prior/raw/ml_prior_lognormal.csv` | Copied byte-for-byte (sha256 `f9bb87a5…`) | None |
| `results/mufixed_rerun.csv` | `results/ml-prior/raw/mufixed_rerun.csv` | Copied byte-for-byte (sha256 `82fd359a…`) | None |

## Producing scripts and exact bare invocations

```text
cd scripts
python ml_prior_lognormal.py   # lognormal 0.1-dex prior on log10(mu), MAP
python ml_prior_mufixed.py     # mu fixed at unity (fiducial Upsilon*)
```

Prior: Gaussian on `log10(mu)` centred at 0 (`mu = 1`), scatter `S_DEX = 0.1`
(Li et al. 2020), same prior for both kernels; `mu` grid
`np.linspace(-0.6, 0.6, 61)` (0.02 dex). Same 9-config `(rmin, ef)` AIC
selection and same-config dAIC vs NFW as the fiducial pipeline.

## Input data files

- `data/MassModels_Lelli2016c.mrt`.

## Headline numbers (reproduced 2026-07-16, exact)

- Lognormal 0.1-dex prior: finite/boundary **12/163 (7%/93%)**; median finite
  `r_c` = **6.4 kpc**; median `χ²/pt` = **1.14**; median same-config `dAIC`
  = **+7.7**.
- `mu` fixed at unity: finite/boundary **4/171 (2%/98%)**; median `χ²/pt`
  = **1.48**; median `dAIC` = **+6.6**; Yukawa-preferred count **0**.

These two runs are the evidence for the FAILED robustness claim `P1-CL-009`:
under a physical stellar normalization the finite-`r_c` population collapses
from the free-μ 58% to 7% (lognormal) / 2% (μ = 1).
