"""Plot the clustering-test figure from results/clustering_test_results.csv.

Left panel : log10 a_c(r_c) vs log10 V_max, with a WLS-free OLS slope and the
             MOND acceleration a0 marked as a reference line.
Right panel: histogram of log10 a_c(r_c) with a0 marked; the title reports the
             measured scatter against the (pre-registered) <0.3 dex criterion.

Reproduces figures/clustering_test_fig.{png,pdf}.

Structure note (2026-07-16, Paper 1 governance import): wrapped in a __main__
guard so the module is import-safe; plotting logic unchanged.
"""
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from _paths import RESULTS_DIR, FIGURES_DIR, require

A0_MOND = 1.2e-10                 # m/s^2
LOG_A0  = np.log10(A0_MOND)
SCATTER_CRITERION = 0.3          # dex


def main():
    csv = RESULTS_DIR / "clustering_test_results.csv"
    require(csv, "Run scripts/cluster_test.py first to generate the results table.")

    d = pd.read_csv(csv)
    x = np.log10(d['Vmax'].values)
    y = np.log10(d['a_c'].values)
    sl, ic, rv, pv, se = stats.linregress(x, y)
    scatter = y.std()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # --- left: a_c vs Vmax ---
    ax1.scatter(x, y, s=22, color='#1f77b4', alpha=0.85)
    xx = np.linspace(x.min(), x.max(), 100)
    ax1.plot(xx, sl*xx + ic, color='red', lw=1.8, label=f'slope {sl:.2f}')
    ax1.axhline(LOG_A0, color='gray', ls='--', lw=1.3, label=r'$a_0^{\mathrm{MOND}}$')
    ax1.set_xlabel(r'$\log_{10} V_{\max}$ [km/s]')
    ax1.set_ylabel(r'$\log_{10} a_c(r_c)$ [m/s$^2$]')
    ax1.set_title(r'Characteristic acceleration at $r_c$ vs $V_{max}$')
    ax1.legend(loc='upper left')

    # --- right: histogram of log a_c ---
    ax2.hist(y, bins=20, color='#1f77b4')
    ax2.axvline(LOG_A0, color='gray', ls='--', lw=1.3)
    ax2.set_xlabel(r'$\log_{10} a_c(r_c)$ [m/s$^2$]')
    ax2.set_ylabel('N')
    ax2.set_title(f'scatter = {scatter:.2f} dex (criterion: <{SCATTER_CRITERION})')

    fig.tight_layout()
    for ext in ('png', 'pdf'):
        outp = FIGURES_DIR / f"clustering_test_fig.{ext}"
        fig.savefig(outp, dpi=150, bbox_inches='tight')
        print(f"saved -> {outp}")
    print(f"\nN={len(d)}  slope={sl:.2f}+-{se:.2f}  scatter={scatter:.2f} dex")


if __name__ == "__main__":
    main()
