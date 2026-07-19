# Characteristic-acceleration (a_c) tests

Gate: `P1-AC-01`.

## Scientific question

Does the characteristic acceleration `a_c = V(r_c)^2/r_c` cluster at a single MOND-like scale, or track `V_max`? Tested on the fiducial (point-source) and extended-source finite-`r_c` in-coverage subsamples.

## Reproduction

```text
cd scripts && python fiducial_rerun.py && python fiducial_ac_test.py && python cluster_test.py
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
