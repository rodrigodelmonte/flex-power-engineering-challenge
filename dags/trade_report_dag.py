import csv
import logging

import pendulum
from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from requests import Session
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util import Retry

logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": pendulum.datetime(2024, 2, 1, tz="UTC"),
    "fs_conn_id": "fs_default",
    "filepath": "/mnt/{{ ds_nodash }}/epex_trades_{{ ds_nodash }}.csv",
    "poke_interval": 10,
    "timeout": 60,
    "schedule_interval": "00 1 * * *",
    "catchup": True,
    "max_active_runs": 1,
}


def post_csv_records_to_api(filepath):

    records_count = 0
    http_client = Session()
    retries = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[502, 503, 504],
        allowed_methods={"POST"},
    )
    http_client.mount("http://", HTTPAdapter(max_retries=retries))

    trade_api = BaseHook.get_connection("trade_api")

    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for record in reader:
            if record:
                response = http_client.post(
                    url=f"{trade_api.host}/v1/trades",
                    json=record,
                    auth=HTTPBasicAuth(trade_api.login, trade_api.password),
                    timeout=20,
                )
                response.raise_for_status()
                records_count += 1
    logger.info("Number of records processed: %s", records_count)


dag = DAG(
    dag_id="trade_report_dag",
    description="Process daily report trades",
    default_args=DEFAULT_ARGS,
)

with dag:

    wait_for_csv = FileSensor(
        task_id="wait_for_csv",
        filepath=DEFAULT_ARGS.get("filepath"),
        poke_interval=5,
        timeout=60,
        dag=dag,
    )

    process_csv = PythonOperator(
        task_id="process_csv",
        python_callable=post_csv_records_to_api,
        op_kwargs={
            "filepath": DEFAULT_ARGS.get("filepath"),
        },
        dag=dag,
    )

    check_result = HttpSensor(
        task_id="check_result",
        http_conn_id="trade_api",
        endpoint="/v1/trades?delivery_day={{ds}}",
        method="GET",
        response_check=lambda response: response.status_code == 200,
        dag=dag,
    )

    wait_for_csv >> process_csv >> check_result
