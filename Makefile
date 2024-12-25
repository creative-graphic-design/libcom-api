PYTHON_VERSION=3.8
IMAGE_NAME=libcom-api

.PHONY: setup
setup:
	pip install -U uv

.PHONY: uv-pin-$(PYTHON_VERSION)
uv-pin-$(PYTHON_VERSION):
	uv python pin $(PYTHON_VERSION)

.PHONY: lock
lock:
	uv lock

.PHONY: build
build:
	uv sync --extra build

.PHONY: chumpy
chumpy: build
	uv sync --extra chumpy

.PHONY: libcom
libcom: build
	uv sync --extra libcom

.PHONY: install
install: uv-pin-$(PYTHON_VERSION) lock chumpy libcom

#
# linter/formatter/typecheck
#

.PHONY: lint
lint:
	uv run ruff check --output-format=github .

.PHONY: format
format:
	uv run ruff format --check --diff .

.PHONY: typecheck
typecheck:
	uv run mypy --cache-dir=/dev/null .

.PHONY: test
test:
	uv run pytest -vsx --log-cli-level=INFO

#
# Docker
#
.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME) .

.PHONY: docker-run
docker-run: docker-build
	docker run -it --rm \
		--name $(IMAGE_NAME)-dev \
		$(IMAGE_NAME) /bin/bash

#
# FastAPI
#
.PHONY: run
run:
	uv run fastapi dev src/libcom_api/__init__.py

.PHONY: clean
clean:
	rm -rf .venv
	rm uv.lock
