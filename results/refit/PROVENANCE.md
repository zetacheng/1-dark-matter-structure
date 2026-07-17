# Single-a0 refit gate — Provenance

Gate: `P1-REFIT-01`. Source repository: `zetacheng/yukawa-sparc-fits`,
commit `fd3b2b615194ed076df3d45cbe97fd0f2e4f2452`, branch
`claude/repo-setup-rerun-q0wws6`.

| Original path (source repo) | Destination path | Transfer | Transformation |
|---|---|---|---|
| `results/rar_refit.csv` | `results/refit/raw/rar_refit.csv` | Copied byte-for-byte (sha256 `cdbbcbe8…`) | None |

## Producing script and exact bare invocation

```text
cd scripts
python rar_refit.py
```

Model: `g_pred = g_bar / (1 - exp(-sqrt(g_bar/a0)))` (McGaugh et al. 2016 RAR
form). One global fitted `a0` scanned on `logspace(0.3e-10, 4e-10, 49)`;
per-galaxy `mu` with a lognormal 0.1-dex prior (MAP on grid); fixed
configuration `rmin = 0`, `sigma_f = 6 km/s`; V-space Gaussian −2 ln L;
unit factor `1e6/3.0857e19`.

## Input data files

- `data/MassModels_Lelli2016c.mrt`.

## Headline numbers (reproduced 2026-07-16, exact)

- best `a0` = **8.83e-11 m/s²** (grid-adjacent Δ(−2 ln L)=1: `[8.36e-11, 9.32e-11]`);
  median `χ²/pt` = 1.35; `mu` median 0.66.

## Scope note — this is NOT the paper headline a0

`rar_refit.py` is the fixed-configuration, lognormal-prior single-`a0` fit
(`a0 = 8.83e-11`). The paper's reported single-`a0` values come from the
nuisance-marginalized comparison (`P1-NUISANCE-01`: `1.046e-10` at floor 6,
`1.279e-10` at floor 3) and, for the headline `0.95±0.03 (stat)` interval,
from the later profiled fit `a0_profile_likelihood.py`, which is **not present**
in the imported record (see `GATES.md` `P1-A0ERR-01` and `MIGRATION.md`).
