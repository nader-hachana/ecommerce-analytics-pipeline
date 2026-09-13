FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY dbt ./dbt
COPY orchestration ./orchestration

ENV DAGSTER_HOME=/app/dagster_home
RUN mkdir -p /app/dagster_home

CMD ["uv", "run", "dagster", "dev", "-m", "orchestration.definitions", "-h", "0.0.0.0"]
