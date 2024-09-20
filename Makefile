DOCKER_IMAGE=spotter

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

migrations/check:
	poetry run python src/manage.py makemigrations --check --dry-run

docker/build:
	docker build --no-cache	--tag=$(DOCKER_IMAGE) .

docker/tests:
	 docker run $(DOCKER_IMAGE) make tests

docker/format/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make format/check'

docker/migrations/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make migrations/check'

tests: venv-dev
	DJANGO_SETTINGS_MODULE=main.settings PYTHONPATH=src poetry run pytest src/tests