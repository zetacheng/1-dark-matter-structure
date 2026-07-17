"""Regression anchors for P1-AC-01 (backs P1-CL-003, P1-CL-004).

Both a_c tests are fast (interpolation on committed fit tables), so they run in
the default suite. Imports the real compute_ac_table from each script.
"""

import numpy as np
import pandas as pd
import pytest
from scipy import stats

import fiducial_ac_test as fac
import cluster_test as ct
from _util import check_anchor, check_count
from conftest import raw, data_available

pytestmark = pytest.mark.skipif(not data_available(), reason="SPARC data not present")


def _slope_scatter_rho(d):
    x = np.log10(d["Vmax"].values)
    y = np.log10(d["a_c"].values)
    sl, ic, rv, pv, se = stats.linregress(x, y)
    rho, _ = stats.spearmanr(x, y)
    return sl, se, y.std(), rho, 10 ** np.median(y)


def test_fiducial_ac_test():
    """Fiducial (point-source) a_c test: 33 in-coverage, slope 1.09±0.17, etc."""
    rc_df = fac.load_sparc()
    fid = pd.read_csv(raw("fiducial/raw/fiducial_rerun.csv"))
    d, n_fin = fac.compute_ac_table(rc_df, fid)
    check_count(len(d), 33, "fiducial a_c in-coverage count")
    sl, se, scat, rho, med = _slope_scatter_rho(d)
    check_anchor(sl, 1.09, tol=0.02, bump_rel=0.05, label="fiducial a_c slope")
    check_anchor(se, 0.17, tol=0.02, bump_rel=0.20, label="fiducial a_c slope err")
    check_anchor(scat, 0.34, tol=0.01, bump_rel=0.05, label="fiducial a_c scatter")
    check_anchor(rho, 0.72, tol=0.02, bump_rel=0.05, label="fiducial a_c Spearman")
    check_anchor(med / fac.A0_MOND, 0.22, tol=0.01, bump_rel=0.10, label="fiducial median a_c/a0")


def test_extended_ac_test():
    """Extended-source a_c test: 100 galaxies, slope 1.33±0.10, scatter 0.44, rho 0.80."""
    rc_df = ct.load_sparc()
    summ = pd.read_csv(ct.SUMMARY)
    d, n_fin = ct.compute_ac_table(rc_df, summ)
    check_count(len(d), 100, "extended a_c in-coverage count")
    sl, se, scat, rho, med = _slope_scatter_rho(d)
    check_anchor(sl, 1.33, tol=0.02, bump_rel=0.05, label="extended a_c slope")
    check_anchor(scat, 0.44, tol=0.01, bump_rel=0.05, label="extended a_c scatter")
    check_anchor(rho, 0.80, tol=0.02, bump_rel=0.05, label="extended a_c Spearman")
