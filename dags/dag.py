from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from pathlib import Path

default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2022, 7, 13)
      }

dag = DAG('update_metis_project', default_args=default_args, schedule_interval="0 0 * * 0")
run_dir = Path(__file__).parent.parent.absolute()

t1 = BashOperator(
    task_id='push_new_housing_data',
    bash_command=f'python {run_dir}/get_api_data.py',
    dag=dag)

t2 = BashOperator(
    task_id='pull_new_housing_data',
    bash_command=f'python {run_dir}/pull_mongo_data.py',
    dag=dag)

t1 >> t2