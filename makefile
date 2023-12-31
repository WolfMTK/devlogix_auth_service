THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help all build up prod stop restart logs ps migrate, bash
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

all: build up run_migrate_bot

build:
	docker compose build $(c)

up:
	docker compose up $(c)

prod:
	docker compose up -d $(c)

stop:
	docker compose stop $(c)

restart:
	docker compose stop
	docker compose up -d

logs:
	docker compose logs --tail=100 -f $(c)

ps:
	docker compose ps

bash:
	docker compose exec -it $(c) bash

migrate:
	docker compose exec -it $(c) alembic upgrade head

run_migrate_bot:
	docker compose exec -it bot alembic upgrade head
