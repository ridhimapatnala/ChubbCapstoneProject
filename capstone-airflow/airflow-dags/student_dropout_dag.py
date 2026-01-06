"""
Airflow DAG to trigger ETL process for student dropout analysis
Custom logs are written to a separate file under airflow-logs
"""

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import logging
import os
from logging.handlers import RotatingFileHandler

# Custom logger setup
def get_custom_logger():
    LOG_DIR = "/opt/airflow/logs/student_dropout_custom"
    os.makedirs(LOG_DIR, exist_ok=True)

    LOG_FILE = os.path.join(LOG_DIR, "student_dropout_etl.log")

    logger = logging.getLogger("student_dropout_custom")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5 * 1024 * 1024,   #5mb limit per log file
            backupCount=3
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s" 
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def log_dag_start(**context):
    logger = get_custom_logger()
    logger.info(
        f"DAG started | dag_id={context['dag'].dag_id} | run_id={context['run_id']}"
    )

def log_dag_end(**context):
    logger = get_custom_logger()
    logger.info(
        f"DAG completed | dag_id={context['dag'].dag_id} | run_id={context['run_id']}"
    )

default_args = {
    "owner": "Ridhima",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# DAG Definition
with DAG(
    dag_id="student_dropout_databricks_etl",
    description="Trigger Databricks Serverless Job for student dropout ETL",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["student_dropout", "databricks", "serverless"],
) as dag:

    start_etl = PythonOperator(
        task_id="start_etl",
        python_callable=log_dag_start
    )
    # main task to run databricks job
    run_student_dropout_job = DatabricksRunNowOperator(
        task_id="run_student_dropout_serverless_job",
        databricks_conn_id="databricks_default",
        job_id=736310244288717
    )

    end_etl = PythonOperator(
        task_id="end_etl",
        python_callable=log_dag_end,
        trigger_rule=TriggerRule.ALL_DONE
    )

    start_etl >> run_student_dropout_job >> end_etl
