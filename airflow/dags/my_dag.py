from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG("my_dag",
         start_date=datetime(2024, 2, 22),
         schedule_interval="30 14 * * *",
         catchup=False):

    task_a = BashOperator(
        task_id="task_a",
        bash_command="python /opt/airflow/scripts/extract/extract_urls.py"
    )
    
    task_b = BashOperator(
        task_id="task_b",
        bash_command="python /opt/airflow/scripts/extract/extract_data.py"
    )

    task_c = BashOperator(
        task_id="task_c",
        bash_command="python /opt/airflow/scripts/transform/transform_data.py"
    )

    task_d = BashOperator(
        task_id="task_d",
        bash_command="python /opt/airflow/scripts/load/load_data.py"
    )

    task_a >> task_b >> task_c >> task_d