# Current Handoff

## Current task

Gated-repository governance import for Paper 1 — complete. The `PROG-SYNC-01`
Paper 1 edit (v16.4) is **done** on branch `paper/v16.4-sync`: the topological-DM
route is withdrawn as a live direction (companion gate `P5-OMEGA-01` `FAILED`),
`P1-CL-011` registered `FAILED`. **The branch is now clear to merge** (pending
reviewer verification and PI authorization of the merge path).

Earlier state: the v16.3 governance import on
`claude/paper1-gated-repo-governance-z478hp` was reviewer-checked and sound but
held from merging solely for this v16.4 withdrawal; that hold is now released.

## Scientific question

None new. This was an infrastructure/governance import: no science was
recomputed, revised, or reinterpreted.

## Locked inputs

- Scientific record: `zetacheng/yukawa-sparc-fits` @ `fd3b2b6…` (byte-for-byte).
- Paper: PI-supplied v16.3 (`paper/yukawa_sparc_paper_v163.tex`).
- Conventions: `CONVENTIONS.md` (dAIC, free-μ vs prior, grids, error-floor vs
  intrinsic-scatter, in-coverage cut, units, `a0_MOND` reference).

## Do not reopen

- The `dAIC` definition (same-config, Yukawa-selected `(rmin, ef)`).
- The two audit defects `P1-A0ERR-01` and `P1-RCSLOPE-01` — registered and
  resolved-per-paper; do not re-fix in a governance sweep.

## Required next input / next items

1. **`P1-A0ERR-01`** — import `a0_profile_likelihood.py` so the re-derived
   `a0 = 0.95 ± 0.03 (stat)` (and the error-model systematic band) is
   reproducible in-repo; add a regression anchor.
2. **`P1-RCSLOPE-01`** — no computation outstanding (resolved v13); confirm the
   in-repo sample-dependence anchor if a claim is ever attached.
3. **Test coverage** — `P1-ISCATTER-01`: import `intrinsic_scatter_comparison.py`
   and `heldout_validation.py`, add raw outputs and a regression anchor so
   `P1-CL-007` / the intrinsic-scatter part of `P1-CL-008` are reproducible here.
4. **v13 paper edits** — already implemented in the supplied v16.3 (θ-medium
   language deleted, `r_c` power law restated as sample dependence, `a0` error
   bar re-derived); no further paper edit is pending from this import. Any new
   edit requires reviewer acceptance and PI authorization.

## Expected Codex output

The imported record, populated governance files, and a green regression suite.

## Questions for ChatGPT

None.

## Questions for Claude (reviewer)

File an independent review under `reviews/claude/` so the `SUPPORTED` claims can
be considered for promotion to `VERIFIED`.

## Open decision for the PI

Repository-naming inconsistency: the paper cites the `yukawa-sparc-fits` URL,
but governance now lives in `1-dark-matter-structure`. See the final report.

## Role separation

Unchanged (see `AGENTS.md`): ChatGPT (conceptual), Codex (implementation), Claude
(independent review), PI (authority). Codex must not promote a result to a claim
without review; no `.tex` edit before reviewer acceptance.
