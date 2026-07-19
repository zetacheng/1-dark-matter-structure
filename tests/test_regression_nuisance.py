"""Regression anchor for P1-NUISANCE-01 (backs the error-floor a0 in P1-CL-008).

Slow: full three-model nuisance-marginalized comparison at error floor 6.
This is the ERROR-FLOOR likelihood; the paper headline intrinsic-scatter dAIC
values live in P1-ISCATTER-01 (producing script not imported).
"""

import pytest

import nuisance_comparison as nc
from _util import check_anchor, check_count
from conftest import data_available

pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(not data_available(), reason="SPARC data not present"),
]


def test_nuisance_floor6():
    """Floor 6: a0 = 1.046e-10; total AIC RAR 26688 / Yukawa 36347 / NFW 24596."""
    assert nc.EF == 6.0  # module default; main() would override from argv
    t1 = nc.load_table1()
    gals = nc.build_gals(nc.load_massmodels(), t1)
    check_count(len(gals), 175, "n galaxies matched (nuisance)")
    res, a0, lo, hi = nc.run(gals)
    aR, aY, aN = nc.model_aics(res)
    check_anchor(a0, 1.046e-10, tol=0.01e-10, bump_rel=0.02, label="nuisance a0 (floor 6)")
    check_anchor(aR, 26688, tol=5, bump_rel=0.01, label="AIC RAR (floor 6)")
    check_anchor(aY, 36347, tol=5, bump_rel=0.01, label="AIC Yukawa (floor 6)")
    check_anchor(aN, 24596, tol=5, bump_rel=0.01, label="AIC NFW (floor 6)")
    # ordering: RAR (1 global param) beats the 2x175-param Yukawa; NFW keeps an edge
    assert aY > aR > aN
