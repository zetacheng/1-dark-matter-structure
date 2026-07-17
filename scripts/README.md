# Scripts

Reviewed numerical and reproducibility scripts. Every script identifies its
inputs, outputs, fixed configuration, and applicable conventions
(see `CONVENTIONS.md`). Scripts must never modify raw outputs under `results/`.

These scripts were imported from `zetacheng/yukawa-sparc-fits`
(commit `fd3b2b6…`) on 2026-07-16. **Import adaptation:** each computational
script was reorganized into importable functions with an
`if __name__ == "__main__": main()` guard so the regression suite in `tests/`
can import and exercise the real code instead of re-typed constants. The
numerical logic is byte-identical to the source; reproduction of every
committed CSV was verified byte-for-byte on the import environment.

| Script | Gate | Produces | Notes |
|---|---|---|---|
| `_paths.py` | — | — | Path resolution; env overrides `SPARC_MRT`, `SUMMARY_CSV`, `SPARC_T1`, `RESULTS_DIR`, `FIGURES_DIR`. |
| `fiducial_rerun.py` | `P1-FIDUCIAL-01` | `fiducial_rerun.csv` | Free-μ Yukawa vs NFW; same-config `dAIC`. Exposes `load_sparc, wls_v1, run_gal, yuk, nfw, fit_all`. |
| `fiducial_ac_test.py` | `P1-AC-01` | `fiducial_ac_test.csv`, `fig4_ac_test.*` | Fiducial `a_c` test. Exposes `compute_ac_table`. |
| `cluster_test.py` | `P1-AC-01` | `clustering_test_results.csv` | Extended-source `a_c` test. Exposes `compute_ac_table`. |
| `plot_ac_test.py` | `P1-AC-01` | `clustering_test_fig.*` | Redraws the clustering figure. |
| `ml_prior_lognormal.py` | `P1-MLPRIOR-01` | `ml_prior_lognormal.csv` | Lognormal 0.1-dex μ prior. Exposes `run_gal_prior, fit_all`. |
| `ml_prior_mufixed.py` | `P1-MLPRIOR-01` | `mufixed_rerun.csv` | μ fixed at unity. Exposes `run_gal, fit_all`. |
| `rar_refit.py` | `P1-REFIT-01` | `rar_refit.csv` | Single-`a0` RAR-kernel refit. Exposes `nu, total_nll, fit_a0`. |
| `nuisance_comparison.py` | `P1-NUISANCE-01` | `nuisance_comparison.csv` | Three-model error-floor comparison. CLI arg = error floor (default 6). Exposes `rar_gal, kern_gal, run, model_aics`. |

Not imported (named in the paper but absent from the source record — see
`MIGRATION.md`): `intrinsic_scatter_comparison.py`, `heldout_validation.py`,
`a0_profile_likelihood.py`, `rc_floor.py`.

## Reproduce

```bash
pip install -e ".[dev]"      # numpy, scipy, pandas, matplotlib, pytest, ruff
cd scripts
python fiducial_rerun.py
python fiducial_ac_test.py
python cluster_test.py
python ml_prior_lognormal.py
python ml_prior_mufixed.py
python rar_refit.py
python nuisance_comparison.py 6
```
