"""P1-ISCATTER-REPRO-01 — 2026 independent reconstruction of the intrinsic-scatter
three-model comparison (RAR single-a0 / Yukawa / NFW).

This is NOT the lost original `intrinsic_scatter_comparison.py`. It rebuilds the
calculation from the pre-registration
(`derivations/p1-iscatter-repro/PREREGISTRATION.md`), reusing the verified
machinery of `nuisance_comparison.py` (SPARC loading, mu/d/i nuisance grids and
priors, kernels, RAR nu, kernel-scale grids) and changing ONLY the noise model:
the error floor is replaced by a single global fitted fractional intrinsic
scatter per model,

    sigma_tot,i^2 = (e_V,i s)^2 + (f_int V_obs,i s)^2 ,   s = sin i0 / sin i .

Blind: this script neither reads nor prints the paper's target values. Run bare:
    python -m scripts.intrinsic_scatter_repro
Outputs go only to results/intrinsic-scatter-repro/ (the reconstruction gate).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

import nuisance_comparison as nc          # reuse verified machinery (unmodified)
from _paths import MRT, T1, require

REPO_ROOT = os.path.dirname(_HERE)
OUT = os.path.join(REPO_ROOT, "results", "intrinsic-scatter-repro")

# Reused, unmodified, from nuisance_comparison:
KM = nc.KM
MUG, PMU = nc.MUG, nc.PMU
m_grid, rs_grid = nc.m_grid, nc.rs_grid
nu, yuk, nfw = nc.nu, nc.yuk, nc.nfw

FINT_BOUNDS = (1e-3, 0.5)          # pre-registered
A0_GRID = np.logspace(np.log10(0.5e-10), np.log10(2.5e-10), 25)   # reused


def _sigma(G, f_int):
    """Intrinsic-scatter sigma per (inclination-grid, point): (I, N).

    sigma_tot^2 = (eV s)^2 + (f_int Vobs s)^2, with s = sfac (per inclination).
    Replaces nuisance_comparison's `np.maximum(eV s, EF)`. Depends on V_obs only,
    so the Yukawa/NFW amplitude B stays a linear WLS solution at fixed f_int.
    """
    eV_s = G['eV'][None, :] * G['sfac'][:, None]
    Vo_s = G['Vo'][None, :] * G['sfac'][:, None]
    return np.sqrt(eV_s**2 + (f_int * Vo_s)**2)


def rar_gal_is(G, a0, f_int):
    """RAR single-a0 per-galaxy MAP over (mu, d, i). Mirror of nc.rar_gal, sigma swapped."""
    r, Vo = G['r'], G['Vo']
    Vo_i = Vo[None, :] * G['sfac'][:, None]
    sig_i = _sigma(G, f_int)
    gbar = (G['Vg2'][None, :] + MUG[:, None] * G['S'][None, :]) / r[None, :] * KM
    gbar = np.maximum(gbar, 1e-15)
    gpred = gbar * nu(gbar / a0)
    Vp = np.sqrt(gpred[:, None, :] * G['dgrid'][None, :, None] * r[None, None, :] / KM)
    res = (Vo_i[None, None, :, :] - Vp[:, :, None, :]) / sig_i[None, None, :, :]
    nll = np.sum(res**2, axis=3) + np.sum(np.log(2 * np.pi * sig_i**2), axis=1)[None, None, :]
    obj = nll + PMU[:, None, None] + G['pd_'][None, :, None] + G['pi_'][None, None, :]
    k = np.unravel_index(np.argmin(obj), obj.shape)
    chi2 = np.sum(((Vo_i[k[2]] - Vp[k[0], k[1]]) / sig_i[k[2]])**2)
    return nll[k], chi2 / len(r)


def kern_gal_is(G, grid, kfun, f_int):
    """Yukawa/NFW per-galaxy MAP over (kernel scale, B, mu, d, i). Mirror of nc.kern_gal."""
    r, Vo = G['r'], G['Vo']
    Vo_i = Vo[None, :] * G['sfac'][:, None]
    sig_i = _sigma(G, f_int)
    w_i = 1.0 / sig_i**2
    X = np.array([kfun(r, km) for km in grid])
    xm = np.max(np.abs(X), axis=1, keepdims=True)
    Xn = np.where(xm > 0, X / np.maximum(xm, 1e-300), X)
    y = Vo_i[None, :, :]**2 - G['dgrid'][:, None, None] * G['Vg2'][None, None, :]
    S_d = G['dgrid'][:, None] * G['S'][None, :]
    c_xy = np.einsum('kn,din->kdi', Xn, w_i[None, :, :] * y)
    c_xs = np.einsum('kn,in,dn->kdi', Xn, w_i, S_d)
    c_xx = np.einsum('kn,in,kn->ki', Xn, w_i, Xn)
    best = None
    for mi, mu in enumerate(MUG):
        B = np.clip((c_xy - mu * c_xs) / np.maximum(c_xx, 1e-300)[:, None, :], 0, 1e30)
        Vm2 = (G['dgrid'][None, :, None, None] * (G['Vg2'][None, None, None, :] +
               mu * G['S'][None, None, None, :]) + B[:, :, :, None] * Xn[:, None, None, :])
        Vm = np.sqrt(np.maximum(Vm2, 0))
        res = (Vo_i[None, None, :, :] - Vm) / sig_i[None, None, :, :]
        nll = np.sum(res**2, axis=3) + np.sum(np.log(2 * np.pi * sig_i**2), axis=1)[None, None, :]
        obj = nll + PMU[mi] + G['pd_'][None, :, None] + G['pi_'][None, None, :]
        k = np.unravel_index(np.argmin(obj), obj.shape)
        if best is None or obj[k] < best[0]:
            chi2 = np.sum(((Vo_i[k[2]] - Vm[k]) / sig_i[k[2]])**2)
            best = (obj[k], nll[k], chi2 / len(r), bool(B[k] > 0))
    return best[1], best[2], best[3]


def _total_rar(gals, a0, f_int):
    return sum(rar_gal_is(G, a0, f_int)[0] for G in gals)


def _total_kern(gals, grid, kfun, f_int):
    return sum(kern_gal_is(G, grid, kfun, f_int)[0] for G in gals)


def _opt_fint(objective):
    """Bounded 1-D minimize of total -2lnL over f_int (pre-registered)."""
    res = minimize_scalar(objective, bounds=FINT_BOUNDS, method="bounded",
                          options={"xatol": 1e-4})
    return float(res.x), float(res.fun)


def fit_rar(gals):
    """Joint (a0, f_int_R): optimize f_int at each a0 on the grid, pick the best a0."""
    best = None
    for a0 in A0_GRID:
        f_int, tot = _opt_fint(lambda f: _total_rar(gals, a0, f))
        if best is None or tot < best[2]:
            best = (a0, f_int, tot)
    return best  # (a0, f_int_R, total_nll_R)


def fit_kern(gals, grid, kfun):
    f_int, tot = _opt_fint(lambda f: _total_kern(gals, grid, kfun, f))
    return f_int, tot


def run(gals):
    """Full reconstruction. Returns (per_galaxy_df, summary_dict). Blind to targets."""
    n = len(gals)
    a0, fR, _ = fit_rar(gals)
    fY, _ = fit_kern(gals, m_grid, yuk)
    fN, _ = fit_kern(gals, rs_grid, nfw)

    rows = []
    for G in gals:
        nR, cR = rar_gal_is(G, a0, fR)
        nY, cY, bY = kern_gal_is(G, m_grid, yuk, fY)
        nN, cN, bN = kern_gal_is(G, rs_grid, nfw, fN)
        rows.append(dict(Galaxy=G['gal'], Q=G['Q'], inc0=G['inc0'],
                         nll_R=nR, chi_R=cR, nll_Y=nY, chi_Y=cY, bY=bY,
                         nll_N=nN, chi_N=cN, bN=bN, N=len(G['r'])))
    df = pd.DataFrame(rows)

    # AIC / k counting per PREREGISTRATION.md section 6 (f_int: +1 per model).
    kR = 3 * n + 1 + 1                                  # nuisances + a0 + f_int_R
    kY = 3 * n + n + int(df['bY'].sum()) + 1            # nuisances + m + B(>0) + f_int_Y
    kN = 3 * n + n + int(df['bN'].sum()) + 1            # nuisances + r_s + B(>0) + f_int_N
    aR = df['nll_R'].sum() + 2 * kR
    aY = df['nll_Y'].sum() + 2 * kY
    aN = df['nll_N'].sum() + 2 * kN

    summary = dict(
        n=n, a0=a0,
        f_int_R=fR, f_int_Y=fY, f_int_N=fN,
        m2lnL_R=float(df['nll_R'].sum()), m2lnL_Y=float(df['nll_Y'].sum()),
        m2lnL_N=float(df['nll_N'].sum()),
        k_R=kR, k_Y=kY, k_N=kN,
        AIC_R=float(aR), AIC_Y=float(aY), AIC_N=float(aN),
        dAIC_R=0.0, dAIC_Y=float(aY - aR), dAIC_N=float(aN - aR),
        med_chi2_R=float(df['chi_R'].median()), med_chi2_Y=float(df['chi_Y'].median()),
        med_chi2_N=float(df['chi_N'].median()),
    )
    return df, summary


def main():
    require(T1, "Download SPARC_Lelli2016c.mrt (Table 1) and place it in data/.")
    require(MRT, "Download MassModels_Lelli2016c.mrt and place it in data/.")
    os.makedirs(os.path.join(OUT, "raw"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "regen"), exist_ok=True)

    t1 = nc.load_table1()
    gals = nc.build_gals(nc.load_massmodels(), t1)
    df, s = run(gals)

    df.to_csv(os.path.join(OUT, "raw", "iscatter_repro.csv"), index=False)
    pd.DataFrame([s]).to_csv(os.path.join(OUT, "regen", "summary.csv"), index=False)

    lines = [
        "P1-ISCATTER-REPRO-01 — 2026 independent reconstruction (blind output)",
        f"galaxies matched: {s['n']}",
        f"fitted a0 (RAR): {s['a0']:.4e} m/s^2",
        "",
        f"{'model':<16}{'-2lnL':>12}{'k':>8}{'AIC':>12}{'dAIC_vs_RAR':>14}{'f_int':>9}{'med chi2/pt':>13}",
        f"{'RAR single-a0':<16}{s['m2lnL_R']:>12.1f}{s['k_R']:>8}{s['AIC_R']:>12.1f}{s['dAIC_R']:>+14.0f}{s['f_int_R']:>9.4f}{s['med_chi2_R']:>13.3f}",
        f"{'Yukawa':<16}{s['m2lnL_Y']:>12.1f}{s['k_Y']:>8}{s['AIC_Y']:>12.1f}{s['dAIC_Y']:>+14.0f}{s['f_int_Y']:>9.4f}{s['med_chi2_Y']:>13.3f}",
        f"{'NFW':<16}{s['m2lnL_N']:>12.1f}{s['k_N']:>8}{s['AIC_N']:>12.1f}{s['dAIC_N']:>+14.0f}{s['f_int_N']:>9.4f}{s['med_chi2_N']:>13.3f}",
    ]
    txt = "\n".join(lines) + "\n"
    with open(os.path.join(OUT, "regen", "summary.txt"), "w") as fh:
        fh.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
