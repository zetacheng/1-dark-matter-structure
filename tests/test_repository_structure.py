"""Regression checks for the required research repository foundation."""

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
    "CITATION.cff",
    "LICENSE",
    ".gitignore",
    "pyproject.toml",
    "Makefile",
    "paper/README.md",
    "paper/figures/.gitkeep",
    "derivations/README.md",
    "scripts/README.md",
    "tests/README.md",
    "tests/test_repository_structure.py",
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
