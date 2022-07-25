
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG('clean_tweet_dag', description='Python DAG', schedule_interval='*/20 * * * *', start_date=datetime(2018, 11, 1), catchup=False) as dag:
    clean_tweet_task	= BashOperator(task_id='python_task', bash_command="python /opt/airflow/py_jobs/Clean_Tweet.py")
clean_tweet_task