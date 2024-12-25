PYTHON_VERSION=3.8
IMAGE_NAME=libcom-api

.PHONY: setup
setup:
	pip install -U uv

.PHONY: uv-pin-$(PYTHON_VERSION)
uv-pin-$(PYTHON_VERSION):
	uv python pin $(PYTHON_VERSION)

.PHONY: build
build:
	uv sync --extra build

.PHONY: chumpy-install
chumpy-install: build
	uv sync --extra chumpy-compile

.PHONY: libcom-install
libcom-install: build

	uv sync --extra libcom-compile

.PHONY: install
install: uv-pin-$(PYTHON_VERSION) chumpy-install libcom-install

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

.PHONY: clean
clean:
	rm -rf .venv
	rm uv.lock
