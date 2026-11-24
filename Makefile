.PHONY: format lint baseline typecheck check auto all

# Les outils sont lancés dans l'environnement du projet (uv sync --group dev).
RUN ?= uv run
# Pause en secondes entre deux tours de make auto.
AUTO_INTERVAL ?= 10

format:
	@echo "▶ Tri des imports avec isort, puis formatage avec Ruff..."
	$(RUN) isort .
	$(RUN) ruff format .

lint:
	@echo "▶ Linting avec Ruff..."
	-$(RUN) ruff check --no-fix .
	@echo "▶ Linting avec pydoclint..."
	$(RUN) pydoclint .
	@echo "▶ Linting avec pylint..."
	-$(RUN) pylint src tests

baseline:
	@echo "▶ Régénération des baselines de Ruff, pylint et pydoclint..."
	-$(RUN) ruff check --no-fix . > ruff-baseline.txt
	-$(RUN) pylint --output=pylint-baseline.txt src tests
	$(RUN) pydoclint --generate-baseline=True .

typecheck:
	@echo "▶ Analyse statique avec mypy..."
	$(RUN) mypy src

check: lint format typecheck

auto:
	@while true; do \
		$(MAKE) --no-print-directory all; \
		echo "▶ Prochain tour dans $(AUTO_INTERVAL) s (Ctrl+C pour arrêter)"; \
		sleep $(AUTO_INTERVAL); \
	done

all: check
