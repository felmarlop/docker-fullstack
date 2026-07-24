# 🚀 Docker Fullstack Boilerplate

[![Python](https://img.shields.io/badge/python-3.13-blue.svg)]()
[![Django](https://img.shields.io/badge/django-5.2-green.svg)]()
[![PostgreSQL](https://img.shields.io/badge/postgresql-17-blue.svg)]()
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)]()

A modern full-stack boilerplate for building Django applications with Docker, Django REST Framework and Nuxt.

The goal of this project is to provide a clean, reusable and scalable foundation for future applications, following modern development practices and software architecture principles.

## 📖 Overview

Docker Fullstack Boilerplate is developed incrementally with a focus on:

- Containerized development workflows
- Clean backend architecture
- Modern frontend integration
- Automated code quality checks
- Production-oriented configuration

The project provides a complete foundation including backend, frontend and infrastructure services.

### Architecture

```mermaid
flowchart LR

    Browser[Browser]

    Browser --> Nginx[Nginx Reverse Proxy]

    Nginx --> Frontend[Nuxt Frontend]
    Nginx --> Backend[Django REST Framework API]

    Backend --> PostgreSQL[(PostgreSQL)]
    Backend --> Redis[(Redis)]

    Beat[Celery Beat] --> Redis
    Redis --> Worker[Celery Worker]

    Worker --> Email[Email Backend]
```

## 🛠️ Tech Stack

### Backend

- Python 3.13
- Django 5.2
- Django REST Framework
- PostgreSQL
- Redis
- Celery

### Frontend

- Vue 3
- Nuxt

### Infrastructure

- Docker
- Docker Compose
- Nginx
- Makefile

### Development Tools

- Ruff
- Pyright
- Pytest

## 📂 Project Structure

```text
.
├── backend/
├── frontend/
├── nginx/
├── compose.dev.yml
├── compose.prod.yml
├── Makefile
└── README.md
```

## ⚙️ Requirements

Before starting, make sure you have installed:

- Docker Engine
- Docker Compose v2
- Git

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/felmarlop/docker-fullstack.git

cd docker-fullstack
cp .env.example .env
```

Review the `.env` file and adjust the configuration to match your local environment if needed.

Build the development environment:

```bash
make build
```

## 📌 Supported Versions

| Component      | Version |
| -------------- | ------- |
| Docker Engine  | 29.3    |
| Docker Compose | 5.1     |
| Python         | 3.13    |
| Django         | 5.2     |
| PostgreSQL     | 17      |
| Ruff           | 0.15.20 |

## ✨ Features

- Docker Compose development environment
- Django REST Framework backend
- Nuxt frontend integration
- PostgreSQL database
- Redis message broker
- Celery background workers
- Environment-based configuration
- Persistent database storage
- PostgreSQL health checks
- Makefile development commands
- Automated linting and type checking
- Console email backend for local development
- Production-ready SMTP configuration

## 🧰 Commands

The project provides a set of Makefile shortcuts to manage the development environment.

| Command              | Description                                 |
| -------------------- | ------------------------------------------- |
| `make start`         | Start the containers                        |
| `make stop`          | Stop the containers                         |
| `make restart`       | Restart the containers                      |
| `make build`         | Rebuild the images and start the containers |
| `make shell`         | Open a shell in the backend container       |
| `make logs`          | Show general logs                           |
| `make logs-backend`  | Show backend logs                           |
| `make logs-worker`   | Show celery worker logs                     |
| `make logs-postgres` | Show postgreSQL logs                        |
| `make logs-redis`    | Show Redis logs                             |
| `make lint`          | Check code formatting and linting with Ruff |
| `make lint-fix`      | Apply Ruff formatting and lint fixes        |
| `make test`          | Run the test suite                          |
| `make type-check`    | Run Pyright static type checking            |

## ⚡ Background Tasks

The project includes Celery, Redis and Celery Beat configured out of the box.

- **Celery Worker** executes asynchronous background tasks.
- **Celery Beat** schedules periodic tasks and sends them to the worker.
- **Redis** acts as the message broker between Django, Beat and the Worker.
- **django-celery-beat** allows periodic tasks to be managed through the Django admin without modifying application code.

Password reset emails are processed asynchronously through Celery, while recurring jobs can be managed from the Django admin using `django-celery-beat`.

## 🚦 Continuous Integration

Every push and pull request automatically runs the backend quality checks using GitHub Actions.

The CI pipeline executes:

- **make lint**: Ruff (linting, formatting and import sorting)
- **make type-check**: Pyright (static type checking)
- **make test**: Pytest (test suite)

The workflow uses the same Docker environment as local development, ensuring consistent behavior across local machines and CI.

## 📄 License

License has not been defined yet.
