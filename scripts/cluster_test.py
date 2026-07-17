"""Clustering test: does the characteristic acceleration a_c(r_c) cluster near a
single scale (the MOND-like a0), or does it track V_max?

For each galaxy with a finite best-fit core radius r_c that lies inside the data
coverage, evaluate a_c = V_obs(r_c)^2 / r_c and the baryonic g_bar(r_c), then
measure their spread and residual correlation with V_max.

Inputs : data/MassModels_Lelli2016c.mrt   (SPARC rotation curves)
         data/summary_v2.csv              (per-galaxy fit summary)
Output : results/clustering_test_results.csv

Structure note (2026-07-16, Paper 1 governance import): numerical logic is
byte-identical to the yukawa-sparc-fits original; reorganized into importable
functions (load_sparc, compute_ac_table) with a __main__ guard for the
regression suite. Reproduction verified unchanged.
"""
import numpy as np, pandas as pd
from _paths import MRT, SUMMARY, RESULTS_DIR, require

KMS2_PER_KPC_TO_SI = 1e6/3.0857e19   # (km/s)^2/kpc -> m/s^2
A0_MOND = 1.2e-10                     # m/s^2  (reference value, NOT fitted)


def load_sparc(path=MRT):
    rows=[]
    for line in open(path, encoding='latin-1', errors='replace'):
        p=line.strip().split()
        if len(p)<8: continue
        try:
            float(p[1]); rows.append((p[0],float(p[2]),float(p[3]),float(p[4]),float(p[5]),float(p[6]),float(p[7])))
        except (ValueError,IndexError): continue
    return pd.DataFrame(rows, columns=['ID','R','Vobs','eV','Vgas','Vdisk','Vbul'])


def compute_ac_table(rc_df, summ):
    """Extended-source a_c table: finite-r_c galaxies with r_c inside data coverage."""
    fin = summ[(~summ['is_boundary']) & summ['best_rc'].notna()].copy()
    out=[]
    for _,row in fin.iterrows():
        g = rc_df[rc_df['ID']==row['Galaxy']].sort_values('R')
        g = g[g['R']>0]
        if len(g)<3: continue
        r=g['R'].values; Vo=g['Vobs'].values
        Vbar2 = g['Vgas'].values**2 + row['best_mu']*(g['Vdisk'].values**2+g['Vbul'].values**2)
        rc = row['best_rc']; Vmax=Vo.max()
        inside = rc <= r[-1]
        if inside:
            V_rc  = np.interp(rc, r, Vo)
            Vb2_rc= np.interp(rc, r, Vbar2)
        else:
            continue   # pre-registered: no extrapolation beyond data
        a_c  = V_rc**2/rc * KMS2_PER_KPC_TO_SI
        gbar = max(Vb2_rc,1e-12)/rc * KMS2_PER_KPC_TO_SI
        out.append(dict(Galaxy=row['Galaxy'], rc=rc, Vmax=Vmax, V_rc=V_rc,
                        a_c=a_c, gbar=gbar, chi2=row['best_chi2_pt']))
    return pd.DataFrame(out), len(fin)


def main():
    from scipy import stats
    require(MRT, "Place MassModels_Lelli2016c.mrt (SPARC) in data/.")
    require(SUMMARY, "Place summary_v2.csv (fit summary) in data/.")

    rc_df = load_sparc()
    summ = pd.read_csv(SUMMARY)
    d, n_fin = compute_ac_table(rc_df, summ)
    print(f"finite-rc galaxies: {n_fin}; r_c inside data coverage: {len(d)}; excluded (rc beyond last point): {n_fin-len(d)}")

    for col,lab in [('a_c','a_c = V_obs(r_c)^2/r_c'), ('gbar','g_bar(r_c)')]:
        lg = np.log10(d[col])
        print(f"\n{lab}:")
        print(f"  median = {10**lg.median():.3e} m/s^2   (a0_MOND = 1.2e-10; ratio = {10**lg.median()/A0_MOND:.2f})")
        print(f"  scatter: std = {lg.std():.3f} dex, 16-84 half-width = {(lg.quantile(0.84)-lg.quantile(0.16))/2:.3f} dex")
        print(f"  full range: {lg.min():.2f} .. {lg.max():.2f}  (span {lg.max()-lg.min():.2f} dex)")

    # residual correlation with Vmax
    for col in ['a_c','gbar']:
        rho,p = stats.spearmanr(np.log10(d['Vmax']), np.log10(d[col]))
        sl,ic,rv,pv,se = stats.linregress(np.log10(d['Vmax']), np.log10(d[col]))
        print(f"\nlog {col} vs log Vmax: Spearman rho={rho:.3f} (p={p:.2e}); slope={sl:.2f}+-{se:.2f}")

    # r_c - Vmax scaling recheck on this subsample
    sl,ic,rv,pv,se = stats.linregress(np.log10(d['Vmax']), np.log10(d['rc']))
    rho,p = stats.spearmanr(np.log10(d['Vmax']), np.log10(d['rc']))
    print(f"\nr_c vs Vmax (this subsample): slope={sl:.2f}+-{se:.2f}, Spearman rho={rho:.3f} (p={p:.2e})  [MOND transition radius expects 2.0]")

    out_csv = RESULTS_DIR / "clustering_test_results.csv"
    d.to_csv(out_csv, index=False)
    print(f"\nsaved per-galaxy table -> {out_csv}")


if __name__ == "__main__":
    main()
