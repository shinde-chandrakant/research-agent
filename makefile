.PHONY: help clean lint test docs install dev

help:
	@echo "Available commands:"
	@echo "  make install    Install the package and dependencies"
	@echo "  make dev        Install development dependencies"
	@echo "  make lint       Run linters"
	@echo "  make test       Run tests"
	@echo "  make docs       Build documentation"
	@echo "  make clean      Clean build artifacts"

install:
	poetry install --only main

dev:
	poetry install --with dev,docs
	poetry run pre-commit install

lint:
	poetry run pre-commit run --all-files

test:
	poetry run pytest

docs:
	poetry run sphinx-build -b html docs docs/_build/html

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} +