.PHONY: check test test-slow test-all lint structure

check: lint test

# Default suite: fast regression + structure (excludes the slow full-sample fits)
test:
	python -m pytest -m "not slow"

# Slow suite: the full 175-galaxy regression anchors
test-slow:
	python -m pytest -m slow

# Everything
test-all:
	python -m pytest

lint:
	python -m ruff check .

structure:
	python -m pytest tests/test_repository_structure.py
