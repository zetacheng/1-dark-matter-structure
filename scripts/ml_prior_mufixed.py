"""M/L robustness variant: mu fixed at unity (the fiducial Upsilon*).
Machinery otherwise identical to fiducial_rerun.py (B-only 1D WLS in V^2
space; 9-config AIC selection; same-config dAIC vs NFW under the same
constraint). Reproduces (paper Sec. "Stellar mass-to-light prior"):
finite/boundary 4/171 (2%/98%); median chi2/pt 1.48; median dAIC +6.6;
Yukawa-preferred count 0. Output: results/mufixed_rerun.csv

Structure note (2026-07-16, Paper 1 governance import): numerical logic is
byte-identical to the yukawa-sparc-fits original; reorganized into importable
functions (load_sparc, run_gal, fit_all) with a __main__ guard for the
regression suite. Reproduction verified unchanged.
"""
import numpy as np, pandas as pd
from _paths import MRT, RESULTS_DIR, require

M_MIN,M_MAX,M_STEPS=0.00125,0.5,140
RS_MIN,RS_MAX,RS_STEPS=0.5,200.0,80
RMIN_LIST=[0.0,2.0,3.0]; EF_LIST=[6.0,4.0,3.0]


def load_sparc(path=MRT):
    rows=[]
    for line in open(path,encoding='latin-1',errors='replace'):
        p=line.strip().split()
        if len(p)<8: continue
        try:
            float(p[1]); rows.append((p[0],float(p[2]),float(p[3]),float(p[4]),float(p[5]),float(p[6]),float(p[7])))
        except (ValueError,IndexError): continue
    return pd.DataFrame(rows,columns=['ID','R','Vobs','eV','Vgas','Vdisk','Vbul'])


def run_gal(g,rmin,ef,grid,kfun):
    g=g[(g['R']>0)&(g['R']>=rmin)].sort_values('R')
    if len(g)<3: return None
    r=g['R'].values;Vo=g['Vobs'].values;eV=g['eV'].values
    Vg2=g['Vgas'].values**2;S=g['Vdisk'].values**2+g['Vbul'].values**2
    N=len(r);sig=np.maximum(eV,ef);w=1.0/sig**2
    y=Vo**2-Vg2-S
    best=None
    for km in grid:
        X=kfun(r,km);xm=np.max(np.abs(X));Xn=X/xm if xm>0 else X
        B=max(float(np.sum(w*Xn*y)/max(np.sum(w*Xn*Xn),1e-300)),0.0)
        Vm=np.sqrt(np.maximum(Vg2+S+B*Xn,0.0))
        s2=sig**2
        nll=float(np.sum((Vo-Vm)**2/s2+np.log(2*np.pi*s2)))
        c2=float(np.sum(((Vo-Vm)/sig)**2))
        aic=nll+2*(1+(B>0))
        if best is None or aic<best['AIC']:
            best=dict(m=km,B=B,chi2_pt=c2/N,AIC=aic,N=N)
    return best


yuk=lambda r,m:(1-np.exp(-2*m*r))/np.maximum(r,1e-12)
def nfw(r,rs):
    x=r/rs;return (np.log(1+x)-x/(1+x))/np.maximum(r,1e-12)
m_grid=np.logspace(np.log10(M_MIN),np.log10(M_MAX),M_STEPS)
rs_grid=np.logspace(np.log10(RS_MIN),np.log10(RS_MAX),RS_STEPS)


def fit_all(df):
    out=[]
    for gal,g in df.groupby('ID',sort=False):
        besty=None; nfw_by_cfg={}
        for rm in RMIN_LIST:
            for ef in EF_LIST:
                by=run_gal(g,rm,ef,m_grid,yuk)
                if by is not None and (besty is None or by['AIC']<besty['AIC']):
                    besty=by; besty['rmin']=rm; besty['ef']=ef
                bn=run_gal(g,rm,ef,rs_grid,nfw)
                if bn is not None: nfw_by_cfg[(rm,ef)]=bn
        if besty is None: continue
        is_bnd=abs(besty['m']-M_MIN)/M_MIN<0.01
        bs=nfw_by_cfg.get((besty['rmin'],besty['ef']))
        out.append(dict(Galaxy=gal,m=besty['m'],rc=(np.nan if is_bnd else 1/besty['m']),
                        B=besty['B'],chi2_pt=besty['chi2_pt'],is_boundary=is_bnd,
                        dAIC=besty['AIC']-bs['AIC'] if bs else np.nan,
                        rmin=besty['rmin'],ef=besty['ef'],N=besty['N']))
    return pd.DataFrame(out)


def main():
    require(MRT,"Place MassModels_Lelli2016c.mrt (SPARC) in data/.")
    df=load_sparc()
    s=fit_all(df)
    s.to_csv(RESULTS_DIR/'mufixed_rerun.csv',index=False)
    fin=s[~s['is_boundary']]; da=s['dAIC'].dropna()
    print(f"finite/boundary: {len(fin)}/{len(s)-len(fin)} ({100*len(fin)/len(s):.0f}%/{100-100*len(fin)/len(s):.0f}%)  [paper: 4/171, 2%/98%]")
    print(f"median chi2/pt: {s['chi2_pt'].median():.2f}  [paper: 1.48]")
    print(f"median dAIC: {da.median():+.1f}  [paper: +6.6] | Yukawa preferred (<-2): {(da<-2).sum()}  [paper: 0]")


if __name__ == "__main__":
    main()
