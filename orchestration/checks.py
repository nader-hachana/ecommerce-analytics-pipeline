from dagster import AssetCheckResult, AssetCheckSeverity, AssetKey, asset_check
from google.cloud import bigquery

from orchestration.assets import PROJECT_ID


@asset_check(asset=AssetKey("fct_order_items"))
def fct_order_items_matches_source_grain():
    """fct_order_items should have exactly one row per source order item, no fan-out from the payment/review joins."""
    client = bigquery.Client(project=PROJECT_ID)
    row = list(
        client.query(f"""
            select
              (select count(*) from `{PROJECT_ID}.olist_dbt.fct_order_items`) as fct_rows,
              (select count(*) from `{PROJECT_ID}.olist_raw.olist_order_items_dataset`) as source_rows
        """).result()
    )[0]

    return AssetCheckResult(
        passed=row.fct_rows == row.source_rows,
        metadata={"fct_rows": row.fct_rows, "source_rows": row.source_rows},
        severity=AssetCheckSeverity.ERROR,
    )
