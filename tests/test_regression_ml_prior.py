"""Regression anchors for P1-MLPRIOR-01 (backs P1-CL-005, P1-CL-006, P1-CL-009).

Slow: full 175-galaxy fits under the lognormal prior and the mu=1 variant.
"""

import pytest

import ml_prior_lognormal as mll
import ml_prior_mufixed as mmf
from _util import check_anchor, check_count
from conftest import data_available

pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(not data_available(), reason="SPARC data not present"),
]


def test_lognormal_prior_collapse():
    """Lognormal 0.1-dex prior: finite 12/163, median finite rc 6.4, chi2 1.14, dAIC +7.7."""
    s = mll.fit_all(mll.load_sparc())
    fin = s[~s["is_boundary"]]
    da = s["dAIC"].dropna()
    check_count(len(s), 175, "n fitted (lognormal)")
    check_count(len(fin), 12, "n finite rc (lognormal)")
    check_anchor(fin["rc"].median(), 6.4, tol=0.1, bump_rel=0.05, label="median finite rc (lognormal)")
    check_anchor(s["chi2_pt"].median(), 1.14, tol=0.01, bump_rel=0.03, label="median chi2/pt (lognormal)")
    check_anchor(da.median(), 7.7, tol=0.1, bump_rel=0.05, label="median dAIC (lognormal)")


def test_mufixed_collapse():
    """mu fixed at unity: finite 4/171, chi2 1.48, dAIC +6.6, Yukawa-preferred 0."""
    s = mmf.fit_all(mmf.load_sparc())
    fin = s[~s["is_boundary"]]
    da = s["dAIC"].dropna()
    check_count(len(s), 175, "n fitted (mu=1)")
    check_count(len(fin), 4, "n finite rc (mu=1)")
    check_anchor(s["chi2_pt"].median(), 1.48, tol=0.02, bump_rel=0.03, label="median chi2/pt (mu=1)")
    check_anchor(da.median(), 6.6, tol=0.1, bump_rel=0.05, label="median dAIC (mu=1)")
    check_count(int((da < -2).sum()), 0, "Yukawa-preferred count (mu=1)")
