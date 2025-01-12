import os
import pandas as pd
import json
from datetime import datetime
import requests
from airflow.models import Variable


def get_data(ti):

    # Load raw data into DataFrame
    api_key_val = Variable.get("StockData_API_KEY") # Use the secret variable function in Apache Airflow
    response = requests.get(api_key_val)

    data = response.json()['data']

    df = pd.DataFrame(data)

    # Replace Nulls (If Applicable)
    default_values = {
        int: 0, 
        float: 0.0, 
        str: '', 
    }

    cleaned_data = df.fillna(value=default_values)
    # Get the current date components
    now = pd.Timestamp.now()
    year = now.year
    month = now.month
    day = now.day

   # Create the directory path if it doesn't exist
    data_dir = f'/opt/airflow/data/StockData_cleaned/{year}/{month}/{day}'
    os.makedirs(data_dir, exist_ok=True)

    # Save the cleaned data to a new file
    cleaned_data.to_csv(f'{data_dir}/StockData.csv', index=False)
    ti.xcom_push(key='output_path', value=f'{data_dir}/StockData.csv')
