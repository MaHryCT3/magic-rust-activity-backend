TAIL=100

define set-default-container
	ifndef c
	c = fastapi
	else ifeq (${c},all)
	override c=
	endif
endef


set-container:
	$(eval $(call set-default-container))
build:
	docker compose -f docker-compose.dev.yml build
up:
	docker compose -f docker-compose.dev.yml up -d
down:
	docker compose -f docker-compose.dev.yml down
logs: set-container
	docker compose -f docker-compose.dev.yml logs --tail=$(TAIL) -f $(c)
restart: set-container
	docker compose -f docker-compose.dev.yml restart $(c)
exec: set-container
	docker compose -f docker-compose.dev.yml exec $(c) /bin/bash

compile-reqs: set-container
	poetry export --without-hashes > requirements.txt

test: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) python -m pytest
