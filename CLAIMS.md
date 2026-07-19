# Claim Ledger

Allowed claim statuses are `PROPOSED`, `SUPPORTED`, `VERIFIED`, `FAILED`, `RETIRED`, `CONDITIONAL`, and `INCONCLUSIVE`.

`VERIFIED` requires a closed gate, reproducible artifacts, and reviewer acceptance. `SUPPORTED` is weaker than `VERIFIED` and must not be presented as equivalent. Failed and retired claims remain recorded for audit and must not be deleted.

**Status of this ledger (2026-07-16).** Registered against paper **v16.3**
(`paper/yukawa_sparc_paper_v163.tex`). Every entry below was independently
reproduced by the reviewer on a clean Linux environment (Python 3.12.3, numpy
2.4.4) and re-run at import; they are therefore `SUPPORTED`, **not** `VERIFIED`
— no independent reviewer record exists in *this* repository yet
(`reviews/claude/` is empty). Where the paper is ahead of the imported
scientific record, the gap is stated in the Evidence column and in
`MIGRATION.md`.

| Claim ID | Claim | Status | Evidence | Gate | Paper section | Last reviewed |
|---|---|---|---|---|---|---|
| P1-CL-001 | Free-μ fiducial: 175 fitted, 101 finite `r_c` (58%), median `r_c` 15.8 kpc, median χ²/pt 1.08. | SUPPORTED | `scripts/fiducial_rerun.py` → `results/fiducial/raw/fiducial_rerun.csv`; reproduced exact 2026-07-16. | P1-FIDUCIAL-01 | Sec.~5 Results (`sec:results`), Overview `tab:overview` | 2026-07-16 |
| P1-CL-002 | Same-config median `dAIC` = +6.6; 48 comparable (27%); 117 NFW-preferred (67%). Per-model-best alternative: +9.5. | SUPPORTED | `scripts/fiducial_rerun.py` → `results/fiducial/raw/fiducial_rerun.csv` (`dAIC`, `dAIC_permodel`); reproduced exact 2026-07-16. `dAIC` convention: `CONVENTIONS.md`. | P1-FIDUCIAL-01 | Sec.~6 Comparison with NFW (`sec:nfw`), `tab:overview` | 2026-07-16 |
| P1-CL-003 | Fiducial a_c test: 33 in-coverage galaxies, slope 1.09 ± 0.17, scatter 0.34 dex, median 0.22 a0, Spearman ρ = 0.72. | SUPPORTED | `scripts/fiducial_ac_test.py` → `results/ac-test/raw/fiducial_ac_test.csv`; reproduced exact 2026-07-16. | P1-AC-01 | Sec.~7.3 a_c test (`sec:ac-test`) | 2026-07-16 |
| P1-CL-004 | Extended-source a_c test: 100 galaxies, slope 1.33 ± 0.10, scatter 0.44 dex, ρ = 0.80. | SUPPORTED | `scripts/cluster_test.py` → `results/ac-test/raw/clustering_test_results.csv`; reproduced exact 2026-07-16. | P1-AC-01 | Sec.~7.2–7.3 emergent scale / a_c test (`sec:a0`, `sec:ac-test`) | 2026-07-16 |
| P1-CL-005 | Lognormal 0.1-dex μ prior collapses the finite-`r_c` population to 12/163 (7%); median finite `r_c` 6.4 kpc; χ²/pt 1.14; `dAIC` +7.7. | SUPPORTED | `scripts/ml_prior_lognormal.py` → `results/ml-prior/raw/ml_prior_lognormal.csv`; reproduced exact 2026-07-16. | P1-MLPRIOR-01 | Sec.~8.4 Stellar M/L prior (`sec:ml-prior`) | 2026-07-16 |
| P1-CL-006 | μ fixed at unity: 4/171 (2%); χ²/pt 1.48; `dAIC` +6.6; Yukawa-preferred count zero. Survivors are gas-dominated dwarfs. | SUPPORTED | `scripts/ml_prior_mufixed.py` → `results/ml-prior/raw/mufixed_rerun.csv`; reproduced exact 2026-07-16 (counts/medians; "gas-dominated dwarfs" is the paper's characterization of the 4 survivors). | P1-MLPRIOR-01 | Sec.~8.4 Stellar M/L prior (`sec:ml-prior`) | 2026-07-16 |
| P1-CL-007 | Three-model comparison with μ/D/i nuisances and a global intrinsic scatter: RAR single-`a0` `dAIC` 0; Yukawa +4859; NFW −1614. Fitted `f_int`: 0.050 / 0.156 / 0.034. | SUPPORTED | Paper v16.4 Sec.~9 (`sec:refit`) + abstract. Original script `intrinsic_scatter_comparison.py` is lost (`P1-ISCATTER-01`, external-evidence-only). **Now backed in-repo by an independent blind reconstruction** (`P1-ISCATTER-REPRO-01`, 2026-07-19): pre-registered, computed blind, then compared — `dAIC` Yukawa **+4857** / NFW **−1621**, `f_int` 0.0515/0.1577/0.0330, `a0` 9.777e-11, all within the pre-registered tolerances (`results/intrinsic-scatter-repro/COMPARISON.md`). Caveat: the reconstruction reuses `nuisance_comparison.py` (shared machinery, not clean-room), so it stays `SUPPORTED`, not `VERIFIED`. The error-floor analog (`P1-NUISANCE-01`) uses a *different* likelihood (+9660/−2092 at floor 6). | P1-ISCATTER-REPRO-01 (recon); P1-ISCATTER-01 (lost original) | Sec.~9 Single-`a0` refit (`sec:refit`) | 2026-07-19 |
| P1-CL-008 | The single-`a0` fit gives `a0 = 9.58e-11 m/s²` under the intrinsic-scatter likelihood; `1.046e-10` and `1.28e-10` under 6 and 3 km/s error floors. | SUPPORTED | Floor values reproduced exact 2026-07-16: `scripts/nuisance_comparison.py 6` → 1.046e-10, `… 3` → 1.279e-10 (`results/nuisance/raw/nuisance_comparison.csv`, the floor-3 run). Intrinsic-scatter 9.58e-11 rests on the absent `intrinsic_scatter_comparison.py`. **v16.3 headline** uses the later profiled fit `a0 = 0.95 ± 0.03 (stat)`, systematics to 1.28 — see `P1-A0ERR-01`. | P1-NUISANCE-01 / P1-ISCATTER-01 | Sec.~7.2 emergent scale (`sec:a0`), Sec.~9 refit (`sec:refit`) | 2026-07-16 |
| P1-CL-009 | The Yukawa kernel's finite-`r_c` population is robust to a physical stellar normalization. | FAILED | Falsified: collapses 58% → 7% (lognormal) / 2% (μ = 1). Evidence `results/ml-prior/` (`P1-MLPRIOR-01`); reproduced exact 2026-07-16. A failed claim retained for audit. | P1-MLPRIOR-01 | Sec.~8.4 Stellar M/L prior (`sec:ml-prior`); Sec.~8 Robustness (`sec:robust`) | 2026-07-16 |
| P1-CL-010 | The galactic acceleration scale is `a0 ~ Λ_DE²/M_Pl ~ cH0/2π`, tying the SPARC scale to the dark-energy sector. | RETIRED | **Reconciled to v16.3:** the causal "tying" reading is withdrawn. v16.3 (abstract, `sec:a0`, `sec:conclusions`) states the relation as a numerical coincidence *between two observed numbers* that "owes nothing to the framework"; the fitted range (0.96–1.28)e-10 brackets the canonical value but the microscopic `K(X)` shape is underived and the RAR interpolation function is a phenomenological stand-in. Cross-repo dependency: companion dark-energy paper `zetacheng/4-dark-energy-cosmology` (owns the `Λ_DE²/M_Pl` side; its equation-of-state calculation terminated the θ-medium mechanism). | — (not a gated computation) | Sec.~7.2 emergent scale (`sec:a0`); Sec.~10 Conclusions (`sec:conclusions`) | 2026-07-16 |
| P1-CL-011 | The topological-DM route (negative-quartic contraction vs an endogenous isoscalar-vector repulsion) yields a nonlocal continuum dark-matter object — the "live microscopic direction" for Paper 1's halo, registered in v16.3 future-directions. | FAILED | **Cross-repo dependency; Paper 1 owns no computation here.** Companion gate `P5-OMEGA-01` in `zetacheng/5-topological-sector` (Status `FAIL`, reviewer record `reviews/claude/2026-07-16-p5-omega-01.md`): the competition was computed — the vector repulsion saturates (bounded in radius by the composite cutoff, bounded in coupling by RPA screening) while the negative-quartic contraction diverges, so the energy collapses to a cutoff-scale minimum with **no continuum window at any coupling**. Identified as this route by `0-programme/reviews/PROG-SYNC-01.md` (proved by quotation against the `.tex`). Withdrawn as a live direction in paper **v16.4** and recorded among the closed routes; the paper's conclusions rest on none of the future-directions routes. | — (cross-repo: `P5-OMEGA-01`, `5-topological-sector`) | Sec.~10.1 Future directions (`sec:future`); v16.4 withdrawal | 2026-07-19 |

## Reconciliation note (task-vs-paper)

This ledger was requested against a v12-era snapshot (P1-CL-010 as `PROPOSED`
tying the scales; the two audit defects `OPEN`). The PI-supplied paper is
v16.3, which **supersedes** that snapshot: it recast the a0 relation as a
coincidence (hence `P1-CL-010` = `RETIRED`, not `PROPOSED`) and resolved both
audit defects (see `GATES.md` `P1-A0ERR-01`, `P1-RCSLOPE-01`). Per PI direction
(2026-07-16) the ledger is reconciled to v16.3. Section numbers are approximate
(the `.tex` uses `\label`s, not fixed numbers): the cited `\label`s are exact.

**v16.4 update (2026-07-19).** Paper v16.4 withdraws the topological-DM route
from future-directions (companion gate `P5-OMEGA-01` `FAILED`). `P1-CL-011` is
added at `FAILED`/closed so that failure is auditable from Paper 1's side. No
data-side claim and no other status changed; `P1-CL-010` is untouched.
