"""Fiducial (point-source) characteristic-acceleration clustering test.

Same methodology as cluster_test.py, but fed by the fiducial fit table
results/fiducial_rerun.csv instead of the extended-source summary_v2.csv.
For each galaxy with a finite best-fit r_c inside the data coverage
(r_c <= last measured radius; pre-registered, no extrapolation), evaluates
a_c = V_obs(r_c)^2 / r_c and g_bar(r_c).

Reproduces the paper's Fig. 4 (fiducial a_c test):
  33 galaxies, slope of log a_c vs log V_max = 1.09 +- 0.17,
  scatter 0.34 dex, median a_c = 0.22 a0, Spearman rho = 0.72.

Inputs : data/MassModels_Lelli2016c.mrt, results/fiducial_rerun.csv
Outputs: results/fiducial_ac_test.csv, figures/fig4_ac_test.{png,pdf}

Structure note (2026-07-16, Paper 1 governance import): numerical logic is
byte-identical to the yukawa-sparc-fits original; reorganized into importable
functions (load_sparc, compute_ac_table) with a __main__ guard for the
regression suite. Reproduction verified unchanged.
"""
import numpy as np, pandas as pd
from scipy import stats
from _paths import MRT, RESULTS_DIR, FIGURES_DIR, require

KMS2_PER_KPC_TO_SI = 1e6/3.0857e19   # (km/s)^2/kpc -> m/s^2
A0_MOND = 1.2e-10                     # m/s^2  (reference value, NOT fitted)
LOG_A0  = np.log10(A0_MOND)


def load_sparc(path=MRT):
    rows=[]
    for line in open(path, encoding='latin-1', errors='replace'):
        p=line.strip().split()
        if len(p)<8: continue
        try:
            float(p[1]); rows.append((p[0],float(p[2]),float(p[3]),float(p[4]),float(p[5]),float(p[6]),float(p[7])))
        except (ValueError,IndexError): continue
    return pd.DataFrame(rows, columns=['ID','R','Vobs','eV','Vgas','Vdisk','Vbul'])


def compute_ac_table(rc_df, fid):
    """For each finite-r_c galaxy with r_c inside the data coverage, evaluate a_c(r_c)."""
    fin = fid[(~fid['is_boundary']) & fid['rc'].notna()].copy()
    out=[]
    for _,row in fin.iterrows():
        g = rc_df[rc_df['ID']==row['Galaxy']].sort_values('R')
        g = g[g['R']>0]
        if len(g)<3: continue
        r=g['R'].values; Vo=g['Vobs'].values
        Vbar2 = g['Vgas'].values**2 + row['mu']*(g['Vdisk'].values**2+g['Vbul'].values**2)
        rc = row['rc']; Vmax=Vo.max()
        if rc > r[-1]:
            continue   # pre-registered: no extrapolation beyond data
        V_rc  = np.interp(rc, r, Vo)
        Vb2_rc= np.interp(rc, r, Vbar2)
        a_c  = V_rc**2/rc * KMS2_PER_KPC_TO_SI
        gbar = max(Vb2_rc,1e-12)/rc * KMS2_PER_KPC_TO_SI
        out.append(dict(Galaxy=row['Galaxy'], rc=rc, Vmax=Vmax, V_rc=V_rc,
                        a_c=a_c, gbar=gbar, chi2=row['chi2_pt']))
    return pd.DataFrame(out), len(fin)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    require(MRT, "Place MassModels_Lelli2016c.mrt (SPARC) in data/.")
    fid_csv = RESULTS_DIR / "fiducial_rerun.csv"
    require(fid_csv, "Run scripts/fiducial_rerun.py first.")

    rc_df = load_sparc()
    f = pd.read_csv(fid_csv)
    d, n_fin = compute_ac_table(rc_df, f)
    print(f"finite-rc galaxies: {n_fin}; r_c inside data coverage: {len(d)}; "
          f"excluded (rc beyond last point): {n_fin-len(d)}")

    x = np.log10(d['Vmax'].values); y = np.log10(d['a_c'].values)
    sl, ic, rv, pv, se = stats.linregress(x, y)
    rho, pp = stats.spearmanr(x, y)
    scatter = y.std()
    print(f"slope = {sl:.2f} +- {se:.2f}   [paper: 1.09 +- 0.17]")
    print(f"scatter = {scatter:.2f} dex    [paper: 0.34]")
    print(f"median a_c = {10**np.median(y)/A0_MOND:.2f} a0   [paper: 0.22]")
    print(f"Spearman rho = {rho:.2f} (p={pp:.1e})   [paper: 0.72]")

    out_csv = RESULTS_DIR / "fiducial_ac_test.csv"
    d.to_csv(out_csv, index=False)
    print(f"saved per-galaxy table -> {out_csv}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    ax1.scatter(x, y, s=22, alpha=0.8)
    xx = np.linspace(x.min(), x.max(), 50)
    ax1.plot(xx, ic + sl*xx, 'r-', lw=1.5,
             label=f"slope = {sl:.2f} $\\pm$ {se:.2f}")
    ax1.axhline(LOG_A0, color='gray', ls='--', lw=1, label="$a_0$ (MOND)")
    ax1.set_xlabel(r"$\log_{10}\, V_{\rm max}$ [km/s]")
    ax1.set_ylabel(r"$\log_{10}\, a_c(r_c)$ [m/s$^2$]")
    ax1.set_title(f"Fiducial run: $a_c$ tracks $V_{{\\rm max}}$ "
                  f"($\\rho$ = {rho:.2f}, n = {len(d)})")
    ax1.legend(fontsize=9)
    ax2.hist(y, bins=12, alpha=0.85)
    ax2.axvline(LOG_A0, color='gray', ls='--', lw=1, label="$a_0$ (MOND)")
    ax2.set_xlabel(r"$\log_{10}\, a_c(r_c)$ [m/s$^2$]")
    ax2.set_ylabel("N galaxies")
    ax2.set_title(f"scatter = {scatter:.2f} dex (criterion: < 0.3 dex)")
    ax2.legend(fontsize=9)
    fig.tight_layout()
    for ext in ("png","pdf"):
        fig.savefig(FIGURES_DIR / f"fig4_ac_test.{ext}", dpi=160)
    print(f"saved figure -> {FIGURES_DIR}/fig4_ac_test.png/.pdf")


if __name__ == "__main__":
    main()
