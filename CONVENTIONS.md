# Convention Registry

No calculation may begin until every convention relevant to that calculation is
filled, reviewed, and locked. Convention changes must be explicit and recorded
in `DECISION_LOG.md`. These conventions describe Paper 1 (*Dark Matter Structure
and Galaxy Phenomenology*) — an empirical rotation-curve analysis. They are the
conventions the analysis actually relies on; several have already caused a
reproducibility discrepancy and are therefore stated in full rather than assumed.

## Model-comparison conventions

| Convention | Locked definition | Why it is load-bearing |
|---|---|---|
| **`dAIC` (headline)** | `dAIC = AIC_Yukawa − AIC_NFW` with **both kernels fitted on the same data cut and the same error floor** — specifically the `(rmin, ef)` configuration **selected by the Yukawa fit**. AIC is comparable only on identical data with an identical noise model. | Comparing each model at its own AIC-optimal cut changes the number; this exact ambiguity produced a reproducibility discrepancy. Fiducial median `dAIC = +6.6` under this definition. |
| **`dAIC_permodel` (diagnostic only)** | `AIC_Yukawa − AIC_NFW` with **each kernel at its own AIC-optimal `(rmin, ef)`**. Kept as a diagnostic column, never as the headline. | Fiducial median `+9.5` — further in NFW's favour. Must not be quoted as the model-comparison result. |
| **AIC** | `AIC = (−2 ln L) + 2k`, `k` = number of parameters actually free at the optimum (`1 + (μ>0) + (B>0)` for the Yukawa/NFW WLS; `+1` global for the single-`a0` RAR model). | Parameter count differs across the free-μ, prior-constrained, and μ-fixed variants. |

## Fit-configuration conventions

| Convention | Locked definition |
|---|---|
| **Free-μ vs prior-constrained** | *Free-μ*: stellar mass-to-light `μ` is a free per-galaxy WLS amplitude (`μ ≥ 0`, unbounded above). *Prior-constrained*: `μ` carries a lognormal prior on `log10 μ` centred at `μ = 1` with 0.1-dex scatter (Li et al. 2020), or is fixed at `μ = 1`. The free-μ finite-`r_c` result is a **kernel-shape diagnostic**, not a physical claim; the physical claim uses the prior. |
| **μ range** | `μ ≥ 0`, unbounded above (not `μ ∈ [0, 10]`). |
| **Fixed grids** | Yukawa mass scale `m`: `logspace(0.00125, 0.5, 140)` (so `r_c = 1/m`); NFW scale `r_s`: `logspace(0.5, 200.0, 80)`; μ grid (prior runs): `linspace(−0.6, 0.6, 61)` in `log10 μ` (0.02 dex); inner-radius cuts `rmin ∈ {0.0, 2.0, 3.0}` kpc; error floors `ef ∈ {6.0, 4.0, 3.0}` km/s. |
| **Fitting space** | Weighted least squares in **`V²` space** (`y = V_obs² − V_gas²`), amplitudes `μ` and `B` solved linearly per kernel scale. The `μ`-fixed variant fits `B` only. |
| **Error-floor model** | Per-point σ = `max(eV, ef)`; `ef` scanned as above (fiducial/robustness) or fixed (`6` km/s for the RAR refit). |
| **Intrinsic-scatter model** | Alternative to the error floor: a **global fitted intrinsic-scatter fraction `f_int`** enters the likelihood (no error floor). This is the paper's headline single-`a0`/three-model likelihood and is **distinct** from the error-floor comparison; the two give different `dAIC`. |
| **In-coverage cut (`a_c` test)** | The characteristic-acceleration test uses only galaxies whose best-fit `r_c ≤` the last measured radius (`r_c` inside the data coverage). **No extrapolation.** Pre-registered. |
| **Boundary flag** | A Yukawa fit with `m` within 1% of `M_MIN` is flagged `is_boundary` (no finite `r_c`); these are excluded from finite-`r_c` statistics. |

## Units and reference values

| Convention | Locked value |
|---|---|
| **Acceleration unit conversion** | `(km/s)²/kpc → m/s²` factor = `1e6 / 3.0857e19` (i.e. `1 kpc = 3.0857e19 m`). |
| **`a0_MOND` reference** | `a0_MOND = 1.2 × 10⁻¹⁰ m/s²`, used as a **reference value for plots and ratios, not a fitted quantity**. |
| **Fitted `a0`** | The single-`a0` refit's `a0` is a **fitted** parameter and must be reported with its likelihood interval and the error-model systematic band; it is never conflated with the `a0_MOND` reference. See `GATES.md` `P1-A0ERR-01`. |
| **Scale relation** | `a0 ~ Λ_DE²/M_Pl ~ cH0/2π` is stated (paper v16.3) as a numerical coincidence **between two observed numbers**, owing nothing to the framework. It is not a derived prediction. See claim `P1-CL-010`. |

## Data conventions

| Convention | Locked value |
|---|---|
| **Sample** | All 175 SPARC galaxies (Lelli, McGaugh & Schombert 2016). |
| **Rotation-curve decomposition** | `V_bar² = V_gas² + μ (V_disk² + V_bul²)`; halo/kernel adds `B · K(r)`. |
| **Distance / inclination nuisances** | Gaussian priors from SPARC Table 1 (`e_D/D`, `e_Inc`); scalings `r → d·r`, `V_bar² → d·V_bar²`, `V_obs → V_obs sin(i0)/sin(i)` (nuisance comparison only). |

## Not yet imported

Any convention required by a future gate and not listed above is `NOT YET
IMPORTED` and must be locked in that gate's specification before code runs.
