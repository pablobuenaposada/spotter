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
	 docker compose up -d --force-recreate
	 docker exec $(DOCKER_IMAGE)-django-1 make tests

docker/run:
	docker compose -f docker-compose.yml up --force-recreate -d --build

docker/format/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make format/check'

docker/migrations/check:
	 docker run --env-file .env.local $(DOCKER_IMAGE) /bin/sh -c 'make migrations/check'

docker/loader:
	docker exec -it $(DOCKER_IMAGE)-django-1 python src/manage.py load_books

tests: venv-dev
	poetry run pytest src/tests