# Progress

## Paper identity

Paper 1 — Dark Matter Structure and Galaxy Phenomenology
Repository: `1-dark-matter-structure`
Scientific record source: `zetacheng/yukawa-sparc-fits` (commit `fd3b2b6…`)

## Current version

**v16.3** — `paper/yukawa_sparc_paper_v163.tex` (PI-supplied 2026-07-16).

## Current scientific status

Scientific record imported and registered against v16.3. Six computation gates
reproduced exactly at import (`P1-FIDUCIAL-01`, `P1-AC-01`, `P1-MLPRIOR-01`,
`P1-REFIT-01`, `P1-NUISANCE-01`); one gate suspended for a missing artifact
(`P1-ISCATTER-01`). Claim ledger and gate registry populated; regression suite
with mutation detection added.

## Verified results

**None.** No independent reviewer record exists in this repository yet, so no
claim is `VERIFIED`. Claims `P1-CL-001` … `P1-CL-008` are `SUPPORTED`
(reviewer-reproduced on a clean environment and re-run at import).

## Failed or retired routes

- `P1-CL-009` — FAILED: the Yukawa finite-`r_c` population is not robust to a
  physical stellar normalization (58% → 7% / 2%).
- `P1-CL-010` — RETIRED: the `a0 ~ Λ_DE²/M_Pl` relation is an observed-number
  coincidence (v16.3), not a framework prediction.
- Audit defects `P1-A0ERR-01`, `P1-RCSLOPE-01` — RETIRED (resolved in paper
  v13–v15), registered not silently fixed.

## Active work

Governance import complete on `claude/paper1-gated-repo-governance-z478hp`.

## Blocked items

- `P1-ISCATTER-01` reproduction is blocked on importing
  `intrinsic_scatter_comparison.py` (and `heldout_validation.py`).
- `P1-A0ERR-01`'s in-repo reproduction is blocked on importing
  `a0_profile_likelihood.py`.

## Next administrative action

File an independent reviewer record under `reviews/claude/` so `SUPPORTED`
claims can be considered for `VERIFIED`; import the missing v13–v16 artifacts.

## Last updated

2026-07-16
