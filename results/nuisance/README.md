# Three-model nuisance comparison (error floor)

Gate: `P1-NUISANCE-01`.

## Scientific question

With per-galaxy μ/distance/inclination nuisances marginalized, how do RAR single-`a0`, Yukawa, and NFW compare by total AIC at fixed error floors, and what single `a0` results?

## Reproduction

```text
cd scripts && python nuisance_comparison.py 6   # and: python nuisance_comparison.py 3
```

## Directory contract

- `raw/`: immutable CSV outputs imported byte-for-byte from
  `zetacheng/yukawa-sparc-fits` (see `PROVENANCE.md` for source paths,
  commit, and sha256).
- `processed/`: reserved for provenance-tracked derived tables.
- `PROVENANCE.md`: source-to-destination ledger, exact invocation, inputs,
  and headline numbers.
- `environment.txt`: import/reproduction environment (real, not a placeholder).

## Status

`SUPPORTED` — independently reproduced by the reviewer on a clean environment
and re-run at import (2026-07-16). **Not** `VERIFIED`: no independent reviewer
record exists in this repository yet. Gate verdict fields live in `GATES.md`;
a `verdict.md` will be added when a reviewer record is filed under
`reviews/claude/`.
