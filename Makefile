.PHONY: format lint typecheck check all

format:
	@echo "▶ Formatage avec Black et isort..."
	black .
	isort .

lint:
	@echo "▶ Linting avec Ruff..."
	-ruff check . --fix

typecheck:
	@echo "▶ Analyse statique avec mypy..."
	-mypy .

check: lint format typecheck

all: check
