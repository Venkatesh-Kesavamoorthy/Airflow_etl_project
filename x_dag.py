from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from x_etl import run_x_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 4,
    'retry_delay': timedelta(minutes=16),  # rate limit window
}

with DAG(
    'x_dag',
    default_args=default_args,
    description='Fetch Elon Musk tweets and save to S3',
    schedule_interval=None,   # ✅ no automatic scheduling, manual trigger only
    catchup=False,
) as dag:

    run_etl = PythonOperator(
        task_id='run_etl',
        python_callable=run_x_etl,
    )

    run_etl
