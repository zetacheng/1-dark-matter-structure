"""Nuisance-marginalized three-model comparison on SPARC.
Per galaxy: mu (lognormal 0.1 dex), distance factor d (Gaussian, e_D/D),
inclination i (Gaussian, e_Inc), all MAP on grids. Models: RAR single-a0
(global a0 fitted), Yukawa (m,B per galaxy), NFW (rs,B per galaxy).
Fixed configuration rmin=0, error floor EF (scan). Scalings under d:
r->d r, Vbar^2 -> d Vbar^2 (flux-based masses), V_obs unchanged;
under i: V_obs -> V_obs sin(i0)/sin(i), eV likewise.
Outputs summary stats for all-sample and the standard cut (Q<3, i0>=30).

At floor 6: a0 ~ 1.046e-10 m/s^2, AIC RAR 26688 / Yukawa 36347 / NFW 24596.
At floor 3: a0 ~ 1.279e-10 m/s^2, AIC RAR 29238 / Yukawa 49102 / NFW 24984.

NOTE (Paper 1 governance import, 2026-07-16): this is the ERROR-FLOOR
three-model comparison. The paper's headline in-sample dAIC values
(RAR 0 / Yukawa +4859 / NFW -1614) and the fitted intrinsic-scatter
fractions f_int come from the INTRINSIC-SCATTER likelihood variant
(paper Sec. refit; script `intrinsic_scatter_comparison.py`), which is NOT
present in the imported yukawa-sparc-fits record. See
results/intrinsic-scatter/PROVENANCE.md and GATES.md P1-ISCATTER-01.

Structure note: numerical logic is byte-identical to the original;
reorganized into importable functions (load_table1, load_massmodels,
build_gals, rar_gal, kern_gal, scan_a0, run) with a __main__ guard. EF is a
module global (default 6.0) set from argv in main(). Reproduction verified.
"""
import sys
import numpy as np, pandas as pd
from _paths import MRT, T1, RESULTS_DIR, require

KPC_M = 3.0857e19
KM = 1e6/KPC_M
EF = 6.0   # error floor (km/s); main() overrides from argv

LOGMU = np.linspace(-0.4, 0.4, 41); MUG = 10.0**LOGMU
PMU = (LOGMU/0.1)**2
ND, NI = 9, 9   # grid points for d and i (+-3 sigma)


def load_table1(path=T1):
    t1 = {}
    for line in open(path, encoding='latin-1', errors='replace'):
        p = line.split()
        if len(p) < 18:
            continue
        try:
            D = float(p[2]); eD = float(p[3])
            inc = float(p[5]); einc = float(p[6])
            Q = int(p[17])
            t1[p[0]] = dict(D=D, eD=eD, inc=inc, einc=einc, Q=Q)
        except (ValueError, IndexError):
            continue
    return t1


def load_massmodels(path=MRT):
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


def build_gals(df, t1):
    gals = []
    for gal, g in df.groupby('ID', sort=False):
        if gal not in t1:
            continue
        g = g[g['R'] > 0].sort_values('R')
        if len(g) < 3:
            continue
        m = t1[gal]
        sd = max(m['eD']/m['D'], 0.01)
        dgrid = np.linspace(max(0.2, 1-3*sd), 1+3*sd, ND)
        si = max(m['einc'], 0.5)
        igrid = np.clip(np.linspace(m['inc']-3*si, m['inc']+3*si, NI), 10.0, 90.0)
        sfac = np.sin(np.radians(m['inc']))/np.sin(np.radians(igrid))   # (NI,)
        gals.append(dict(gal=gal, r=g['R'].values, Vo=g['Vobs'].values,
                         eV=g['eV'].values, Vg2=g['Vgas'].values**2,
                         S=g['Vdisk'].values**2 + g['Vbul'].values**2,
                         dgrid=dgrid, pd_=(  (dgrid-1)/sd )**2,
                         igrid=igrid, pi_=((igrid-m['inc'])/si)**2,
                         sfac=sfac, Q=m['Q'], inc0=m['inc']))
    return gals


def nu(y): return 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-30))))
yuk = lambda r, m: (1 - np.exp(-2*m*r))/np.maximum(r, 1e-12)
def nfw(r, rs):
    x = r/rs
    return (np.log(1 + x) - x/(1 + x))/np.maximum(r, 1e-12)
m_grid  = np.logspace(np.log10(0.00125), np.log10(0.5), 140)
rs_grid = np.logspace(np.log10(0.5), np.log10(200.0), 80)


def rar_gal(G, a0):
    """min over (mu,d,i) of data nll + priors; returns (nll_data, chi2pt)."""
    r, Vo, eV = G['r'], G['Vo'], G['eV']
    # obs side: (NI, N)
    Vo_i = Vo[None,:]*G['sfac'][:,None]
    sig_i = np.maximum(eV[None,:]*G['sfac'][:,None], EF)
    # bar side: g_bar independent of d (Vbar^2 and R scale together)
    gbar = (G['Vg2'][None,:] + MUG[:,None]*G['S'][None,:])/r[None,:]*KM  # (M,N)
    gbar = np.maximum(gbar, 1e-15)
    gpred = gbar*nu(gbar/a0)                                            # (M,N)
    # Vpred^2 = gpred * d*r  -> (M,D,N)
    Vp = np.sqrt(gpred[:,None,:]*G['dgrid'][None,:,None]*r[None,None,:]/KM)
    res = (Vo_i[None,None,:,:] - Vp[:,:,None,:])/sig_i[None,None,:,:]   # (M,D,I,N)
    nll = np.sum(res**2, axis=3) + np.sum(np.log(2*np.pi*sig_i**2), axis=1)[None,None,:]
    obj = nll + PMU[:,None,None] + G['pd_'][None,:,None] + G['pi_'][None,None,:]
    k = np.unravel_index(np.argmin(obj), obj.shape)
    chi2 = np.sum(((Vo_i[k[2]] - Vp[k[0],k[1]])/sig_i[k[2]])**2)
    return nll[k], chi2/len(r)


def kern_gal(G, grid, kfun):
    r, Vo, eV = G['r'], G['Vo'], G['eV']
    Vo_i = Vo[None,:]*G['sfac'][:,None]                    # (I,N)
    sig_i = np.maximum(eV[None,:]*G['sfac'][:,None], EF)   # (I,N)
    w_i = 1.0/sig_i**2
    X = np.array([kfun(r, km) for km in grid])
    xm = np.max(np.abs(X), axis=1, keepdims=True)
    Xn = np.where(xm > 0, X/np.maximum(xm, 1e-300), X)     # (K,N)
    # y[d,i,n] = (Vo_i)^2 - d*Vg2   (V^2-space target)
    y = Vo_i[None,:,:]**2 - G['dgrid'][:,None,None]*G['Vg2'][None,None,:]  # (D,I,N)
    S_d = G['dgrid'][:,None]*G['S'][None,:]                                # (D,N)
    # WLS pieces: c_xy[k,d,i], c_xs[k,d,i], c_xx[k,i]
    c_xy = np.einsum('kn,din->kdi', Xn, w_i[None,:,:]*y)
    c_xs = np.einsum('kn,in,dn->kdi', Xn, w_i, S_d)
    c_xx = np.einsum('kn,in,kn->ki', Xn, w_i, Xn)
    best = None
    for mi, mu in enumerate(MUG):
        B = np.clip((c_xy - mu*c_xs)/np.maximum(c_xx, 1e-300)[:,None,:], 0, 1e30)  # (K,D,I)
        Vm2 = (G['dgrid'][None,:,None,None]*(G['Vg2'][None,None,None,:] +
               mu*G['S'][None,None,None,:]) + B[:,:,:,None]*Xn[:,None,None,:])
        Vm = np.sqrt(np.maximum(Vm2, 0))                                   # (K,D,I,N)
        res = (Vo_i[None,None,:,:] - Vm)/sig_i[None,None,:,:]
        nll = np.sum(res**2, axis=3) + np.sum(np.log(2*np.pi*sig_i**2), axis=1)[None,None,:]
        obj = nll + PMU[mi] + G['pd_'][None,:,None] + G['pi_'][None,None,:]
        k = np.unravel_index(np.argmin(obj), obj.shape)
        if best is None or obj[k] < best[0]:
            chi2 = np.sum(((Vo_i[k[2]] - Vm[k])/sig_i[k[2]])**2)
            best = (obj[k], nll[k], chi2/len(G['r']), B[k] > 0)
    return best[1], best[2], best[3]


def scan_a0(gals):
    a0_grid = np.logspace(np.log10(0.5e-10), np.log10(2.5e-10), 25)
    tots = []
    for a0 in a0_grid:
        tots.append(sum(rar_gal(G, a0)[0] for G in gals))
    ib = int(np.argmin(tots)); a0 = a0_grid[ib]
    lo = a0_grid[max(k for k in range(ib+1) if tots[k]-tots[ib] > 1)] if any(tots[k]-tots[ib] > 1 for k in range(ib+1)) else a0_grid[0]
    hi = a0_grid[min(k for k in range(ib, len(a0_grid)) if tots[k]-tots[ib] > 1)] if any(tots[k]-tots[ib] > 1 for k in range(ib, len(a0_grid))) else a0_grid[-1]
    return a0, lo, hi


def run(gals):
    """Full three-model comparison at the current EF; returns (res_frame, a0, lo, hi)."""
    a0, lo, hi = scan_a0(gals)
    rows = []
    for G in gals:
        nR, cR = rar_gal(G, a0)
        nY, cY, bY = kern_gal(G, m_grid, yuk)
        nN, cN, bN = kern_gal(G, rs_grid, nfw)
        rows.append(dict(Galaxy=G['gal'], Q=G['Q'], inc0=G['inc0'],
                         nll_R=nR, chi_R=cR, nll_Y=nY, chi_Y=cY, bY=bY,
                         nll_N=nN, chi_N=cN, bN=bN, N=len(G['r'])))
    return pd.DataFrame(rows), a0, lo, hi


def model_aics(d):
    """Return (aR, aY, aN) total AICs for the sample frame d at the current EF."""
    n = len(d)
    aR = d['nll_R'].sum() + 2*(3*n + 1)
    aY = d['nll_Y'].sum() + 2*(3*n + n + d['bY'].sum())
    aN = d['nll_N'].sum() + 2*(3*n + n + d['bN'].sum())
    return aR, aY, aN


def main():
    global EF
    require(T1, "Download SPARC_Lelli2016c.mrt (Table 1) from "
                "https://astroweb.case.edu/SPARC/ and place it in data/.")
    EF = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0

    t1 = load_table1()
    print(f"Table 1 parsed: {len(t1)} galaxies")
    df = load_massmodels()
    gals = build_gals(df, t1)
    print(f"galaxies matched: {len(gals)}")

    res, a0, lo, hi = run(gals)
    res.to_csv(str(RESULTS_DIR)+'/nuisance_comparison.csv', index=False)

    def report(d, label):
        n = len(d)
        aR, aY, aN = model_aics(d)
        print(f"\n[{label}] n={n}, EF={EF}")
        print(f"  a0 = {a0:.3e} m/s^2  (1sig ~ [{lo:.2e}, {hi:.2e}])")
        print(f"  {'model':<16}{'AIC':>10}{'med chi2/pt':>13}")
        for nm, a, c in [('RAR single-a0', aR, d['chi_R'].median()),
                         ('Yukawa', aY, d['chi_Y'].median()),
                         ('NFW', aN, d['chi_N'].median())]:
            print(f"  {nm:<16}{a:10.0f}{c:13.2f}   dAIC_vs_RAR={a-aR:+.0f}")
        print(f"  per-galaxy median dnll: Y-R {np.median(d['nll_Y']-d['nll_R']):+.1f} | N-R {np.median(d['nll_N']-d['nll_R']):+.1f}")

    report(res, "all galaxies")
    report(res[(res['Q'] < 3) & (res['inc0'] >= 30)], "standard cut (Q<3, i>=30)")


if __name__ == "__main__":
    main()
