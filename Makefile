.PHONY: setup run test clean

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	python src/run.py "Analyze ROAS drop"

test:
	python -m pytest -q

clean:
	rm -rf __pycache__ .pytest_cache logs/* reports/*
