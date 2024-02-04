import pendulum
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor

DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": pendulum.datetime(2024, 2, 1, tz="UTC"),
    "poke_interval": 10,
    "timeout": 60,
    "schedule_interval": "00 2 * * *",
    "catchup": True,
    "max_active_runs": 1,
}

dag = DAG(
    dag_id="pnl_report_dag_v01",
    description="Process daily PNL report",
    template_searchpath="/opt/airflow/include",
    default_args=DEFAULT_ARGS,
)

with dag:

    check_source_table = SqlSensor(
        task_id="check_source_table",
        conn_id="flexpower_db",
        sql="select count(1) from public.trade where delivery_day = '{{ ds }}';",
    )

    upsert_daily_pnl_report = SQLExecuteQueryOperator(
        task_id="upsert_daily_phl_report",
        conn_id="flexpower_db",
        sql="upsert_daily_pnl_report.sql",
    )

    check_daily_phl_report = SqlSensor(
        task_id="check_daily_phl_report",
        conn_id="flexpower_db",
        sql="select count(1) from public.pnl_reports where delivery_day = '{{ ds }}';",
    )

    (check_source_table >> upsert_daily_pnl_report >> check_daily_phl_report)
