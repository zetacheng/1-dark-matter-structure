"""Fast unit anchors on the real kernel/likelihood functions and the dAIC logic.

Imports the actual production functions (no re-typed constants) and exercises
their mathematical form, the unit convention, and the same-config vs
per-model-best dAIC distinction. Each numeric anchor carries a
mutation-discrimination companion (see tests/_util.py).
"""

import numpy as np
import pandas as pd

import fiducial_rerun as fr
import fiducial_ac_test as fac
import rar_refit as rr
from _util import check_anchor
from conftest import raw


def test_yukawa_kernel_form_and_small_r_limit():
    """K(r) = (1 - e^{-2mr})/r  ->  2m as r->0; positive and decreasing in r."""
    m = 0.1
    # small-r limit
    small = fr.yuk(np.array([1e-6]), m)[0]
    check_anchor(small, 2 * m, tol=1e-3, bump_rel=0.05, label="yukawa small-r -> 2m")
    # explicit value at r=5 kpc, m=0.1  -> (1-e^{-1})/5
    val = fr.yuk(np.array([5.0]), m)[0]
    expected = (1 - np.exp(-1.0)) / 5.0
    check_anchor(val, expected, tol=1e-9, bump_rel=1e-3, label="yukawa(5,0.1)")
    r = np.array([1.0, 2.0, 4.0, 8.0])
    k = fr.yuk(r, m)
    assert np.all(k > 0) and np.all(np.diff(k) < 0)


def test_nfw_kernel_value():
    """NFW kernel (ln(1+x) - x/(1+x))/r at r=10, rs=5  (x=2)."""
    val = fr.nfw(np.array([10.0]), 5.0)[0]
    x = 2.0
    expected = (np.log(1 + x) - x / (1 + x)) / 10.0
    check_anchor(val, expected, tol=1e-9, bump_rel=1e-3, label="nfw(10,5)")


def test_rar_interpolation_deep_and_newtonian_limits():
    """nu(y)=1/(1-e^{-sqrt(y)}): g_pred=g*nu(g/a0) -> g (high g), sqrt(g a0) (low g)."""
    a0 = 1.2e-10
    g_hi = 1e-8  # >> a0
    gpred_hi = g_hi * rr.nu(g_hi / a0)
    check_anchor(gpred_hi, g_hi, tol=g_hi * 1e-3, bump_rel=0.01,
                 label="RAR Newtonian limit g_pred->g_bar")
    g_lo = 1e-15  # << a0 (deep enough that the sqrt(g/a0)/2 correction is <0.2%)
    gpred_lo = g_lo * rr.nu(g_lo / a0)
    deep = np.sqrt(g_lo * a0)
    check_anchor(gpred_lo, deep, tol=deep * 0.01, bump_rel=0.05,
                 label="RAR deep-MOND limit g_pred->sqrt(g_bar a0)")


def test_unit_convention_and_reference_a0():
    """(km/s)^2/kpc -> m/s^2 factor and the a0_MOND reference value."""
    check_anchor(fac.KMS2_PER_KPC_TO_SI, 1e6 / 3.0857e19, tol=1e-30,
                 bump_rel=1e-6, label="km^2/s^2/kpc -> SI")
    check_anchor(fac.A0_MOND, 1.2e-10, tol=1e-24, bump_rel=1e-6, label="a0_MOND reference")


def test_daic_same_config_vs_permodel_invariant():
    """Per galaxy dAIC_permodel >= dAIC: NFW's own-best AIC <= its same-config AIC.

    This is the structural signature of the paper's dAIC definition
    (same Yukawa-selected config) vs the diagnostic per-model-best column.
    """
    df = pd.read_csv(raw("fiducial/raw/fiducial_rerun.csv"))
    both = df.dropna(subset=["dAIC", "dAIC_permodel"])
    assert len(both) > 150
    # invariant holds for every galaxy (float slack)
    assert np.all(both["dAIC_permodel"] >= both["dAIC"] - 1e-9)
    # and the two definitions genuinely differ on a nontrivial fraction
    assert (both["dAIC_permodel"] > both["dAIC"] + 1e-6).mean() > 0.1
    # medians land on the paper values and in the correct order (permodel more NFW-favoured)
    check_anchor(both["dAIC"].median(), 6.6, tol=0.15, bump_rel=0.05,
                 label="median dAIC (same-config)")
    check_anchor(both["dAIC_permodel"].median(), 9.5, tol=0.2, bump_rel=0.05,
                 label="median dAIC_permodel")


def test_committed_raw_is_readable_and_shaped():
    """The imported record is present and has the expected row counts (cheap guard)."""
    counts = {
        "fiducial/raw/fiducial_rerun.csv": 175,
        "ac-test/raw/fiducial_ac_test.csv": 33,
        "ac-test/raw/clustering_test_results.csv": 100,
        "ml-prior/raw/ml_prior_lognormal.csv": 175,
        "ml-prior/raw/mufixed_rerun.csv": 175,
        "refit/raw/rar_refit.csv": 175,
        "nuisance/raw/nuisance_comparison.csv": 175,
    }
    for rel, n in counts.items():
        assert len(pd.read_csv(raw(rel))) == n, rel
