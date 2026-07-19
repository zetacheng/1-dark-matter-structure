# Paper 1 Migration

## Source

Scientific record: `zetacheng/yukawa-sparc-fits`, commit
`fd3b2b615194ed076df3d45cbe97fd0f2e4f2452`, branch
`claude/repo-setup-rerun-q0wws6` (last pushed 2026-07-13).
Paper source: PI-supplied `paper1_sparc_v163.tex` (v16.3), imported under `paper/`.

## Administrative metadata

- [x] source inventory
- [x] commit provenance (single source commit; recorded per gate)
- [x] branch provenance
- [x] ownership classification (Paper 1 only; companion dark-energy work referenced, not merged)

## Paper source

- [x] latest Paper 1 source imported (`paper/yukawa_sparc_paper_v163.tex`)
- [ ] figures imported (paper figures not supplied; the analysis figures under
      `results/ac-test/figures/` are the reproducible fit/test figures)
- [ ] bibliography imported (self-contained in the `.tex`; no external `.bib` supplied)

## Scientific record

- [x] SPARC data (`MassModels`, Table 1, `summary_v2.csv`) — byte-for-byte
- [x] analysis scripts (import-refactored for testability; logic unchanged)
- [x] raw result CSVs by gate — byte-for-byte
- [x] claim ledger
- [x] gate registry
- [x] decision log
- [x] failed routes (`P1-CL-009`)
- [x] regression tests + regression anchors + mutation detection
- [ ] **intrinsic-scatter comparison artifact** — `intrinsic_scatter_comparison.py`
      absent from the source record (see below)
- [ ] **v13–v16 data-gate artifacts** — `a0_profile_likelihood.py`,
      `heldout_validation.py`, `rc_floor.py` absent from the source record

## Known provenance gaps (the reason this file exists)

The paper (v16.3) is ahead of the imported scientific record. The source repo
`yukawa-sparc-fits` is at the v12-era state and contains only
`fiducial_rerun.py`, `fiducial_ac_test.py`, `cluster_test.py`,
`ml_prior_lognormal.py`, `ml_prior_mufixed.py`, `rar_refit.py`,
`nuisance_comparison.py`, `plot_ac_test.py`. The following are cited in the
paper but were **not** in the source and could not be imported:

| Missing script | Backs | Recorded as |
|---|---|---|
| `intrinsic_scatter_comparison.py` | `P1-CL-007`, intrinsic-scatter part of `P1-CL-008` | `SUPPORTED` (reviewer-reproduced); gap flagged in `results/intrinsic-scatter/` and `P1-ISCATTER-01` |
| `a0_profile_likelihood.py` | `a0 = 0.95±0.03 (stat)` (resolves `P1-A0ERR-01`) | defect `P1-A0ERR-01` recorded RETIRED-per-paper; artifact import pending |
| `heldout_validation.py` | held-out `Δ(−2 ln L) = −4207` | noted in `P1-REFIT-01` / `P1-ISCATTER-01` |
| `rc_floor.py` | v16 `r_c` lower-boundary censoring | noted; not claim-bearing here |

Importing these from the later `yukawa-sparc-fits` state (or from the PI) is
the top migration follow-up; see `HANDOFF.md`.

## Cross-paper exclusions

Companion dark-energy paper (`zetacheng/4-dark-energy-cosmology`) owns the
`Λ_DE²/M_Pl` side of the `a0` coincidence and the equation-of-state calculation
that falsified the θ-medium narrative. Referenced, not merged (`P1-CL-010`).

## Repository-naming note (for the PI)

The scientific record and its paper citation live in `yukawa-sparc-fits`; this
governance repository is `1-dark-matter-structure` (the `N-topic` convention
used by Papers 2–5). The paper's abstract and reproducibility statement cite the
`yukawa-sparc-fits` URL verbatim. This migration does **not** rename anything and
does **not** edit the paper. See the final PI report for the decision item.
