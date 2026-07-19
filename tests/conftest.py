"""Shared test setup.

Puts ``scripts/`` on the import path and redirects the scripts' output
directories to a temporary location BEFORE any script module is imported, so
importing the (import-refactored) analysis modules neither runs a full fit nor
writes into the committed repository tree.
"""

import os
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
DATA = REPO_ROOT / "data"

# Redirect script outputs to a temp dir (scripts/_paths.py reads these at import).
_TMP = Path(tempfile.gettempdir()) / "p1_governance_test_out"
os.environ.setdefault("RESULTS_DIR", str(_TMP / "results"))
os.environ.setdefault("FIGURES_DIR", str(_TMP / "figures"))

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def raw(rel: str) -> Path:
    """Path to a committed immutable raw artifact, e.g. raw('fiducial/raw/fiducial_rerun.csv')."""
    return REPO_ROOT / "results" / rel


def data_available() -> bool:
    return (DATA / "MassModels_Lelli2016c.mrt").exists()
