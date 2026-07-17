# Decision Log

This is an append-only record. Do not remove or silently rewrite earlier decisions; add a superseding entry instead.

## 2026-07-14 — Separate the five papers into five repositories

### Decision

Maintain each of the five papers in a separate, paper-specific repository. This repository is exclusively for Paper 1, *Dark Matter Structure and Galaxy Phenomenology*.

### Reason

Separate repositories provide explicit scientific scope, provenance, gate history, result ownership, and paper-edit discipline for each paper.

### Evidence

Principal Investigator repository mapping supplied during infrastructure initialization.

### Consequences

Content from Papers 2–5 must not be imported into this repository. Cross-paper dependencies must be referenced explicitly rather than merged.

### Supersedes

None.

### Related gate

None; infrastructure decision.

### Related branch and files

Branch: `main`. Files: repository governance and workflow files created during infrastructure initialization.

## 2026-07-16 — Import the Paper 1 scientific record and register it against v16.3

### Decision

Import the `zetacheng/yukawa-sparc-fits` scientific record (SPARC data, analysis
scripts, raw result CSVs) into this governance repository byte-for-byte, and
register it against the PI-supplied paper **v16.3**. The imported scripts were
reorganized into importable functions with a `__main__` guard purely to enable
regression tests; numerical logic is byte-identical and reproduction of every
CSV was verified. Claims are entered `SUPPORTED` (reviewer-reproduced), not
`VERIFIED` — no in-repo reviewer record exists.

### Reason

The PI directed (2026-07-16) that the governance layer be built in this
`N-topic` repository with the science imported, and that the ledger be
reconciled to the supplied v16.3 paper rather than the v12-era snapshot in the
original task brief. See the two decisions recorded in the session hand-off.

### Evidence

Source commit `fd3b2b615194ed076df3d45cbe97fd0f2e4f2452`; per-gate `PROVENANCE.md`
and checksums; `MIGRATION.md`.

### Consequences

`P1-CL-010` is `RETIRED` (v16.3 recast the a0 relation as an observed-number
coincidence), not `PROPOSED`. Provenance gaps are recorded, not papered over
(see next entry).

### Supersedes

Extends the 2026-07-14 infrastructure decision; supersedes nothing.

### Related gate

All `P1-*` gates.

### Related branch and files

Branch `claude/paper1-gated-repo-governance-z478hp`; `data/`, `scripts/`,
`results/`, `CLAIMS.md`, `GATES.md`, `CONVENTIONS.md`, `MIGRATION.md`.

## 2026-07-16 — Two audit defects registered, not silently fixed

### Decision

Two defects found in reviewer audit on 2026-07-16 are **registered** in
`GATES.md` rather than silently fixed:

- **`P1-A0ERR-01`** — the `a0` statistical error bar was not properly derived
  (single-grid-step −0.01 side; `f_int` possibly not re-profiled at each `a0`;
  statistical-only interval while the error-model systematic is ~20× larger).
- **`P1-RCSLOPE-01`** — the `r_c`–`V_max` slope is sample-dependent
  (0.51 / 0.82 / 1.39); the "arithmetic consequence" a_c-slope argument mixed
  samples.

Both are recorded `RETIRED` (resolved/superseded), because the paper's own
v13–v15 work already addressed them: `P1-A0ERR-01` by withdrawing the slice
(v13) and re-deriving the profiled `a0 = 0.95 ± 0.03 (stat)` (v15,
`a0_profile_likelihood.py`); `P1-RCSLOPE-01` by restating the slope as sample
instability (v13). Neither was re-fixed in this sweep.

### Reason

The claim ledger exists precisely to record such defects and their disposition.
Reconciling to v16.3 means recording them as resolved-in-paper, with the honest
caveat that `P1-A0ERR-01`'s resolving artifact is not yet imported here.

### Evidence

Paper v16.3 changelog (v13, v15) and abstract; `GATES.md` `P1-A0ERR-01`,
`P1-RCSLOPE-01`.

### Consequences

They block nothing except the claims that rest on them: `P1-A0ERR-01` governs
`P1-CL-008`'s error bar; no current claim rests on the `r_c` slope. Importing
`a0_profile_likelihood.py` to make `P1-A0ERR-01`'s resolution reproducible
in-repo is an open follow-up (`HANDOFF.md`).

### Supersedes

None.

### Related gate

`P1-A0ERR-01`, `P1-RCSLOPE-01`.

### Related branch and files

Branch `claude/paper1-gated-repo-governance-z478hp`; `GATES.md`,
`results/intrinsic-scatter/`.

## Entry template

## YYYY-MM-DD — Decision title

### Decision

### Reason

### Evidence

### Consequences

### Supersedes

### Related gate

### Related branch and files
