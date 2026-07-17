# Single-a0 RAR-kernel refit

Gate: `P1-REFIT-01`.

## Scientific question

Under an acceleration-dependent (RAR) kernel with one global `a0`, a lognormal μ prior, and a fixed configuration, what single `a0` and fit quality result?

## Reproduction

```text
cd scripts && python rar_refit.py
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
