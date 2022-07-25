
from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta

with DAG('save_tweet_dag', description='Python DAG', schedule_interval='*/15 * * * *', start_date=datetime(2018, 11, 1), catchup=False) as dag:
    save_tweet_task	= BashOperator(task_id='python_task', bash_command="python /opt/airflow/py_jobs/Colect_twitter.py")
save_tweet_task

