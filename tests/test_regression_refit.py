"""Regression anchor for P1-REFIT-01 (part of the P1-CL-008 evidence chain).

Slow: full single-a0 RAR-kernel scan over 175 galaxies.
"""

import pytest

import rar_refit as rr
from _util import check_anchor, check_count
from conftest import data_available

pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(not data_available(), reason="SPARC data not present"),
]


def test_single_a0_refit():
    """Fixed-config lognormal-prior single-a0 refit: a0 ~ 8.83e-11, median chi2/pt 1.35."""
    gals = rr.build_gals(rr.load_sparc())
    a0, lo, hi, per = rr.fit_a0(gals)
    check_count(len(per), 175, "n galaxies (rar refit)")
    check_anchor(a0, 8.83e-11, tol=0.03e-11, bump_rel=0.01, label="rar refit a0")
    check_anchor(per["chi2_pt"].median(), 1.35, tol=0.02, bump_rel=0.03, label="median chi2/pt (rar refit)")
    # this fixed-config a0 is deliberately NOT the paper headline a0 (see P1-A0ERR-01)
    assert 8.0e-11 < a0 < 9.6e-11
