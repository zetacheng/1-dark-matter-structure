"""Fiducial re-run of the per-galaxy Yukawa vs NFW fits over the SPARC sample.

Fits each SPARC galaxy rotation curve with a Yukawa kernel (free mass scale m,
so r_c = 1/m) and, as a comparison, an NFW kernel, scanning a small grid of
inner-radius cuts (rmin) and error floors (ef) and selecting by AIC. Reproduces
the fiducial summary numbers quoted in the paper.

dAIC definition (paper): AIC_Yukawa - AIC_NFW with BOTH kernels fitted on the
same data cut and error floor, namely the (rmin, ef) configuration selected by
the Yukawa fit. AIC values are only comparable on identical data with an
identical noise model, so a same-configuration comparison is required; the
per-model-best alternative (each kernel at its own AIC-optimal configuration)
is kept as a diagnostic column dAIC_permodel. Fiducial numbers:
median dAIC = +6.6 (per-model-best: +9.5); |dAIC|<=2: 48 (27%);
dAIC>2 (NFW preferred): 117 (67%).

Input : data/MassModels_Lelli2016c.mrt   (SPARC, Lelli et al. 2016)
Output: results/fiducial_rerun.csv

Structure note (2026-07-16, Paper 1 governance import): the numerical logic is
byte-identical to the yukawa-sparc-fits original; the module was reorganized
into importable functions (load_sparc, wls_v1, run_gal, yuk, nfw, fit_all) with
a __main__ guard so the regression suite can import and exercise the real code.
Reproduction of results/fiducial/raw/fiducial_rerun.csv was verified unchanged.
"""
import numpy as np, pandas as pd
from _paths import MRT, RESULTS_DIR, require

M_MIN, M_MAX, M_STEPS = 0.00125, 0.5, 140
RS_MIN, RS_MAX, RS_STEPS = 0.5, 200.0, 80
RMIN_LIST = [0.0, 2.0, 3.0]
EF_LIST   = [6.0, 4.0, 3.0]


def load_sparc(path=MRT):
    """Parse a SPARC MassModels .mrt into a DataFrame (same parser as the fit code)."""
    rows=[]
    for line in open(path, encoding='latin-1', errors='replace'):
        p=line.strip().split()
        if len(p)<8: continue
        try:
            float(p[1]); rows.append((p[0],float(p[2]),float(p[3]),float(p[4]),float(p[5]),float(p[6]),float(p[7])))
        except (ValueError,IndexError): continue
    return pd.DataFrame(rows, columns=['ID','R','Vobs','eV','Vgas','Vdisk','Vbul'])


def wls_v1(y, S, X, sig):
    w = 1.0/sig**2
    A = np.array([[np.sum(w*S*S), np.sum(w*S*X)],[np.sum(w*S*X), np.sum(w*X*X)]])
    b = np.array([np.sum(w*S*y), np.sum(w*X*y)])
    try: th = np.linalg.solve(A,b)
    except np.linalg.LinAlgError: th = np.array([1.0,1e4])
    return max(th[0],0.0), min(max(th[1],0.0),1e30)


def run_gal(g, rmin, ef, kernel_grid, kfun):
    g = g[(g['R']>0)&(g['R']>=rmin)].sort_values('R')
    if len(g)<3: return None
    r=g['R'].values; Vo=g['Vobs'].values; eV=g['eV'].values
    Vg2=g['Vgas'].values**2; S=g['Vdisk'].values**2+g['Vbul'].values**2
    N=len(r); sig=np.maximum(eV,ef); y=Vo**2-Vg2
    best=None
    for km in kernel_grid:
        X = kfun(r,km)
        xm = np.max(np.abs(X))
        Xn = X/xm if xm>0 else X
        mu,B = wls_v1(y,S,Xn,sig)
        Vm = np.sqrt(np.maximum(Vg2+mu*S+B*Xn,0.0))
        s2=sig**2
        nll = float(np.sum((Vo-Vm)**2/s2+np.log(2*np.pi*s2)))
        c2 = float(np.sum(((Vo-Vm)/sig)**2))
        k = 1+(mu>0)+(B>0)
        aic = nll+2*k
        if best is None or aic<best['AIC']:
            best = dict(m=km,mu=mu,B=B,chi2_pt=c2/N,nll=nll,AIC=aic,N=N)
    return best


yuk = lambda r,m: (1-np.exp(-2*m*r))/np.maximum(r,1e-12)
def nfw(r,rs):
    x=r/rs; return (np.log(1+x)-x/(1+x))/np.maximum(r,1e-12)

m_grid = np.logspace(np.log10(M_MIN),np.log10(M_MAX),M_STEPS)
rs_grid= np.logspace(np.log10(RS_MIN),np.log10(RS_MAX),RS_STEPS)


def fit_all(df):
    """Run the fiducial Yukawa vs NFW selection over every galaxy; returns the summary frame."""
    out=[]
    for gal,g in df.groupby('ID', sort=False):
        besty=None; bestn=None; nfw_by_cfg={}
        for rm in RMIN_LIST:
            for ef in EF_LIST:
                by = run_gal(g,rm,ef,m_grid,yuk)
                if by is not None and (besty is None or by['AIC']<besty['AIC']):
                    besty=by; besty['rmin']=rm; besty['ef']=ef
                bn = run_gal(g,rm,ef,rs_grid,nfw)
                if bn is not None:
                    nfw_by_cfg[(rm,ef)]=bn
                    if bestn is None or bn['AIC']<bestn['AIC']:
                        bestn=bn
        if besty is None: continue
        is_bnd = abs(besty['m']-M_MIN)/M_MIN < 0.01
        bn_same = nfw_by_cfg.get((besty['rmin'],besty['ef']))
        dAIC = besty['AIC']-bn_same['AIC'] if bn_same is not None else np.nan
        out.append(dict(Galaxy=gal, m=besty['m'], rc=(np.nan if is_bnd else 1/besty['m']),
                        mu=besty['mu'], B=besty['B'], chi2_pt=besty['chi2_pt'],
                        is_boundary=is_bnd,
                        dAIC=dAIC,                                  # paper definition (same config)
                        dAIC_permodel=besty['AIC']-bestn['AIC'],    # diagnostic
                        rmin=besty['rmin'], ef=besty['ef'], N=besty['N']))
    return pd.DataFrame(out)


def main():
    require(MRT, "Download MassModels_Lelli2016c.mrt from the SPARC database "
                 "(Lelli et al. 2016) and place it in data/.")
    df = load_sparc()
    s = fit_all(df)
    out_csv = RESULTS_DIR / "fiducial_rerun.csv"
    s.to_csv(out_csv, index=False)
    fin = s[~s['is_boundary']]
    da = s['dAIC'].dropna(); dp = s['dAIC_permodel'].dropna()
    print(f"fitted: {len(s)}; finite rc: {len(fin)} ({100*len(fin)/len(s):.0f}%)  [paper: 101, 58%]")
    print(f"median rc: {fin['rc'].median():.1f} kpc  [paper: 15.8]")
    print(f"median chi2/pt: {s['chi2_pt'].median():.2f}  [paper: 1.08]")
    print(f"median dAIC (same-config, paper def.): {da.median():+.1f}  [paper: +6.6]")
    print(f"  comparable |dAIC|<=2: {(da.abs()<=2).sum()} ({100*(da.abs()<=2).mean():.0f}%)  [paper: 48, 27%]")
    print(f"  NFW preferred dAIC>2: {(da>2).sum()} ({100*(da>2).mean():.0f}%)  [paper: 117, 67%]")
    print(f"median dAIC (per-model best, diagnostic): {dp.median():+.1f}")
    print(f"\nsaved -> {out_csv}")


if __name__ == "__main__":
    main()
