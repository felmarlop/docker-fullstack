# -----------------------------------------------------------------------------
# Docker Fullstack Boilerplate
#
# Copyright (c) 2026 Felix Martin
# --

COMPOSE = docker compose --env-file backend/.env
BACKEND = $(COMPOSE) exec backend
NGINX = $(COMPOSE) exec nginx
CELERY_BEAT = $(COMPOSE) exec celery-beat
CELERY_WORKER = $(COMPOSE) exec celery-worker
CI_BACKEND = $(COMPOSE) run --rm backend

.PHONY: \
	help \
	build \
	start \
	stop \
	restart \
	shell \
	beat-shell \
	worker-shell \
	reload-nginx \
	generate-secret-key \
	logs \
	logs-backend \
	logs-nginx \
	logs-worker \
	logs-beat \
	logs-postgres \
	logs-redis \
	lint \
	lint-fix \
	test \
	type-check \
	ci-lint \
	ci-test \
	ci-type-check

help:
	@echo ""
	@echo "Docker Fullstack Boilerplate"
	@echo ""
	@echo " \033[1mAvailable commands:\033[0m"
	@echo ""
	@echo "  \033[1m - make build \033[0m          	Rebuild the images and start the containers"
	@echo "  \033[1m - make start \033[0m          	Start the containers"
	@echo "  \033[1m - make stop \033[0m           	Stop the containers"
	@echo "  \033[1m - make restart \033[0m        	Restart the containers"
	@echo "  \033[1m - make shell \033[0m          	Open a shell in the backend container"
	@echo "  \033[1m - make beat-shell \033[0m     	Open a shell in the Celery Beat container"
	@echo "  \033[1m - make worker-shell \033[0m   	Open a shell in the Celery Worker container"
	@echo "  \033[1m - make reload-nginx \033[0m 	Reload Nginx configuration"
	@echo "  \033[1m - make generate-secret-key \033[0m 	Generate a new Django secret key"
	@echo "  \033[1m - make logs \033[0m           	Show general logs"
	@echo "  \033[1m - make logs-backend \033[0m   	Show backend logs"
	@echo "  \033[1m - make logs-nginx \033[0m   	Show Nginx logs"
	@echo "  \033[1m - make logs-worker \033[0m    	Show Celery Worker logs"
	@echo "  \033[1m - make logs-beat \033[0m      	Show Celery Beat logs"
	@echo "  \033[1m - make logs-postgres \033[0m  	Show postgreSQL logs"
	@echo "  \033[1m - make logs-redis \033[0m     	Show Redis logs"
	@echo "  \033[1m - make lint \033[0m           	Check code formatting and linting with Ruff"
	@echo "  \033[1m - make lint-fix \033[0m       	Apply Ruff lint and formatting fixes"
	@echo "  \033[1m - make test \033[0m           	Run tests"
	@echo "  \033[1m - make type-check \033[0m     	Run Pyright static type checking"
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

beat-shell:
	$(CELERY_BEAT) bash

worker-shell:
	$(CELERY_WORKER) bash

reload-nginx:
	$(NGINX) nginx -t
	$(NGINX) nginx -s reload

generate-secret-key:
	$(BACKEND) python manage.py generate_secret_key

logs:
	$(COMPOSE) logs -f

logs-backend:
	$(COMPOSE) logs -f backend

logs-nginx:
	$(COMPOSE) logs -f nginx

logs-worker:
	$(COMPOSE) logs -f celery-worker

logs-beat:
	$(COMPOSE) logs -f celery-beat

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
ci-lint:
	$(CI_BACKEND) ruff check .
	$(CI_BACKEND) ruff format . --check

ci-test:
	$(CI_BACKEND) pytest

ci-type-check:
	$(CI_BACKEND) pyright
