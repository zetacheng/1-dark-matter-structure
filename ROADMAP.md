# Roadmap

## Priority 0 — Governance import (DONE 2026-07-16)

Scientific record imported from `yukawa-sparc-fits`; claim ledger, gate
registry, conventions, provenance, and regression suite populated against v16.3.

## Priority 1 — Close the provenance gaps

- Import `intrinsic_scatter_comparison.py` + `heldout_validation.py` →
  reproduce `P1-CL-007` and the intrinsic-scatter part of `P1-CL-008`
  (`P1-ISCATTER-01`).
- Import `a0_profile_likelihood.py` → reproduce the v15 profiled
  `a0 = 0.95 ± 0.03 (stat)` in-repo (`P1-A0ERR-01`).
- File an independent reviewer record (`reviews/claude/`) so `SUPPORTED` claims
  can be considered for `VERIFIED`.

## Priority 2 — v13 fix list (PI-supplied; already implemented in v16.3)

Recorded here for provenance. These were the v13 corrective items; the supplied
v16.3 already carries all three, so **no paper edit is outstanding**:

1. **Delete the θ-medium language** — falsified by the companion equation-of-state
   calculation (`zetacheng/4-dark-energy-cosmology`). *(Done: v16 DE narrative
   synced; monopole DE-generator candidacy terminated by direct measurement.)*
2. **Restate the `r_c` power law as sample dependence** — `P1-RCSLOPE-01`.
   *(Done in v13: slope reported sample-unstable 0.51/0.82/1.39; cherry-picked
   0.82 → 1.18 line removed.)*
3. **Re-derive the `a0` error bar** — `P1-A0ERR-01`. *(Done in v13 withdrawal +
   v15 profiled re-derivation → `a0 = 0.95 ± 0.03 (stat)`, systematics to 1.28.)*

Any *new* paper edit requires reviewer acceptance and PI authorization
(`AGENTS.md`).

## Priority 3 — Future extensions

Deferred to the PI's programme (e.g. the topological-DM route flagged in the
v16 future-directions section). Not scoped by this import.
