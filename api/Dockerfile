FROM python:3.11-slim

WORKDIR /usr/src/app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY src ./


CMD ["poetry", "run", "python", "main.py"]