# Fiducial gate — Provenance

Gate: `P1-FIDUCIAL-01`. Source repository: `zetacheng/yukawa-sparc-fits`,
commit `fd3b2b615194ed076df3d45cbe97fd0f2e4f2452`, branch
`claude/repo-setup-rerun-q0wws6`.

| Original path (source repo) | Destination path | Transfer | Transformation |
|---|---|---|---|
| `results/fiducial_rerun.csv` | `results/fiducial/raw/fiducial_rerun.csv` | Copied byte-for-byte (sha256 `d7dcad45…`) | None |

## Producing script

`scripts/fiducial_rerun.py`

## Exact bare invocation

```text
cd scripts
python fiducial_rerun.py
```

Fixed configuration (in-script constants, not CLI): mass grid
`M_MIN,M_MAX,M_STEPS = 0.00125, 0.5, 140`; NFW scale grid
`0.5, 200.0, 80`; inner-radius cuts `RMIN_LIST = [0.0, 2.0, 3.0]`; error
floors `EF_LIST = [6.0, 4.0, 3.0]`; per-galaxy AIC selection; Yukawa-selected
`(rmin, ef)` used for the same-config dAIC.

## Input data files

- `data/MassModels_Lelli2016c.mrt` (SPARC mass models, 175 galaxies).

## Headline numbers (reproduced 2026-07-16, exact)

- 175 galaxies fitted; 101 finite `r_c` (58%); 74 at the boundary.
- median finite `r_c` = 15.8 kpc; median `χ²/pt` = 1.08.
- median `dAIC` (same-config, paper definition) = **+6.6**;
  `|dAIC| ≤ 2` (comparable): 48 (27%); `dAIC > 2` (NFW preferred): 117 (67%).
- diagnostic `dAIC_permodel` median = **+9.5**.

The `raw/` CSV is immutable. Regenerate with the invocation above; the
regression suite (`tests/test_regression_fiducial.py`) exercises the same code
on the real data with stated tolerances.
