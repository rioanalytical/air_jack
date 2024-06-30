from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['your_email@example.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'complex_data_pipeline',
    default_args=default_args,
    description='A complex data pipeline DAG',
    schedule_interval=timedelta(days=1),
)

# Define tasks
def extract():
    print("Extracting data...")

def transform():
    print("Transforming data...")

def load():
    print("Loading data...")

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag,
)

mysql_task = MySqlOperator(
    task_id='run_mysql_query',
    mysql_conn_id='your_mysql_conn_id',
    sql='SELECT * FROM your_table;',
    dag=dag,
)

email_task = EmailOperator(
    task_id='send_email',
    to='your_email@example.com',
    subject='DAG Completed',
    html_content='Your DAG has completed successfully.',
    dag=dag,
)

# Define task dependencies
extract_task >> transform_task >> load_task >> mysql_task >> email_task
