# Gate Registry

Allowed gate statuses are `PROPOSED`, `SPECIFIED`, `RUNNING`, `PASS`, `FAIL`, `INCONCLUSIVE`, `SUSPENDED`, `RETIRED`.

Registered against paper **v16.3** on 2026-07-16. The six computation gates
below (`P1-FIDUCIAL-01` … `P1-NUISANCE-01`) were reproduced exactly at import
and are `PASS` on their anchors; their claims are recorded `SUPPORTED` (not
`VERIFIED`) because no independent reviewer record exists in this repository
yet. `P1-ISCATTER-01` is `SUSPENDED` (producing artifact not imported). The two
audit defects (`P1-A0ERR-01`, `P1-RCSLOPE-01`) are recorded `RETIRED`
(resolved/superseded by the paper's own v13–v15 work), **not** silently fixed
in this sweep.

---

## P1-FIDUCIAL-01 — Fiducial free-μ Yukawa-vs-NFW fits

Status: PASS

### Scientific question

Across all 175 SPARC galaxies, what free-μ Yukawa fit quality results, what
fraction have a finite core radius `r_c = 1/m`, and how does the kernel compare
to NFW under the same-config `dAIC`?

### Scope

Per-galaxy weighted least squares in `V²` space; free μ; the fixed grids and
9-config `(rmin, ef)` AIC selection in `CONVENTIONS.md`. No priors.

### Locked assumptions

Free μ (`μ ≥ 0`, unbounded); error floor σ = `max(eV, ef)`; boundary flag at
`m` within 1% of `M_MIN`; same-config `dAIC` = Yukawa − NFW at the
Yukawa-selected `(rmin, ef)`.

### Inputs

`data/MassModels_Lelli2016c.mrt` (SPARC, Lelli et al. 2016), commit `fd3b2b6…`.

### Analytic anchors

Yukawa kernel `K(r) = (1 − e^{−2mr})/r`; NFW kernel
`K(r) = [ln(1+x) − x/(1+x)]/r`, `x = r/r_s`. `dAIC` per the convention registry.

### Regression anchors

`tests/test_regression_fiducial.py` (fast few-galaxy import of `run_gal`;
slow full-sample headline numbers) and `tests/test_kernels.py` (kernel forms,
`dAIC` same-config vs per-model logic).

### Kill criterion

Any headline number outside the stated tolerance, or a mismatch between the
same-config and per-model `dAIC` definitions.

### Required computations

`python scripts/fiducial_rerun.py`.

### Required deliverables

Script, immutable raw CSV, provenance, environment, regression anchor.

### Result

175 fitted; 101 finite `r_c` (58%); median `r_c` 15.8 kpc; median χ²/pt 1.08;
median `dAIC` +6.6 (48 comparable, 27%; 117 NFW-preferred, 67%);
`dAIC_permodel` +9.5. Reproduced exact 2026-07-16.

### Reviewer verdict

Reproduced independently (clean env) and at import → claims `SUPPORTED`. No
in-repo independent reviewer record yet → **not** `VERIFIED`.

### Consequences

Backs `P1-CL-001`, `P1-CL-002`. The `dAIC` definition is load-bearing and is
locked in `CONVENTIONS.md` after a prior reproducibility discrepancy.

### Repository branch

`claude/paper1-gated-repo-governance-z478hp`

### Relevant files

`scripts/fiducial_rerun.py`, `results/fiducial/`.

### Date opened / closed

Imported 2026-07-16 / anchors PASS 2026-07-16 (claim promotion pending review).

---

## P1-AC-01 — Characteristic-acceleration (a_c) tests

Status: PASS

### Scientific question

Does `a_c = V(r_c)²/r_c` cluster at a single MOND-like scale, or track `V_max`?

### Scope

Finite-`r_c` galaxies with `r_c` inside the data coverage (pre-registered, no
extrapolation), on both the fiducial (point-source) and extended-source fit
tables.

### Locked assumptions

In-coverage cut `r_c ≤` last measured radius; unit factor `1e6/3.0857e19`;
`a0_MOND = 1.2e-10 m/s²` as a reference, not a fit.

### Inputs

`data/MassModels_Lelli2016c.mrt`; `data/summary_v2.csv`;
`results/fiducial/raw/fiducial_rerun.csv`.

### Analytic anchors

Linear regression of `log a_c` on `log V_max`; Spearman ρ; log-scatter.

### Regression anchors

`tests/test_regression_ac_test.py` (imports `compute_ac_table` from both
scripts; fast on a subsample, slow on the full in-coverage set).

### Kill criterion

Slope, scatter, ρ, median `a_c/a0`, or in-coverage count outside tolerance;
any extrapolated galaxy entering the sample.

### Required computations

`python scripts/fiducial_ac_test.py`; `python scripts/cluster_test.py`.

### Required deliverables

Scripts, raw CSVs, figures, provenance, environment, regression anchor.

### Result

Fiducial: 33 in-coverage; slope 1.09 ± 0.17; scatter 0.34 dex; median 0.22 a0;
ρ 0.72. Extended: 100 galaxies; slope 1.33 ± 0.10; scatter 0.44 dex; ρ 0.80.
Reproduced exact 2026-07-16.

### Reviewer verdict

Reproduced → `SUPPORTED`; not `VERIFIED` (no in-repo reviewer record).

### Consequences

Backs `P1-CL-003`, `P1-CL-004`. `a_c` tracks `V_max` — the kernel demands
acceleration dependence, motivating the single-`a0` refit.

### Repository branch

`claude/paper1-gated-repo-governance-z478hp`

### Relevant files

`scripts/fiducial_ac_test.py`, `scripts/cluster_test.py`,
`scripts/plot_ac_test.py`, `results/ac-test/`.

### Date opened / closed

Imported 2026-07-16 / anchors PASS 2026-07-16.

---

## P1-MLPRIOR-01 — Stellar mass-to-light prior robustness

Status: PASS

### Scientific question

Is the free-μ finite-`r_c` population robust to a physical stellar
mass-to-light normalization?

### Scope

Lognormal 0.1-dex prior on `log10 μ` (Li et al. 2020), and the stronger
`μ = 1` fixed variant; machinery otherwise the fiducial pipeline.

### Locked assumptions

Prior centred at `μ = 1`; μ grid `linspace(−0.6, 0.6, 61)`; same 9-config AIC
selection and same-config `dAIC`.

### Inputs

`data/MassModels_Lelli2016c.mrt`.

### Analytic anchors

Finite/boundary split; median finite `r_c`; median χ²/pt; median `dAIC`;
Yukawa-preferred count.

### Regression anchors

`tests/test_regression_ml_prior.py` (imports `fit_all`/`run_gal_prior`; slow
full-sample headline numbers).

### Kill criterion

Any headline count/median outside tolerance.

### Required computations

`python scripts/ml_prior_lognormal.py`; `python scripts/ml_prior_mufixed.py`.

### Required deliverables

Scripts, raw CSVs, provenance, environment, regression anchor.

### Result

Lognormal: finite/boundary 12/163 (7%); median finite `r_c` 6.4 kpc; χ²/pt 1.14;
`dAIC` +7.7. μ = 1: 4/171 (2%); χ²/pt 1.48; `dAIC` +6.6; Yukawa-preferred 0.
Reproduced exact 2026-07-16.

### Reviewer verdict

Reproduced → `SUPPORTED`; not `VERIFIED`.

### Consequences

Backs `P1-CL-005`, `P1-CL-006`, and the FAILED robustness claim `P1-CL-009`:
the finite-`r_c` population collapses from 58% to 7% / 2%.

### Repository branch

`claude/paper1-gated-repo-governance-z478hp`

### Relevant files

`scripts/ml_prior_lognormal.py`, `scripts/ml_prior_mufixed.py`,
`results/ml-prior/`.

### Date opened / closed

Imported 2026-07-16 / anchors PASS 2026-07-16.

---

## P1-REFIT-01 — Single-a0 RAR-kernel refit

Status: PASS

### Scientific question

Under an acceleration-dependent (RAR) kernel with one global fitted `a0`, a
lognormal μ prior, and a fixed configuration, what single `a0` and fit quality
result?

### Scope

`g_pred = g_bar/(1 − e^{−√(g_bar/a0)})`; global `a0` on `logspace(0.3e-10,
4e-10, 49)`; fixed `rmin = 0`, `σ_f = 6 km/s`.

### Locked assumptions

Lognormal 0.1-dex μ prior; V-space Gaussian −2 ln L; unit factor `1e6/3.0857e19`.

### Inputs

`data/MassModels_Lelli2016c.mrt`.

### Analytic anchors

Best `a0`; median χ²/pt; μ distribution.

### Regression anchors

`tests/test_regression_refit.py` (imports `nu`, `total_nll`, `fit_a0`; slow
full-sample `a0`).

### Kill criterion

`a0` or median χ²/pt outside tolerance.

### Required computations

`python scripts/rar_refit.py`.

### Required deliverables

Script, raw CSV, provenance, environment, regression anchor.

### Result

Best `a0` = 8.83e-11 m/s² (grid-adjacent [8.36e-11, 9.32e-11]); median χ²/pt
1.35; μ median 0.66. Reproduced exact 2026-07-16. **Note:** this fixed-config
value is distinct from the paper headline `a0` — see `P1-NUISANCE-01` and
`P1-A0ERR-01`.

### Reviewer verdict

Reproduced → `SUPPORTED`; not `VERIFIED`.

### Consequences

Part of the evidence chain for `P1-CL-008`; establishes the single-`a0` route.

### Repository branch

`claude/paper1-gated-repo-governance-z478hp`

### Relevant files

`scripts/rar_refit.py`, `results/refit/`.

### Date opened / closed

Imported 2026-07-16 / anchors PASS 2026-07-16.

---

## P1-NUISANCE-01 — Three-model nuisance comparison (error floor)

Status: PASS

### Scientific question

With per-galaxy μ/distance/inclination nuisances marginalized, how do RAR
single-`a0`, Yukawa, and NFW compare by total AIC at fixed error floors, and
what single `a0` results?

### Scope

Three models; MAP over μ (lognormal 0.1 dex), distance (Gaussian `e_D/D`),
inclination (Gaussian `e_Inc`); fixed `rmin = 0`; error floor is the CLI arg.

### Locked assumptions

Distance/inclination scalings in `CONVENTIONS.md`; Table 1 priors from
`data/SPARC_Lelli2016c.mrt`; committed raw CSV is the **floor-3** run.

### Inputs

`data/MassModels_Lelli2016c.mrt`, `data/SPARC_Lelli2016c.mrt`.

### Analytic anchors

Global `a0` per floor; total AICs; per-galaxy median Δnll.

### Regression anchors

`tests/test_regression_nuisance.py` (imports `run`/`model_aics`; slow
full-sample floor-6 `a0` and AICs).

### Kill criterion

`a0` or model AICs outside tolerance at the tested floor.

### Required computations

`python scripts/nuisance_comparison.py 6`; `python scripts/nuisance_comparison.py 3`.

### Required deliverables

Script, raw CSV, provenance, environment, regression anchor.

### Result

Floor 6: `a0` 1.046e-10; AIC RAR 26688 / Yukawa 36347 / NFW 24596. Floor 3:
`a0` 1.279e-10; AIC RAR 29238 / Yukawa 49102 / NFW 24984. Reproduced exact
2026-07-16. **This is the error-floor likelihood**, distinct from the paper's
intrinsic-scatter headline (`P1-ISCATTER-01`).

### Reviewer verdict

Reproduced → `SUPPORTED`; not `VERIFIED`.

### Consequences

Backs the error-floor `a0` values in `P1-CL-008`.

### Repository branch

`claude/paper1-gated-repo-governance-z478hp`

### Relevant files

`scripts/nuisance_comparison.py`, `results/nuisance/`.

### Date opened / closed

Imported 2026-07-16 / anchors PASS 2026-07-16.

---

## P1-ISCATTER-01 — Intrinsic-scatter three-model comparison

Status: SUSPENDED

### Scientific question

Under a global intrinsic-scatter likelihood (fitted `f_int` per model, no error
floor), how do RAR single-`a0`, Yukawa, and NFW compare, in sample and on
held-out galaxies?

### Scope

The paper's headline three-model comparison and the single-`a0` value under the
intrinsic-scatter likelihood.

### Locked assumptions

Global fitted `f_int` per model; no error floor (`CONVENTIONS.md`).

### Inputs

`data/MassModels_Lelli2016c.mrt`, `data/SPARC_Lelli2016c.mrt`.

### Analytic anchors

In-sample `dAIC` RAR 0 / Yukawa +4859 / NFW −1614; `f_int` 0.050 / 0.156 /
0.034; held-out `Δ(−2 ln L) = −4207`; single-`a0` 9.58e-11.

### Regression anchors

None yet — the producing script is absent (see below).

### Kill criterion

(Deferred until the artifact is imported.)

### Required computations

`python scripts/intrinsic_scatter_comparison.py` — **script not present.**

### Required deliverables

Import `intrinsic_scatter_comparison.py` and `heldout_validation.py` from the
later `yukawa-sparc-fits` state, add raw outputs and a regression anchor.

### Result

Not reproducible in this repository. The paper numbers are recorded in
`P1-CL-007` / `P1-CL-008` as `SUPPORTED` (reviewer-reproduced elsewhere). The
present error-floor analog (`P1-NUISANCE-01`) gives different numbers,
confirming the two likelihoods are distinct.

### Reviewer verdict

SUSPENDED pending recovery of the **original** artifact — see
`results/intrinsic-scatter/PROVENANCE.md` and `MIGRATION.md`. The paper's numbers
have since been **independently reconstructed** (gate `P1-ISCATTER-REPRO-01`,
2026-07-19) and fall within the pre-registered tolerances; that reconstruction —
not the lost original — now backs `P1-CL-007`. This gate stays SUSPENDED because
it tracks the lost original artifact specifically.

### Consequences

`P1-CL-007` and the intrinsic-scatter part of `P1-CL-008` are now reproducible
in-repo via the 2026 reconstruction (`P1-ISCATTER-REPRO-01`), with the caveat
that the reconstruction reuses `nuisance_comparison.py` and is not a clean-room
reimplementation.

### Repository branch

`claude/paper1-gated-repo-governance-z478hp`

### Relevant files

`results/intrinsic-scatter/` (raw empty); reconstruction under
`results/intrinsic-scatter-repro/`.

### Date opened / closed

Registered 2026-07-16 / open (SUSPENDED); reconstruction filed 2026-07-19.

---

## P1-ISCATTER-REPRO-01 — Intrinsic-scatter comparison, 2026 reconstruction

Status: PASS

### Scientific question

Does an independent reconstruction (built from the paper's method, blind to its
numbers) confirm the intrinsic-scatter three-model comparison — `dAIC` RAR 0 /
Yukawa +4859 / NFW −1614, `f_int` 0.050/0.156/0.034, `a0` 9.58e-11?

### Scope

Reconstruct the lost `intrinsic_scatter_comparison.py` result by substituting the
intrinsic-scatter likelihood into the verified `nuisance_comparison.py` machinery.
This is a **2026 reconstruction, not the original run**.

### Locked assumptions

Fixed in `derivations/p1-iscatter-repro/PREREGISTRATION.md` **before computing**:
RAR kernel + single global `a0`; μ/d/i nuisance grids and priors reused verbatim;
`σ_tot,i² = (e_V,i s)² + (f_int V_obs,i s)²` with one global `f_int` per model,
Gaussian normalization retained; `a0` 25-point grid; `f_int` bounded-Brent on
`[1e-3, 0.5]`; AIC/k counting stated (`f_int` cancels in `dAIC`, `a0` RAR-only);
all 175 galaxies.

### Inputs

`data/MassModels_Lelli2016c.mrt`, `data/SPARC_Lelli2016c.mrt`.

### Analytic anchors

Per-galaxy `−2 ln L` reproducible from `rar_gal_is`/`kern_gal_is` at the fitted
`(a0, f_int)`; `dAIC` from the pre-registered `k` counting.

### Regression anchors

`tests/test_regression_iscatter_repro.py` (imports `rar_gal_is`/`kern_gal_is`,
re-runs a few galaxies against the committed `raw/iscatter_repro.csv`; committed
mutation-discrimination assertion).

### Kill criterion

Any pre-registered quantity outside its pre-registered tolerance, or wrong sign /
order of magnitude on any `dAIC`.

### Required computations

`python -m scripts.intrinsic_scatter_repro`.

### Result

Reconstruction: `a0` 9.777e-11; `dAIC` Yukawa **+4857**, NFW **−1621**; `f_int`
0.0515 / 0.1577 / 0.0330; median χ²/pt 0.840 / 0.740 / 0.647. **All within the
pre-registered tolerances** (`results/intrinsic-scatter-repro/COMPARISON.md`):
outcome **REPRODUCED**.

### Reviewer verdict

PASS on the pre-registered anchors. Not `VERIFIED`: no independent reviewer
re-run in this repository, and the reconstruction reuses `nuisance_comparison.py`
(shared-machinery caveat in `COMPARISON.md`). Backs `P1-CL-007` as `SUPPORTED`.

### Consequences

Closes the in-repo reproducibility gap for `P1-CL-007` (via reconstruction, not
the lost original). Confirms the paper's headline `dAIC` +4859/−1614.

### Repository branch

`paper/v16.4-sync`

### Relevant files

`scripts/intrinsic_scatter_repro.py`, `derivations/p1-iscatter-repro/`,
`results/intrinsic-scatter-repro/`, `tests/test_regression_iscatter_repro.py`.

### Date opened / closed

Pre-registered + computed + compared 2026-07-19 / PASS 2026-07-19.

---

# Known defects (audit 2026-07-16)

The two entries below were identified in reviewer audit on 2026-07-16. They are
open computations in origin; the paper's own v13–v15 work already addressed
them, so they are recorded here as `RETIRED` (resolved/superseded), **not**
silently re-fixed in this sweep. They block nothing except the claims that rest
on them (`P1-CL-008`'s error bar; no current claim rests on the `r_c` slope).

## P1-A0ERR-01 — The `a0` error bar is not properly derived

Status: RETIRED (resolved — superseded by v13 withdrawal and v15 re-derivation)

### Scientific question

Is the quoted `a0 = 0.96 +0.12 −0.01 e-10` interval sound?

### Scope

The statistical interval on the single-`a0` fit.

### The defect (as found)

The interval came from a `Δ(−2 ln L) = 1` crossing along the `a0` axis on a
discrete grid. Three problems: (1) the −0.01 side is a single grid step and may
be a discreteness artifact; (2) it was not established that `f_int` was
re-profiled at each `a0` rather than held at its global best (the latter
under-estimates the interval); (3) the quoted uncertainty is purely statistical
while the systematic across error models (0.96 → 1.28) is ~20× larger.

### Kill criterion / required computation

Re-derive with `f_int` profiled at each `a0` on a refined grid, and report the
error-model systematic alongside.

### Resolution (per paper record)

v13 **withdrew** the `+0.12/−0.01` slice (conditioned on best-fit `f_int` and
grid-quantized, both bias-narrow); the systematic band 0.96–1.28 was quoted as
dominant. v15 **re-derived** the profiled `a0` (`a0_profile_likelihood.py`,
continuous nuisance polish → `0.95 [0.920, 0.979]e-10`), identified the grid-MAP
staircase noise as the defect of the withdrawn slice, and reported the
statistical (±0.03) vs 5-fold empirical (±0.10) discrepancy as galaxy-level
heterogeneity. v16.3 headline: `a0 = 0.95 ± 0.03 (stat)`, systematics to 1.28.

### Provenance gap (not fully closed in this repository)

The resolving artifact `a0_profile_likelihood.py` is **not present** in the
imported record. The resolution is therefore recorded **per the paper**, not
independently reproduced here; importing that script is an open follow-up
(`MIGRATION.md`, `HANDOFF.md`).

### Consequences

`P1-CL-008`'s statistical error bar is governed by this entry. Do not re-open or
re-fix in this sweep.

### Date opened / closed

Found 2026-07-16 / retired 2026-07-16 (resolved in paper v13–v15; artifact
import pending).

## P1-RCSLOPE-01 — The `r_c`–`V_max` slope is sample-dependent

Status: RETIRED (resolved — superseded by the v13 correction)

### Scientific question

Is the `r_c`–`V_max` relation a power law, and does the "arithmetic
consequence" argument (2 − 0.82 = 1.18 ≈ measured a_c slope 1.09) hold?

### Scope

The `r_c`–`V_max` slope and its use in the a_c-slope argument.

### The defect (as found)

Measured slopes are sample-dependent: 0.82 ± 0.15 (extended-source, n = 156),
1.39 ± 0.22 (fiducial, n = 101), 0.51 ± 0.24 (a_c-test subsample, n = 33). The
"arithmetic consequence" took the slope from one sample and the a_c slope from
another; same-sample arithmetic gives 1.49 and 0.61 respectively, matching
neither. (The n=100 in-coverage extended subsample slope, 0.82 ± 0.11, is
reproducible from `scripts/cluster_test.py`.)

### Kill criterion / required action

Report the spread as evidence of sample dependence rather than as a power law.

### Resolution (per paper record)

v13 **corrected** the arithmetic: the `r_c`–`V_max` slope is reported as
sample-unstable (0.51 / 0.82 / 1.39), the cherry-picked 0.82 → 1.18 line was
removed, and the instability itself is reported as a failure mode; the robust
statement is "`a_c` tracks `V_max`." v16.3 carries this. This resolution **is**
reproducible in-repo from the imported fit tables.

### Consequences

No current claim rests on the `r_c` slope. Paper text edit was implemented in
v13 (tracked historically as a v13 item); nothing outstanding here.

### Date opened / closed

Found 2026-07-16 / retired 2026-07-16 (resolved in paper v13).

---

## Sea–Ice programme gate stubs (PROPOSED)

The gate below is a **stub** created from the programme Sea–Ice research map
(`0-programme:sea-ice/SEA_ICE_RESEARCH_MAP.md`, snapshot 2026-07-19,
re-confirmed against this `GATES.md` before creation — no ID collision with
`P1-FIDUCIAL-01`, `P1-AC-01`, `P1-MLPRIOR-01`, `P1-REFIT-01`,
`P1-NUISANCE-01`, `P1-ISCATTER-01`, `P1-ISCATTER-REPRO-01`, `P1-A0ERR-01`,
`P1-RCSLOPE-01`). It is the real, paper-owned object behind the Sea–Ice
`SI-6` routing alias; the programme repo owns no evidence.

**CLAIMS↔GATES note.** This gate ID has **no** claim row in `CLAIMS.md` yet,
and none is added here. A claim appears only when the gate is actually run.
The CLAIMS↔GATES guard (`tests/test_repository_structure.py ::
test_every_claims_gate_has_a_gates_heading`) checks the CLAIMS→GATES
direction only — every gate ID *cited in* `CLAIMS.md` must have a heading
here — so a gate with no backing claim is tolerated and the guard is not
weakened.

## P1-SEAICE-RAR-01 — Derive the RAR and a universal `a_0` (not fit)

Status: PROPOSED

### Sea–Ice alias

SI-6. Owner: Paper 1.

### Scientific question

Does the effective theory *derive* the radial-acceleration relation (RAR) and
a universal `a_0`, **without inserting** the empirical interpolation function?

### Scope

A **derivation** gate: `g_obs(g_bar)` and `a_0` must come from the interface
elastic response, the bound-mode response, and the resulting modified Poisson
kernel — not from a fit. This is **distinct** from the existing `P1-ISCATTER-*`
and RAR-*fit* gates (`P1-REFIT-01`, `P1-FIDUCIAL-01`, `P1-AC-01`), which fit or
compare kernels to data; here the interpolation may not be an input.

### Locked assumptions

`CONVENTIONS.md`; the galaxy sample and benchmark registered before fitting
(pre-registration policy §5); `a_0` derived from microscopic / interface
parameters, not fitted; the empirical RAR interpolation function may not be
used as an input.

### Inputs

Interface elastic response and bound-mode response from Paper 4
(`P4-SEA-ICE-01`, `P4-BOUND-DM-01`); the modified Poisson kernel derived from
them.

### Dependency

Depends on `P4-SEA-ICE-01` (SI-3) **and** `P4-BOUND-DM-01` (SI-5b) in
`zetacheng/4-dark-energy-cosmology`. Terminal gate of the Sea–Ice critical
chain.

### Kill criterion

The RAR must be inserted, or `a_0` is freely fitted, or the derived shape is
wrong, or there is a lensing–dynamics mismatch → the galactic explanation
fails.

### Required computations

(not started)

### Required deliverables

(not started)

### Result

(not started)

### Reviewer verdict

(not started)

### Consequences

Success would complete the Sea–Ice chain (galaxies from the microscopic
theory); failure leaves the empirical RAR (`P1-CL-007` SUPPORTED) as evidence
for the *phenomenon* only, not for a microscopic derivation.

### Repository branch

`sea-ice/gate-stubs`

### Relevant files

`0-programme:sea-ice/SEA_ICE_RESEARCH_MAP.md`,
`0-programme:sea-ice/SEA_ICE_PREREGISTRATION_POLICY.md`.

### Date opened / closed

Opened 2026-07-20 / Open (PROPOSED stub).
