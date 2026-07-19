# Tests

Repository-structure checks plus regression anchors that **import and run the
real analysis functions** (not re-typed constants). Passing tests are necessary
evidence but do not by themselves certify a scientific result.

## Layout

| File | Suite | Covers |
|---|---|---|
| `test_repository_structure.py` | fast | required files/dirs; per-gate provenance; **CLAIMS `Gate` column ↔ GATES `## <ID>` heading cross-check**; environment.txt is not a placeholder |
| `test_kernels.py` | fast | Yukawa/NFW/RAR kernel forms and limits; unit convention; `a0_MOND` reference; same-config vs per-model `dAIC` invariant |
| `test_regression_fiducial.py` | fast + `slow` | `P1-FIDUCIAL-01`: 5-galaxy re-fit (fast) and full 175-galaxy headline numbers (slow) |
| `test_regression_ac_test.py` | fast | `P1-AC-01`: fiducial and extended `a_c` tests |
| `test_regression_ml_prior.py` | `slow` | `P1-MLPRIOR-01`: lognormal-prior and μ=1 collapses |
| `test_regression_refit.py` | `slow` | `P1-REFIT-01`: single-`a0` RAR refit |
| `test_regression_nuisance.py` | `slow` | `P1-NUISANCE-01`: three-model error-floor comparison |

## Running

```bash
make test        # default: fast suite only (-m "not slow")
make test-slow   # the full-sample 175-galaxy anchors (-m slow)
make test-all    # everything
```

## Tolerances and mutation detection

- Anchors use **stated numerical tolerances**, never byte-identity:
  cross-platform floating-point reduction order makes byte-identity
  unachievable (learned in the Paper 3 repo).
- Every numeric anchor carries a **committed mutation-discrimination companion**
  (`tests/_util.py`): a value perturbed by more than the tolerance must be
  rejected, proving the tolerance discriminates rather than passing anything.
- A separate **temporary** mutation demonstration (perturbing a production
  quantity to confirm the anchors fail, then restoring) was run at import time
  and reported in the migration record; it is intentionally **not committed**.

`P1-ISCATTER-01` has no regression anchor: its producing script
(`intrinsic_scatter_comparison.py`) was not in the imported record. That gap is
tracked, not hidden (see `MIGRATION.md`).
