from dagster import ScheduleDefinition, define_asset_job

daily_refresh_job = define_asset_job(name="daily_olist_refresh", selection="*")

daily_refresh_schedule = ScheduleDefinition(
    job=daily_refresh_job,
    cron_schedule="0 6 * * *",
)
