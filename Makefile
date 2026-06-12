.DEFAULT_GOAL := help
.PHONY: help setup install playwright test test-nav test-verbose run codegen

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

setup: install playwright ## Install dependencies and Playwright browsers

install: ## Install project dependencies with pdm
	pdm install

playwright: ## Install Playwright browsers
	pdm run python -m playwright install

test: ## Run all tests
	pdm run pytest -s

test-nav: ## Run the entity navigation tests
	pdm run pytest tests/ui/test_entity_navigation.py

test-verbose: ## Run tests with verbose output
	pdm run pytest -v

run: ## Run the FastAPI app locally
	pdm run uvicorn app.main:app --reload

codegen: ## Generate Playwright code against localhost:4200
	pdm run playwright codegen localhost:4200
