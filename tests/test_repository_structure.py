"""Regression checks for the required research repository foundation.

Includes the CLAIMS.md ``Gate`` column vs GATES.md ``## <ID>`` heading
cross-check: this exact defect (a claim citing a gate that has no registry
entry) occurred in the Paper 3 repository and must be caught structurally.
"""

import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "PROGRESS.md",
    "GATES.md",
    "DECISION_LOG.md",
    "ROADMAP.md",
    "CLAIMS.md",
    "HANDOFF.md",
    "AGENTS.md",
    "CONVENTIONS.md",
    "MIGRATION.md",
    "CITATION.cff",
    "LICENSE",
    ".gitignore",
    "pyproject.toml",
    "Makefile",
    "paper/README.md",
    "paper/yukawa_sparc_paper_v163.tex",
    "paper/figures/.gitkeep",
    "derivations/README.md",
    "scripts/README.md",
    "scripts/_paths.py",
    "scripts/fiducial_rerun.py",
    "scripts/fiducial_ac_test.py",
    "scripts/cluster_test.py",
    "scripts/ml_prior_lognormal.py",
    "scripts/ml_prior_mufixed.py",
    "scripts/rar_refit.py",
    "scripts/nuisance_comparison.py",
    "scripts/plot_ac_test.py",
    "tests/README.md",
    "tests/test_repository_structure.py",
    "data/README.md",
    "data/MassModels_Lelli2016c.mrt",
    "data/SPARC_Lelli2016c.mrt",
    "data/summary_v2.csv",
    "results/README.md",
    "results/raw/.gitkeep",
    "results/processed/.gitkeep",
    "results/figures/.gitkeep",
    "reviews/README.md",
    "reviews/chatgpt/.gitkeep",
    "reviews/claude/.gitkeep",
    "archive/README.md",
    "docs/RESEARCH_WORKFLOW.md",
    "docs/RESULT_SCHEMA.md",
    "docs/BRANCHING_POLICY.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/gate.yml",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/paper-sync.yml",
    ".github/workflows/ci.yml",
)

REQUIRED_DIRECTORIES = (
    "paper",
    "paper/figures",
    "derivations",
    "scripts",
    "tests",
    "data",
    "results",
    "results/raw",
    "results/processed",
    "results/figures",
    "reviews",
    "reviews/chatgpt",
    "reviews/claude",
    "archive",
    "docs",
    ".github",
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
)

# Every gate directory holds the required provenance metadata.
GATE_RESULT_DIRS = (
    "fiducial",
    "ac-test",
    "ml-prior",
    "refit",
    "nuisance",
    "intrinsic-scatter",
)


def test_required_files_exist() -> None:
    """Every required file is present as a regular file."""
    missing = [path for path in REQUIRED_FILES if not (REPOSITORY_ROOT / path).is_file()]
    assert not missing, f"Missing required files: {missing}"


def test_required_directories_exist() -> None:
    """Every required directory is present."""
    missing = [
        path for path in REQUIRED_DIRECTORIES if not (REPOSITORY_ROOT / path).is_dir()
    ]
    assert not missing, f"Missing required directories: {missing}"


def test_gate_result_dirs_have_provenance() -> None:
    """Each gate results directory has PROVENANCE.md, environment.txt, README.md, raw/."""
    problems = []
    for g in GATE_RESULT_DIRS:
        base = REPOSITORY_ROOT / "results" / g
        for req in ("PROVENANCE.md", "environment.txt", "README.md"):
            if not (base / req).is_file():
                problems.append(f"results/{g}/{req}")
        if not (base / "raw").is_dir():
            problems.append(f"results/{g}/raw/")
    assert not problems, f"Missing gate provenance artifacts: {problems}"


def test_environment_files_are_not_placeholders() -> None:
    """environment.txt must record a real environment, not a bare placeholder.

    Paper 5 learned this the hard way: 'Migrated historical artifact' hid a real
    cross-platform float gap. Require concrete Python/NumPy/SciPy version strings.
    """
    for g in GATE_RESULT_DIRS:
        text = (REPOSITORY_ROOT / "results" / g / "environment.txt").read_text()
        assert re.search(r"Python\s*:\s*3\.\d+", text), f"{g}: no Python version recorded"
        assert re.search(r"NumPy\s*:\s*\d+\.\d+", text), f"{g}: no NumPy version recorded"
        assert re.search(r"SciPy\s*:\s*\d+\.\d+", text), f"{g}: no SciPy version recorded"
        assert "Migrated historical artifact" not in text


def _claims_gate_ids() -> set:
    """Gate IDs cited in the CLAIMS.md 'Gate' column (5th markdown cell)."""
    ids = set()
    for line in (REPOSITORY_ROOT / "CLAIMS.md").read_text().splitlines():
        line = line.strip()
        if not line.startswith("| P1-CL-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        gate_cell = cells[4]  # Claim ID | Claim | Status | Evidence | Gate | ...
        for gid in re.findall(r"P1-[A-Z0-9]+-\d+", gate_cell):
            ids.add(gid)
    return ids


def _gates_heading_ids() -> set:
    """Gate IDs that have a '## <ID>' heading in GATES.md."""
    ids = set()
    for line in (REPOSITORY_ROOT / "GATES.md").read_text().splitlines():
        m = re.match(r"##\s+(P1-[A-Z0-9]+-\d+)\b", line.strip())
        if m:
            ids.add(m.group(1))
    return ids


def test_every_claims_gate_has_a_gates_heading() -> None:
    """Every gate ID cited in CLAIMS.md has a matching '## <ID>' heading in GATES.md.

    (The Paper 3 defect: a claim referenced a gate with no registry entry.)
    """
    cited = _claims_gate_ids()
    registered = _gates_heading_ids()
    assert cited, "no gate IDs parsed from CLAIMS.md — parser or ledger changed"
    missing = sorted(cited - registered)
    assert not missing, (
        f"CLAIMS.md cites gate IDs with no '## <ID>' heading in GATES.md: {missing}"
    )
