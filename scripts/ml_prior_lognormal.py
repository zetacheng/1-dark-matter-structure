"""M/L robustness: lognormal stellar mass-to-light prior (MAP).

Repeats the analysis with a Gaussian prior on log10(mu) centred at 0
(mu = 1, the fiducial Upsilon*), scatter 0.1 dex (Li et al. 2020), same
prior for both kernels. mu is selected on a 0.02-dex grid by the
penalized velocity-space -2lnL; B is solved at each mu by the same
V^2-space WLS as the fiducial pipeline. NOTE (documented in the paper):
this estimator differs from the fiducial joint V^2-WLS -- with the prior
switched off it gives a 44/131 (25%/75%) finite/boundary split rather
than the fiducial 101/74; the estimator sensitivity is itself reported.
Reproduces (paper Sec. "Stellar mass-to-light prior"):
finite/boundary 12/163 (7%/93%); median finite r_c 6.4 kpc; median
chi2/pt 1.14; median same-config dAIC +7.7.
Output: results/ml_prior_lognormal.csv

Structure note (2026-07-16, Paper 1 governance import): numerical logic is
byte-identical to the yukawa-sparc-fits original; reorganized into importable
functions (load_sparc, run_gal_prior, fit_all) with a __main__ guard for the
regression suite. Reproduction verified unchanged.
"""
import numpy as np, pandas as pd
from _paths import MRT, RESULTS_DIR

M_MIN, M_MAX, M_STEPS = 0.00125, 0.5, 140
RS_MIN, RS_MAX, RS_STEPS = 0.5, 200.0, 80
RMIN_LIST = [0.0, 2.0, 3.0]
EF_LIST   = [6.0, 4.0, 3.0]
S_DEX     = 0.1
LOGMU     = np.linspace(-0.6, 0.6, 61)          # log10 mu grid (0.02 dex)
MU        = 10.0**LOGMU
PRIOR     = (LOGMU / S_DEX)**2                   # -2 ln p, Gaussian in log10 mu


def load_sparc(path=MRT):
    rows = []
    for line in open(path, encoding='latin-1', errors='replace'):
        p = line.strip().split()
        if len(p) < 8:
            continue
        try:
            float(p[1])
            rows.append((p[0], float(p[2]), float(p[3]), float(p[4]),
                         float(p[5]), float(p[6]), float(p[7])))
        except (ValueError, IndexError):
            continue
    return pd.DataFrame(rows, columns=['ID','R','Vobs','eV','Vgas','Vdisk','Vbul'])


def run_gal_prior(g, rmin, ef, grid, kfun):
    """MAP fit over (kernel scale, mu grid), B by 1D WLS. Returns best dict."""
    g = g[(g['R'] > 0) & (g['R'] >= rmin)].sort_values('R')
    if len(g) < 3:
        return None
    r  = g['R'].values; Vo = g['Vobs'].values; eV = g['eV'].values
    Vg2 = g['Vgas'].values**2
    S   = g['Vdisk'].values**2 + g['Vbul'].values**2
    N   = len(r)
    sig = np.maximum(eV, ef); w = 1.0/sig**2
    y   = Vo**2 - Vg2

    # kernel matrix, normalized per scale as in fiducial pipeline
    X = np.array([kfun(r, km) for km in grid])              # (K, N)
    xm = np.max(np.abs(X), axis=1, keepdims=True)
    Xn = np.where(xm > 0, X/np.maximum(xm, 1e-300), X)      # (K, N)

    # 1D WLS for B given mu:  B = max( sum w X (y - mu S) / sum w X X, 0 )
    c_xy = Xn @ (w*y)                                       # (K,)
    c_xs = Xn @ (w*S)                                       # (K,)
    c_xx = np.einsum('kn,n,kn->k', Xn, w, Xn)               # (K,)
    B = (c_xy[:, None] - np.outer(c_xs, MU)) / np.maximum(c_xx, 1e-300)[:, None]
    B = np.clip(B, 0.0, 1e30)                               # (K, M)

    # V-space -2lnL on the (K, M) grid
    Vm2 = Vg2[None, None, :] + MU[None, :, None]*S[None, None, :] \
          + B[:, :, None]*Xn[:, None, :]
    Vm  = np.sqrt(np.maximum(Vm2, 0.0))                     # (K, M, N)
    res = Vo[None, None, :] - Vm
    nll = np.sum(res**2 * w[None, None, :], axis=2) \
          + np.sum(np.log(2*np.pi*sig**2))                  # (K, M)
    obj = nll + PRIOR[None, :]

    ik, im = np.unravel_index(np.argmin(obj), obj.shape)
    mu = MU[im]; b = B[ik, im]
    chi2 = float(np.sum(((Vo - Vm[ik, im])/sig)**2))
    k = 1 + 1 + (b > 0)                                     # scale + mu + B
    return dict(m=grid[ik], mu=mu, B=b, chi2_pt=chi2/N,
                nll=float(nll[ik, im]), AIC=float(nll[ik, im]) + 2*k,
                obj=float(obj[ik, im]), N=N)


yuk = lambda r, m: (1 - np.exp(-2*m*r))/np.maximum(r, 1e-12)
def nfw(r, rs):
    x = r/rs
    return (np.log(1 + x) - x/(1 + x))/np.maximum(r, 1e-12)

m_grid  = np.logspace(np.log10(M_MIN), np.log10(M_MAX), M_STEPS)
rs_grid = np.logspace(np.log10(RS_MIN), np.log10(RS_MAX), RS_STEPS)


def fit_all(df):
    out = []
    for gal, g in df.groupby('ID', sort=False):
        besty = None; nfw_by_cfg = {}
        for rm in RMIN_LIST:
            for ef in EF_LIST:
                by = run_gal_prior(g, rm, ef, m_grid, yuk)
                if by is not None and (besty is None or by['obj'] < besty['obj']):
                    besty = by; besty['rmin'] = rm; besty['ef'] = ef
                bn = run_gal_prior(g, rm, ef, rs_grid, nfw)
                if bn is not None:
                    nfw_by_cfg[(rm, ef)] = bn
        if besty is None:
            continue
        is_bnd = abs(besty['m'] - M_MIN)/M_MIN < 0.01
        bn_same = nfw_by_cfg.get((besty['rmin'], besty['ef']))
        dAIC = besty['AIC'] - bn_same['AIC'] if bn_same is not None else np.nan
        out.append(dict(Galaxy=gal, m=besty['m'],
                        rc=(np.nan if is_bnd else 1/besty['m']),
                        mu=besty['mu'], B=besty['B'], chi2_pt=besty['chi2_pt'],
                        is_boundary=is_bnd, dAIC=dAIC,
                        rmin=besty['rmin'], ef=besty['ef'], N=besty['N']))
    return pd.DataFrame(out)


def main():
    df = load_sparc()
    s = fit_all(df)
    out_csv = RESULTS_DIR / "ml_prior_lognormal.csv"
    s.to_csv(out_csv, index=False)
    fin = s[~s['is_boundary']]
    da = s['dAIC'].dropna()
    print(f"[lognormal mu prior: centre mu=1, {S_DEX} dex]")
    print(f"fitted: {len(s)}; finite rc: {len(fin)}/{len(s)-len(fin)} "
          f"({100*len(fin)/len(s):.0f}%/{100-100*len(fin)/len(s):.0f}%)  [fiducial: 101/74, 58%/42%]")
    print(f"median finite rc: {fin['rc'].median():.1f} kpc  [fiducial: 15.8]")
    print(f"median chi2/pt: {s['chi2_pt'].median():.2f}  [fiducial: 1.08]")
    print(f"median dAIC (same-config): {da.median():+.1f}  [fiducial: +6.6]")
    print(f"  comparable |dAIC|<=2: {(da.abs()<=2).sum()} ({100*(da.abs()<=2).mean():.0f}%)")
    print(f"  NFW preferred >2: {(da>2).sum()} ({100*(da>2).mean():.0f}%) | "
          f"Yukawa preferred <-2: {(da<-2).sum()}")
    print(f"mu distribution: median {s['mu'].median():.2f}, "
          f"16-84%: {s['mu'].quantile(0.16):.2f}-{s['mu'].quantile(0.84):.2f}, "
          f"mu<0.5: {(s['mu']<0.5).sum()}")
    print(f"saved -> {out_csv}")


if __name__ == "__main__":
    main()
