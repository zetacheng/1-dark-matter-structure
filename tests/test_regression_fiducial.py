"""Regression anchors for P1-FIDUCIAL-01 (backs P1-CL-001, P1-CL-002).

Fast: import the real fit_all/run_gal and re-fit a few galaxies, comparing to the
committed record. Slow: the full 175-galaxy headline numbers.
"""

import numpy as np
import pandas as pd
import pytest

import fiducial_rerun as fr
from _util import check_anchor, check_count
from conftest import raw, data_available

pytestmark = pytest.mark.skipif(not data_available(), reason="SPARC data not present")

COMMITTED = None


def committed():
    global COMMITTED
    if COMMITTED is None:
        COMMITTED = pd.read_csv(raw("fiducial/raw/fiducial_rerun.csv"))
    return COMMITTED


def test_fiducial_fast_subset_matches_record():
    """Re-fit 5 real galaxies with the real fit_all; compare to the committed CSV.

    This exercises the actual production fitting code (not a re-typed constant)
    on real data, fast enough for the default suite.
    """
    ref = committed()
    names = list(ref["Galaxy"].iloc[:5])
    df = fr.load_sparc()
    sub = df[df["ID"].isin(names)]
    got = fr.fit_all(sub).set_index("Galaxy")
    exp = ref[ref["Galaxy"].isin(names)].set_index("Galaxy")
    assert len(got) == len(exp) == len(names)
    for g in names:
        assert bool(got.loc[g, "is_boundary"]) == bool(exp.loc[g, "is_boundary"]), g
        # continuous quantities: relative tolerance (cross-platform float order)
        check_anchor(got.loc[g, "chi2_pt"], exp.loc[g, "chi2_pt"],
                     tol=abs(exp.loc[g, "chi2_pt"]) * 1e-4 + 1e-9, bump_rel=0.02,
                     label=f"{g} chi2_pt")
        if not bool(exp.loc[g, "is_boundary"]):
            check_anchor(got.loc[g, "rc"], exp.loc[g, "rc"],
                         tol=abs(exp.loc[g, "rc"]) * 1e-4 + 1e-9, bump_rel=0.02,
                         label=f"{g} rc")
        if np.isfinite(exp.loc[g, "dAIC"]):
            check_anchor(got.loc[g, "dAIC"], exp.loc[g, "dAIC"],
                         tol=abs(exp.loc[g, "dAIC"]) * 1e-4 + 1e-6, bump_rel=0.05,
                         label=f"{g} dAIC")


@pytest.mark.slow
def test_fiducial_full_headline_numbers():
    """Full 175-galaxy fit reproduces the paper's fiducial summary."""
    s = fr.fit_all(fr.load_sparc())
    fin = s[~s["is_boundary"]]
    da = s["dAIC"].dropna()
    dp = s["dAIC_permodel"].dropna()

    check_count(len(s), 175, "n fitted")
    check_count(len(fin), 101, "n finite rc")
    check_anchor(100 * len(fin) / len(s), 58.0, tol=0.6, bump_rel=0.05, label="finite %")
    check_anchor(fin["rc"].median(), 15.8, tol=0.1, bump_rel=0.02, label="median rc")
    check_anchor(s["chi2_pt"].median(), 1.08, tol=0.01, bump_rel=0.03, label="median chi2/pt")
    check_anchor(da.median(), 6.6, tol=0.1, bump_rel=0.05, label="median dAIC")
    check_count(int((da.abs() <= 2).sum()), 48, "n comparable |dAIC|<=2")
    check_count(int((da > 2).sum()), 117, "n NFW-preferred dAIC>2")
    check_anchor(dp.median(), 9.5, tol=0.15, bump_rel=0.05, label="median dAIC_permodel")
