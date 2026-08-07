.PHONY: setup verify science-test science-artifacts web-dev web-test web-build check clean

setup:
	python -m pip install --no-build-isolation -e '.[dev]'
	npm ci

verify:
	python scripts/research.py verify candidates/CANDIDATE-000001.json --reproducible

science-test:
	PYTHONPATH=src pytest

science-artifacts:
	python scripts/research.py verify candidates/CANDIDATE-000001.json --write --reproducible

web-dev:
	npm run dev

web-test:
	npm run build
	npm run test:web

web-build:
	npm run build

check:
	npm run check

clean:
	rm -rf dist .pytest_cache **/__pycache__
