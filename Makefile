.PHONY: check test lint structure

check: lint test

test:
	python -m pytest

lint:
	python -m ruff check .

structure:
	python -m pytest tests/test_repository_structure.py
