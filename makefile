# -----------------------------------------------------------------------------
# Docker Fullstack Boilerplate
#
# Copyright (c) 2026 Felix Martin
# --

COMPOSE = docker compose --env-file backend/.env
BACKEND = $(COMPOSE) exec backend

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
	@echo "  \033[1m - make up \033[0m         Start the containers"
	@echo "  \033[1m - make shell \033[0m      Open a shell in the backend container"
	@echo "  \033[1m - make rebuild \033[0m    Rebuild the images and start the containers"
	@echo "  \033[1m - make down \033[0m       Stop the containers"
	@echo "  \033[1m - make restart \033[0m    Restart the containers"
	@echo ""

up:
	$(COMPOSE) up

rebuild:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

restart: down up

shell:
	$(BACKEND) bash

lint:
	$(BACKEND) ruff check .
	$(BACKEND) ruff format . --check

lint-fix:
	$(BACKEND) ruff check . --fix
	$(BACKEND) ruff format .
