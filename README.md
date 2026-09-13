# E-Commerce Analytics Platform

[![dbt CI](https://github.com/nader-hachana/ecommerce-analytics-platform/actions/workflows/dbt-ci.yml/badge.svg)](https://github.com/nader-hachana/ecommerce-analytics-platform/actions/workflows/dbt-ci.yml)

dbt models on top of BigQuery, built from the Olist Brazilian E-Commerce dataset on Kaggle (~100k orders, 2016-2018). Orchestrated with Dagster, containerized with Docker.

See [ANALYSIS.md](ANALYSIS.md) for the actual findings, revenue by category, repeat purchase rate, and how delivery delay relates to review scores.

## Stack

- BigQuery
- dbt
- Dagster
- Docker

## Running it

You'll need a GCP project with BigQuery enabled and a Kaggle account.

```bash
uv sync
gcloud auth login
gcloud auth application-default login
gcloud config set project <your-project-id>
```

Get a Kaggle API token from kaggle.com/settings and save it to `~/.kaggle/access_token`.

Set `project` in `~/.dbt/profiles.yml` to your GCP project id (see `dbt/dbt_project.yml` for the profile name).

Then either run dbt directly:

```bash
cd dbt
uv run --project .. dbt build
```

Or run the whole pipeline (raw data load + dbt + tests) through Dagster:

```bash
uv run dagster dev -m orchestration.definitions
```

Or with Docker:

```bash
cd docker
docker compose up
```
