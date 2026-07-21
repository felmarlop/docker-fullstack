# -----------------------------------------------------------------------------
# Docker Fullstack Boilerplate
#
# Copyright (c) 2026 Felix Martin
# --

COMPOSE = docker compose --env-file backend/.env
BACKEND = $(COMPOSE) exec backend
CI_COMPOSE = docker compose --env-file backend/.env.example
CI_BACKEND = $(CI_COMPOSE) run --rm backend

.PHONY: \
	help \
	up \
	shell \
	rebuild \
	down \
	restart

help:
	@echo ""
	@echo "Docker Fullstack Boilerplate"
	@echo ""
	@echo " \033[1mAvailable commands:\033[0m"
	@echo ""
	@echo "  \033[1m - make build \033[0m         Rebuild the images and start the containers"
	@echo "  \033[1m - make start \033[0m         Start the containers"
	@echo "  \033[1m - make stop \033[0m          Stop the containers"
	@echo "  \033[1m - make restart \033[0m       Restart the containers"
	@echo "  \033[1m - make shell \033[0m         Open a shell in the backend container"
	@echo "  \033[1m - make lint \033[0m          Check code formatting and linting with Ruff"
	@echo "  \033[1m - make lint-fix \033[0m      Check ruff format and apply changes"
	@echo "  \033[1m - make test \033[0m          Run tests"
	@echo "  \033[1m - make type-check \033[0m    Run Pyright static type checking"
	@echo ""

build:
	$(COMPOSE) up --build

start:
	$(COMPOSE) up

stop:
	$(COMPOSE) down

restart: stop start

shell:
	$(BACKEND) bash

lint:
	$(BACKEND) ruff check .
	$(BACKEND) ruff format . --check

lint-fix:
	$(BACKEND) ruff check . --fix
	$(BACKEND) ruff format .

test:
	$(BACKEND) pytest

type-check:
	$(BACKEND) pyright

# Continuous Integration commands (Github Actions)
ci-build:
	$(CI_COMPOSE) up -d --build

ci-stop:
	$(CI_COMPOSE) down

ci-lint:
	$(CI_BACKEND) ruff check .
	$(CI_BACKEND) ruff format . --check

ci-test:
	$(CI_BACKEND) pytest

ci-type-check:
	$(CI_BACKEND) pyright
