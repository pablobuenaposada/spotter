FROM python:3.12

WORKDIR /app

COPY src /app/src
COPY Makefile poetry.lock pyproject.toml /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN make venv