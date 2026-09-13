from pathlib import Path

from dagster import Definitions
from dagster_dbt import DbtCliResource

from orchestration.assets import olist_dbt_assets, raw_olist_tables
from orchestration.checks import fct_order_items_matches_source_grain
from orchestration.project import dbt_project
from orchestration.schedules import daily_refresh_schedule

defs = Definitions(
    assets=[raw_olist_tables, olist_dbt_assets],
    asset_checks=[fct_order_items_matches_source_grain],
    schedules=[daily_refresh_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=dbt_project, profiles_dir=str(Path.home() / ".dbt")),
    },
)
