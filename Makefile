.PHONY: setup verify science-test science-artifacts web-dev web-test web-build check

setup:
	python -m pip install --no-build-isolation -r requirements-dev.txt
	npm install

verify:
	python scripts/research.py verify candidates/CANDIDATE-000001.json --reproducible

science-test:
	PYTHONPATH=src pytest

science-artifacts:
	python scripts/research.py verify candidates/CANDIDATE-000001.json --write --reproducible

web-dev:
	npm run dev

web-test:
	npm run test:web

web-build:
	npm run build

check: science-test web-test web-build
