"""Regression anchor for P1-ISCATTER-REPRO-01 (backs P1-CL-007 via reconstruction).

Fast: import the real rar_gal_is/kern_gal_is, re-run a few galaxies at the
committed fitted (a0, f_int), and compare per-galaxy -2lnL to the committed
raw/iscatter_repro.csv. Each anchor carries a committed mutation-discrimination
companion. Tolerances are numerical (cross-platform float order), not
byte-identity. The full 175-galaxy fit (~7 min) is exercised by the script's
bare invocation, not here.
"""

import pandas as pd
import pytest

import intrinsic_scatter_repro as isr
import nuisance_comparison as nc
from _util import check_anchor
from conftest import raw, data_available

pytestmark = pytest.mark.skipif(not data_available(), reason="SPARC data not present")

_GALS = None
_RAW = None
_SUM = None


def _load():
    global _GALS, _RAW, _SUM
    if _GALS is None:
        _GALS = {G["gal"]: G for G in nc.build_gals(nc.load_massmodels(), nc.load_table1())}
        _RAW = pd.read_csv(raw("intrinsic-scatter-repro/raw/iscatter_repro.csv")).set_index("Galaxy")
        _SUM = pd.read_csv(raw("intrinsic-scatter-repro/regen/summary.csv")).iloc[0]
    return _GALS, _RAW, _SUM


def test_reconstruction_reruns_match_record():
    """Re-run rar_gal_is/kern_gal_is on 4 galaxies at the committed (a0, f_int)."""
    gals, ref, s = _load()
    a0, fR, fY, fN = s["a0"], s["f_int_R"], s["f_int_Y"], s["f_int_N"]
    names = list(ref.index[:4])
    for g in names:
        G = gals[g]
        nR = isr.rar_gal_is(G, a0, fR)[0]
        nY = isr.kern_gal_is(G, isr.m_grid, isr.yuk, fY)[0]
        nN = isr.kern_gal_is(G, isr.rs_grid, isr.nfw, fN)[0]
        for got, col, label in [(nR, "nll_R", "RAR"), (nY, "nll_Y", "Yukawa"), (nN, "nll_N", "NFW")]:
            exp = float(ref.loc[g, col])
            check_anchor(got, exp, tol=abs(exp) * 1e-5 + 1e-4, bump_rel=1e-3,
                         label=f"{g} {label} -2lnL")


def test_committed_summary_is_self_consistent():
    """The reconstruction's own committed summary has the expected structure.

    (Guards the record, not the paper: RAR is the reference; Yukawa is penalized,
    NFW favoured; both dAIC are order-1e3; f_int are physical fractions.)
    """
    _, _, s = _load()
    assert s["dAIC_R"] == 0.0
    assert s["dAIC_Y"] > 1000 and s["dAIC_N"] < -1000          # sign + order
    assert 1000 < abs(s["dAIC_Y"]) < 1e5 and 1000 < abs(s["dAIC_N"]) < 1e5
    for f in (s["f_int_R"], s["f_int_Y"], s["f_int_N"]):
        assert 0.001 < f < 0.5                                  # inside the fitted bounds
    assert 0.5e-10 <= s["a0"] <= 2.5e-10                        # inside the a0 grid
