# Import the usual suspects 
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from get_data import get_data
from print_stock_data import print_stock_data
from data_to_blob import data_to_blob
from datetime import datetime


# Define or Instantiate DAG
dag = DAG(
    'stock_data_ETL_FTSE',
    start_date=datetime(2024, 12, 18),
    end_date=datetime(2025, 12, 31),
    schedule_interval='0 17 * * *', # GMT
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    catchup=False
)

# Define or Instantiate Tasks

# Use a task to collect data from our API 

data_grab_task = PythonOperator(
    task_id='get_data_task',
    python_callable= get_data,
    dag=dag
)

# Create task to save, clean and then, print data in Airflow for validation 

print_stock_data = PythonOperator(

    task_id='print_stock_data',

    python_callable = print_stock_data,

    dag=dag
)

# Upload data from our local save to our Azure storage blob 

upload_to_blob = PythonOperator(
        task_id='upload_to_blob',
        python_callable = data_to_blob,
        op_kwargs={
            'container_name': 'stockdatablob',
            'execution_date': str(datetime.today().strftime('%Y-%m-%d'))
        }
    )

# Define Task Dependencies
data_grab_task >> print_stock_data >> upload_to_blob
