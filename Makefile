DOCKER_IMAGE=pure

venv:
	poetry install --without dev

venv-dev:
	poetry install

format: venv-dev
	poetry run black src
	poetry run ruff check src --fix

format/check: venv-dev
	poetry run black --verbose src --check
	poetry run ruff check src

docker/build:
	docker build --no-cache	--tag=$(DOCKER_IMAGE) .

docker/format/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make format/check'