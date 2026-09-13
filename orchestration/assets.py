import subprocess
from pathlib import Path

from dagster import AssetExecutionContext, AssetKey, AssetOut, MaterializeResult, multi_asset
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets
from google.cloud import bigquery

from orchestration.project import dbt_project

DATA_DIR = Path(__file__).parent.parent / "data"
PROJECT_ID = "project-1bf8476e-c6ef-4205-840"
RAW_DATASET = "olist_raw"

# table name -> explicit schema, or None to autodetect
# product_category_name_translation needs an explicit one, its header has a BOM
# character that breaks autodetect
RAW_TABLES = {
    "olist_orders_dataset": None,
    "olist_order_items_dataset": None,
    "olist_order_payments_dataset": None,
    "olist_order_reviews_dataset": None,
    "olist_customers_dataset": None,
    "olist_products_dataset": None,
    "olist_sellers_dataset": None,
    "olist_geolocation_dataset": None,
    "product_category_name_translation": "product_category_name:STRING,product_category_name_english:STRING",
}


@multi_asset(
    outs={name: AssetOut(key=["raw", name]) for name in RAW_TABLES},
    group_name="raw",
)
def raw_olist_tables(context: AssetExecutionContext):
    """Downloads the Olist dataset from Kaggle and loads each table into BigQuery."""
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", "olistbr/brazilian-ecommerce", "-p", str(DATA_DIR), "--unzip", "--force"],
        check=True,
    )

    client = bigquery.Client(project=PROJECT_ID)

    for table_name, schema in RAW_TABLES.items():
        csv_path = DATA_DIR / f"{table_name}.csv"
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=schema is None,
            allow_quoted_newlines=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )
        if schema:
            job_config.schema = [bigquery.SchemaField(*col.split(":")) for col in schema.split(",")]

        with open(csv_path, "rb") as f:
            job = client.load_table_from_file(f, f"{PROJECT_ID}.{RAW_DATASET}.{table_name}", job_config=job_config)
        job.result()

        table = client.get_table(f"{PROJECT_ID}.{RAW_DATASET}.{table_name}")
        yield MaterializeResult(asset_key=["raw", table_name], metadata={"row_count": table.num_rows})


class OlistDbtTranslator(DagsterDbtTranslator):
    """Maps dbt sources onto the raw_olist_tables assets."""

    def get_asset_key(self, dbt_resource_props):
        if dbt_resource_props["resource_type"] == "source":
            return AssetKey(["raw", dbt_resource_props["name"]])
        return super().get_asset_key(dbt_resource_props)


@dbt_assets(manifest=dbt_project.manifest_path, dagster_dbt_translator=OlistDbtTranslator())
def olist_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
