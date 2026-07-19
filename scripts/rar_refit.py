"""Single-a0 acceleration-dependent (RAR-kernel) refit of SPARC.
Model: g_pred = g_bar / (1 - exp(-sqrt(g_bar/a0)))  [McGaugh+ 2016 form]
Global parameter: a0 (single, fitted). Per galaxy: mu with lognormal
0.1-dex prior (MAP on grid). Fixed configuration rmin=0, sigma_f=6 km/s
(no per-galaxy config selection). V-space Gaussian -2lnL.

Structure note (2026-07-16, Paper 1 governance import): numerical logic is
byte-identical to the yukawa-sparc-fits original; reorganized into importable
functions (load_sparc, build_gals, nu, total_nll, fit_a0) with a __main__
guard for the regression suite. total_nll now takes the galaxy list as an
explicit argument instead of a module global; the arithmetic is unchanged.
Reproduction verified unchanged.
"""
import numpy as np, pandas as pd
from _paths import MRT, RESULTS_DIR

KPC_M = 3.0857e19          # m per kpc
KMS2_KPC_TO_SI = 1e6/KPC_M # (km/s)^2/kpc -> m/s^2
EF = 6.0
LOGMU = np.linspace(-0.6,0.6,61); MU=10.0**LOGMU
PRIOR = (LOGMU/0.1)**2


def load_sparc(path=MRT):
    rows=[]
    for line in open(path,encoding='latin-1',errors='replace'):
        p=line.strip().split()
        if len(p)<8: continue
        try:
            float(p[1]); rows.append((p[0],float(p[2]),float(p[3]),float(p[4]),float(p[5]),float(p[6]),float(p[7])))
        except (ValueError,IndexError): continue
    return pd.DataFrame(rows,columns=['ID','R','Vobs','eV','Vgas','Vdisk','Vbul'])


def build_gals(df):
    gals=[]
    for gal,g in df.groupby('ID',sort=False):
        g=g[g['R']>0].sort_values('R')
        if len(g)<3: continue
        gals.append((gal,g['R'].values,g['Vobs'].values,
                     np.maximum(g['eV'].values,EF),
                     g['Vgas'].values**2*np.sign(g['Vgas'].values),  # keep sign convention: Vgas can be neg? SPARC Vgas>=0 typically
                     g['Vdisk'].values**2+g['Vbul'].values**2))
    return gals


def nu(y):   # RAR interpolation
    return 1.0/(1.0-np.exp(-np.sqrt(np.maximum(y,1e-30))))


def total_nll(a0_si, gals):
    tot=0.0; per=[]
    for gal,r,Vo,sig,Vg2,S in gals:
        gbar = (Vg2[None,:]+MU[:,None]*S[None,:])/r[None,:]*KMS2_KPC_TO_SI  # (M,N)
        gbar = np.maximum(gbar,1e-15)
        gpred = gbar*nu(gbar/a0_si)
        Vm = np.sqrt(gpred*r[None,:]/KMS2_KPC_TO_SI)
        nll = np.sum(((Vo[None,:]-Vm)/sig[None,:])**2,axis=1) \
              + np.sum(np.log(2*np.pi*sig**2))
        obj = nll+PRIOR
        im = np.argmin(obj)
        chi2 = np.sum(((Vo-Vm[im])/sig)**2)
        tot += obj[im]
        per.append((gal,MU[im],chi2/len(r),len(r)))
    return tot,per


def fit_a0(gals):
    """Scan the global a0 grid; return (a0_best, lo, hi, per_galaxy_frame)."""
    a0_grid = np.logspace(np.log10(0.3e-10),np.log10(4e-10),49)
    tots=[]
    for a0 in a0_grid:
        t,_=total_nll(a0, gals); tots.append(t)
    tots=np.array(tots)
    ib=int(np.argmin(tots))
    a0=a0_grid[ib]
    # 1-sigma from delta(total -2lnL)=1
    lo=hi=a0
    for k in range(ib,-1,-1):
        if tots[k]-tots[ib]>1: lo=a0_grid[k]; break
    for k in range(ib,len(a0_grid)):
        if tots[k]-tots[ib]>1: hi=a0_grid[k]; break
    t,per=total_nll(a0, gals)
    per=pd.DataFrame(per,columns=['Galaxy','mu','chi2_pt','N'])
    return a0, lo, hi, per


def main():
    df=load_sparc()
    gals=build_gals(df)
    a0, lo, hi, per = fit_a0(gals)
    per.to_csv(RESULTS_DIR/'rar_refit.csv',index=False)
    print(f"best a0 = {a0:.3e} m/s^2  (grid-adjacent 1sig: [{lo:.2e},{hi:.2e}])")
    print(f"  [empirical RAR a0 = 1.2e-10; Lambda_DE^2/M_Pl ~ 2e-10]")
    print(f"median chi2/pt = {per['chi2_pt'].median():.2f}")
    print(f"chi2/pt<1: {(per['chi2_pt']<1).sum()} ({100*(per['chi2_pt']<1).mean():.0f}%) | <2: {(per['chi2_pt']<2).sum()} ({100*(per['chi2_pt']<2).mean():.0f}%)")
    print(f"mu: median {per['mu'].median():.2f}, 16-84%: {per['mu'].quantile(0.16):.2f}-{per['mu'].quantile(0.84):.2f}")
    print(f"n galaxies {len(per)}, total data points {per['N'].sum()}")
    # parameter count: 1 global + 175 prior-constrained mu  vs NFW: 175 mu + 350


if __name__ == "__main__":
    main()
