# monkinetic Makefile
#
# this might be replaced later, but this gets things going
VENV:=$(shell pwd)/.venv
VENV_BIN:=$(VENV)/bin
MANAGE:=$(VENV_BIN)/python monkinetic/manage.py

# create local virtual environment
# I'm open to changing this uv (https://github.com/astral-sh/uv) if we want
.venv:
	python -mvenv $(VENV)

.PHONY: deps linting serve
# install application and development dependencies
deps:
	$(VENV_BIN)/pip install -r requirements.txt

# setup pre-commit linting with ruff
linting:
	$(VENV_BIN)/pre-commit install

dev: .venv deps linting

# serve the app natively
serve:
	$(VENV_BIN)/python monkinetic/manage.py runserver 0.0.0.0:8000

# django things
migrate_make:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

shell:
	$(MANAGE) shell

# Docker
build:
	docker build -t monkinetic:$(shell git rev-parse --short HEAD) -t monkinetic:latest -f docker/Dockerfile .

# Docker Compose
COMPOSE:=docker compose -f docker/docker-compose.yml

s:=
up:
	$(COMPOSE) up $(s) -d

s:=
attach:
	$(COMPOSE) up $(s)

s:=
restart:
	$(COMPOSE) restart $(s)

bash: up
	$(COMPOSE) exec web sh -c bash

down:
	$(COMPOSE) down

static: up
	$(COMPOSE) exec web sh -c '/opt/venv/bin/python /app/monkinetic/manage.py collectstatic'

logs:
	$(COMPOSE)  logs -f web

# deploy

fly_deploy:
	fly deploy

fly_logs:
	fly logs

fly_console:
	fly ssh console

fly_db_console:
	fly ssh console -a monkinetic-db
