# Stellar M/L-prior robustness

Gate: `P1-MLPRIOR-01`.

## Scientific question

Is the free-μ finite-`r_c` population robust to a physical stellar mass-to-light normalization (lognormal 0.1-dex prior, and μ fixed at unity)?

## Reproduction

```text
cd scripts && python ml_prior_lognormal.py && python ml_prior_mufixed.py
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
