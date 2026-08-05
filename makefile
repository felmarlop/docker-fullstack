# -----------------------------------------------------------------------------
# Docker Fullstack Boilerplate
#
# Copyright (c) 2026 Felix Martin
# -----------------------------------------------------------------------------

ENV_FILE = .env

include $(ENV_FILE)
export

COMPOSE = docker compose -f compose.dev.yml
COMPOSE_PROD = docker compose -f compose.prod.yml
BACKEND = $(COMPOSE) exec backend
BACKEND_PROD = $(COMPOSE_PROD) exec backend
FRONTEND = $(COMPOSE) exec frontend
NGINX = $(COMPOSE) exec nginx
CELERY_BEAT = $(COMPOSE) exec celery-beat
CELERY_WORKER = $(COMPOSE) exec celery-worker
BACKEND_CI = $(COMPOSE) run --rm backend

.PHONY: \
	help \
	build \
	rebuild \
	start \
	stop \
	restart \
	backend-shell \
	frontend-shell \
	beat-shell \
	worker-shell \
	reload-nginx \
	create-superuser \
	generate-django-secret-key \
	logs \
	backend-logs \
	frontend-logs \
	nginx-logs \
	celery-worker-logs \
	celery-beat-logs \
	postgres-logs \
	redis-logs \
	backend-lint \
	backend-lint-fix \
	backend-type-check \
	frontend-lint \
	frontend-lint-fix \
	backend-test \
	backend-ci-lint \
	backend-ci-test \
	backend-ci-type-check \
	build-prod \
	start-prod \
	stop-prod \
	restart-prod \
	backend-shell-prod \
	logs-prod

help:
	@echo ""
	@echo "Docker Fullstack Boilerplate"
	@echo ""
	@echo " \033[1mAvailable commands:\033[0m"
	@echo ""
	@echo "  \033[1m - make build \033[0m			Build the images and start the containers"
	@echo "  \033[1m - make rebuild \033[0m			Rebuild the images and start the containers without cache"
	@echo "  \033[1m - make start \033[0m   			Start the containers"
	@echo "  \033[1m - make stop \033[0m    			Stop the containers"
	@echo "  \033[1m - make restart \033[0m 			Restart the containers"
	@echo ""
	@echo "  \033[1m - make backend-shell \033[0m		Open a shell in the backend container"
	@echo "  \033[1m - make frontend-shell \033[0m 		Open a shell in the frontend container"
	@echo "  \033[1m - make beat-shell \033[0m			Open a shell in the Celery Beat container"
	@echo "  \033[1m - make worker-shell \033[0m   		Open a shell in the Celery Worker container"
	@echo ""
	@echo "  \033[1m - make reload-nginx \033[0m 		Reload Nginx configuration"
	@echo "  \033[1m - make create-superuser \033[0m		Create Django superuser"
	@echo "  \033[1m - make generate-django-secret-key \033[0m	Generate a new Django secret key"
	@echo ""
	@echo "  \033[1m - make logs \033[0m           		Show general logs"
	@echo "  \033[1m - make backend-logs \033[0m   		Show backend logs"
	@echo "  \033[1m - make frontend-logs \033[0m   		Show frontend logs"
	@echo "  \033[1m - make logs-nginx-logs \033[0m   		Show Nginx logs"
	@echo "  \033[1m - make celery-worker-logs \033[0m    		Show Celery Worker logs"
	@echo "  \033[1m - make celery-beat-logs \033[0m      		Show Celery Beat logs"
	@echo "  \033[1m - make postgres-logs \033[0m  		Show PostgreSQL logs"
	@echo "  \033[1m - make redis-logs \033[0m     		Show Redis logs"
	@echo ""
	@echo "  \033[1m - make backend-lint \033[0m			Check code formatting and linting"
	@echo "  \033[1m - make backend-lint-fix \033[0m		Apply lint and formatting fixes"
	@echo "  \033[1m - make frontend-lint \033[0m		Check code formatting and linting"
	@echo "  \033[1m - make frontend-lint-fix \033[0m		Apply lint and formatting fixes"
	@echo "  \033[1m - make backend-type-check \033[0m		Run Pyright static type checking"
	@echo "  \033[1m - make backend-test \033[0m			Run tests"
	@echo ""

show-dev-urls:
	@echo ""
	@echo "🐳 Docker Fullstack Boilerplate is running!"
	@echo ""
	@echo "Available services:"
	@echo ""
	@echo "  ✔ Application	http://localhost:$(NGINX_PORT)"
	@echo "  ✔ API		http://localhost:$(NGINX_PORT)/api/"
	@echo "  ✔ Admin	http://localhost:$(NGINX_PORT)/admin/"
	@echo ""

# -----------------------------------------------------------------------------
# Development commands
# -----------------------------------------------------------------------------

build:
	$(COMPOSE) build
	$(COMPOSE) up -d
	@$(MAKE) --no-print-directory show-dev-urls

rebuild:
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d
	@$(MAKE) --no-print-directory show-dev-urls

start:
	$(COMPOSE) up -d
	@$(MAKE) --no-print-directory show-dev-urls

stop:
	$(COMPOSE) down

restart: stop start

backend-shell:
	$(BACKEND) bash

frontend-shell:
	$(FRONTEND) sh

beat-shell:
	$(CELERY_BEAT) bash

worker-shell:
	$(CELERY_WORKER) bash

reload-nginx:
	$(NGINX) nginx -t
	$(NGINX) nginx -s reload

create-superuser:
	$(BACKEND) python manage.py createsuperuser

generate-django-secret-key:
	$(BACKEND) python manage.py generate_secret_key

logs:
	$(COMPOSE) logs -f

backend-logs:
	$(COMPOSE) logs -f backend

frontend-logs:
	$(COMPOSE) logs -f frontend

nginx-logs:
	$(COMPOSE) logs -f nginx

celery-worker-logs:
	$(COMPOSE) logs -f celery-worker

celery-beat-logs:
	$(COMPOSE) logs -f celery-beat

postgres-logs:
	$(COMPOSE) logs -f postgres

redis-logs:
	$(COMPOSE) logs -f redis

backend-lint:
	$(BACKEND) ruff check .
	$(BACKEND) ruff format . --check

backend-lint-fix:
	$(BACKEND) ruff check . --fix
	$(BACKEND) ruff format .

frontend-lint:
	cd frontend && pnpm lint:check
	cd frontend && pnpm format:check

frontend-lint-fix:
	cd frontend && pnpm lint
	cd frontend && pnpm format

backend-type-check:
	$(BACKEND) pyright

backend-test:
	$(BACKEND) pytest

# -----------------------------------------------------------------------------
# Continuous Integration commands (Github Actions)
# -----------------------------------------------------------------------------

backend-ci-lint:
	$(BACKEND_CI) ruff check .
	$(BACKEND_CI) ruff format . --check

backend-ci-type-check:
	$(BACKEND_CI) pyright

backend-ci-test:
	$(BACKEND_CI) pytest

# -----------------------------------------------------------------------------
# Production commands
# -----------------------------------------------------------------------------

build-prod:
	$(COMPOSE_PROD) up -d --build

start-prod:
	$(COMPOSE_PROD) up -d

stop-prod:
	$(COMPOSE_PROD) down

restart-prod: stop-prod start-prod

backend-shell-prod:
	$(BACKEND_PROD) bash

logs-prod:
	$(COMPOSE_PROD) logs -f
