"""
Airflow DAG to trigger ETL process for student dropout analysis
"""

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime, timedelta
import logging
import os
from logging.handlers import RotatingFileHandler

# Logging Configuration

LOG_DIR = "/opt/airflow/logs/student_dropout_etl"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "student_dropout_etl.log")

logger = logging.getLogger("student_dropout_etl")
logger.setLevel(logging.INFO)

# prevent duplicate logging handlers 
if not logger.handlers:
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Monitoring 
def on_task_success(context):
    logger.info(
        f"Task {context['task_instance'].task_id} completed successfully "
        f"for DAG {context['dag'].dag_id}"
    )

def on_task_failure(context):
    logger.error(
        f"Task {context['task_instance'].task_id} failed "
        f"for DAG {context['dag'].dag_id}",
        exc_info=True
    )

default_args = {
    "owner": "Ridhima",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_success_callback": on_task_success,
    "on_failure_callback": on_task_failure,
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

    logger.info("Initializing Student Dropout Databricks ETL DAG")

    run_student_dropout_job = DatabricksRunNowOperator(
        task_id="run_student_dropout_serverless_job",
        databricks_conn_id="databricks_default",
        job_id=736310244288717
    )

    logger.info(
        "DatabricksRunNowOperator configured with job_id=736310244288717"
    )
