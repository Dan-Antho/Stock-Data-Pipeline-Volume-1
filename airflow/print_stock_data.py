import pandas as pd
from datetime import datetime

# Define a function to print and save our stock data
def print_stock_data():

    # Get the current date components
    now = pd.Timestamp.now()
    year = now.year
    month = now.month
    day = now.day

    # Create the directory path if it doesn't exist
    data_dir = f'/opt/airflow/data/StockData_cleaned/{year}/{month}/{day}'

    cleaned_data= pd.read_csv(data_dir + "/StockData.csv")
    print(cleaned_data)
