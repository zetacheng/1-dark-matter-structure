# Data

Immutable raw inputs. These files are imported byte-for-byte from
`zetacheng/yukawa-sparc-fits` (commit `fd3b2b6…`) and must never be edited.

| File | Source URL | Provenance |
|------|-----------|-----------|
| `MassModels_Lelli2016c.mrt` | <https://astroweb.case.edu/SPARC/> | SPARC mass models for 175 disk galaxies, Lelli, McGaugh & Schombert (2016), AJ 152, 157. Public SPARC database. |
| `SPARC_Lelli2016c.mrt` | <https://astroweb.case.edu/SPARC/> | SPARC Table 1 (Galaxy Sample): distances, inclinations and their errors (`e_D`, `e_Inc`), Hubble type, quality flag `Q`, for the same 175 galaxies. Used by `nuisance_comparison.py` for the distance/inclination Gaussian priors. |
| `summary_v2.csv` | derived | Per-galaxy Yukawa-vs-NFW fit summary (175 rows): `Galaxy`, `is_boundary`, `best_rc`, `best_mu`, `best_chi2_pt`, etc. Produced by the fiducial fitting pipeline; input to `cluster_test.py`. |

The scripts read these from `data/` by default; override with the `SPARC_MRT`,
`SUMMARY_CSV`, and `SPARC_T1` environment variables (see `scripts/_paths.py`).

Original SPARC dataset home page: <https://astroweb.case.edu/SPARC/>
(the mass-models README historically also linked <http://astroweb.cwru.edu/SPARC/>,
now redirected to the case.edu host).
