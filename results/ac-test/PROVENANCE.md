# a_c-test gate — Provenance

Gate: `P1-AC-01`. Source repository: `zetacheng/yukawa-sparc-fits`,
commit `fd3b2b615194ed076df3d45cbe97fd0f2e4f2452`, branch
`claude/repo-setup-rerun-q0wws6`.

| Original path (source repo) | Destination path | Transfer | Transformation |
|---|---|---|---|
| `results/fiducial_ac_test.csv` | `results/ac-test/raw/fiducial_ac_test.csv` | Copied byte-for-byte (sha256 `7131d208…`) | None |
| `results/clustering_test_results.csv` | `results/ac-test/raw/clustering_test_results.csv` | Copied byte-for-byte (sha256 `55bae9cb…`) | None |
| `figures/fig4_ac_test.{png,pdf}` | `results/ac-test/figures/` | Copied byte-for-byte | None (regenerable) |
| `figures/clustering_test_fig.{png,pdf}` | `results/ac-test/figures/` | Copied byte-for-byte | None (regenerable) |

## Producing scripts and exact bare invocations

```text
cd scripts
python fiducial_rerun.py      # produces the fiducial fit table consumed below
python fiducial_ac_test.py    # -> fiducial_ac_test.csv + figures/fig4_ac_test.*
python cluster_test.py        # -> clustering_test_results.csv (extended source)
python plot_ac_test.py        # redraws figures/clustering_test_fig.*
```

Pre-registered cut (both tests): only galaxies with a finite best-fit `r_c`
that lies **inside the data coverage** (`r_c ≤` last measured radius); no
extrapolation. Unit conversion `KMS2_PER_KPC_TO_SI = 1e6/3.0857e19`;
`A0_MOND = 1.2e-10 m/s²` is a reference value, not fitted.

## Input data files

- `data/MassModels_Lelli2016c.mrt` (both tests).
- `data/summary_v2.csv` (extended-source fit summary; input to `cluster_test.py`).
- `results/fiducial/raw/fiducial_rerun.csv` (fiducial fit table; input to
  `fiducial_ac_test.py`).

## Headline numbers (reproduced 2026-07-16, exact)

- Fiducial (point-source) `a_c` test: **33** in-coverage galaxies (of 101
  finite-`r_c`; 68 excluded as `r_c` beyond last point); slope of
  `log a_c` vs `log V_max` = **1.09 ± 0.17**; scatter **0.34 dex**; median
  `a_c` = **0.22 a0**; Spearman `ρ = 0.72`.
- Extended-source `a_c` test: **100** in-coverage galaxies (of 156
  finite-`r_c`); `a_c` scatter **0.44 dex**; slope **1.33 ± 0.10**;
  Spearman `ρ = 0.80`.
