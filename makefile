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
	build \
	start \
	stop \
	restart \
	shell \
	logs \
	logs-backend \
	logs-worker \
	logs-postgres \
	logs-redis \
	lint \
	lint-fix \
	test \
	type-check \
	ci-build \
	ci-stop \
	ci-lint \
	ci-test \
	ci-type-check

help:
	@echo ""
	@echo "Docker Fullstack Boilerplate"
	@echo ""
	@echo " \033[1mAvailable commands:\033[0m"
	@echo ""
	@echo "  \033[1m - make build \033[0m          Rebuild the images and start the containers"
	@echo "  \033[1m - make start \033[0m          Start the containers"
	@echo "  \033[1m - make stop \033[0m           Stop the containers"
	@echo "  \033[1m - make restart \033[0m        Restart the containers"
	@echo "  \033[1m - make shell \033[0m          Open a shell in the backend container"
	@echo "  \033[1m - make logs \033[0m           Show general logs"
	@echo "  \033[1m - make logs-backend \033[0m   Show backend logs"
	@echo "  \033[1m - make logs-worker \033[0m    Show celery wroker logs"
	@echo "  \033[1m - make logs-postgres \033[0m  Show postgreSQL logs"
	@echo "  \033[1m - make logs-redis \033[0m     Show Redis logs"
	@echo "  \033[1m - make lint \033[0m           Check code formatting and linting with Ruff"
	@echo "  \033[1m - make lint-fix \033[0m       Apply Ruff lint and formatting fixes"
	@echo "  \033[1m - make test \033[0m           Run tests"
	@echo "  \033[1m - make type-check \033[0m     Run Pyright static type checking"
	@echo ""

build:
	$(COMPOSE) up -d --build

start:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) down

restart: stop start

shell:
	$(BACKEND) bash

logs:
	$(COMPOSE) logs -f

logs-backend:
	$(COMPOSE) logs -f backend

logs-worker:
	$(COMPOSE) logs -f celery-worker

logs-postgres:
	$(COMPOSE) logs -f postgres

logs-redis:
	$(COMPOSE) logs -f redis

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
