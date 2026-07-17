# Results

Raw outputs are immutable and must never be edited manually. Processed results must record complete provenance, including the generating script and raw input used.

Every result directory must include:

- `README.md`;
- configuration;
- raw output;
- a processed table;
- a verdict;
- the commit hash;
- the branch;
- the date;
- environment information.

Recommended layout:

```text
results/<gate-id>/
  README.md
  config.json
  raw/
  processed/
  figures/
  verdict.md
  environment.txt
```

See `docs/RESULT_SCHEMA.md` for the required provenance standard.

## Gate directories

Each gate holds `raw/` (immutable imported CSVs), `processed/`, `PROVENANCE.md`,
`environment.txt`, and `README.md`.

| Directory | Gate | Raw artifact(s) |
|---|---|---|
| `fiducial/` | `P1-FIDUCIAL-01` | `fiducial_rerun.csv` |
| `ac-test/` | `P1-AC-01` | `fiducial_ac_test.csv`, `clustering_test_results.csv` (+ `figures/`) |
| `ml-prior/` | `P1-MLPRIOR-01` | `ml_prior_lognormal.csv`, `mufixed_rerun.csv` |
| `refit/` | `P1-REFIT-01` | `rar_refit.csv` |
| `nuisance/` | `P1-NUISANCE-01` | `nuisance_comparison.csv` (error-floor-3 run) |
| `intrinsic-scatter/` | `P1-ISCATTER-01` | none — producing script not imported (provenance gap) |

The imported CSVs are byte-for-byte copies from `zetacheng/yukawa-sparc-fits`
(commit `fd3b2b6…`); see each gate's `PROVENANCE.md`. The top-level `raw/`,
`processed/`, and `figures/` placeholders are retained for schema compatibility.
