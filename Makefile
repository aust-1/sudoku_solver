.PHONY: format lint typecheck check auto all

format:
	@echo "▶ Formatage avec Ruff, puis Black et isort..."
	isort .
	black .
	ruff format

lint:
	@echo "▶ Linting avec Ruff..."
	-ruff check . --fix > ruff-baseline.txt
	@echo "▶ Linting avec pydoclint..."
	pydoclint .

typecheck:
	@echo "▶ Analyse statique avec mypy..."
	-mypy .

check: lint format typecheck

auto:
	make all
	make auto

all: check
