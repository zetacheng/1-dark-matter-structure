"""Shared path resolution for the Yukawa/SPARC fit scripts.

Resolves locations relative to the repository root so the scripts run from
anywhere. Every location can be overridden with an environment variable, which
is handy on clusters or when the raw SPARC data lives outside the repo.

Env overrides:
    SPARC_MRT     -> path to MassModels_Lelli2016c.mrt   (default: data/)
    SUMMARY_CSV   -> path to summary_v2.csv              (default: data/)
    SPARC_T1      -> path to SPARC_Lelli2016c.mrt (Table 1)  (default: data/)
    RESULTS_DIR   -> directory for CSV outputs           (default: results/)
    FIGURES_DIR   -> directory for figure outputs        (default: figures/)
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = Path(os.environ.get("DATA_DIR", ROOT / "data"))
RESULTS_DIR = Path(os.environ.get("RESULTS_DIR", ROOT / "results"))
FIGURES_DIR = Path(os.environ.get("FIGURES_DIR", ROOT / "figures"))

MRT = Path(os.environ.get("SPARC_MRT", DATA_DIR / "MassModels_Lelli2016c.mrt"))
SUMMARY = Path(os.environ.get("SUMMARY_CSV", DATA_DIR / "summary_v2.csv"))
T1 = Path(os.environ.get("SPARC_T1", DATA_DIR / "SPARC_Lelli2016c.mrt"))

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def require(path, hint):
    if not Path(path).exists():
        raise SystemExit(
            f"ERROR: required input not found: {path}\n"
            f"       {hint}"
        )
    return path
