# Fiducial Yukawa-vs-NFW fits

Gate: `P1-FIDUCIAL-01`.

## Scientific question

Across all 175 SPARC galaxies, what is the free-μ Yukawa fit quality, the finite-`r_c` fraction, and the same-config `dAIC` against NFW?

## Reproduction

```text
cd scripts && python fiducial_rerun.py
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
