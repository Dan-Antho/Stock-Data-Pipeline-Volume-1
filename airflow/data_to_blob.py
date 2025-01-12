from airflow.providers.microsoft.azure.hooks.wasb import WasbHook 
# Upload to Azure Blob Storage
def data_to_blob(ti, container_name, execution_date):
    # Get file path, stock ticker and exchange
    file_path = ti.xcom_pull(key='output_path', task_ids='get_data_task')
    print(file_path)
    print(type(file_path))
    ticker = 'AAPL'
    exchange = 'NASDAQ'
 
    # Format the blob name acording to the date of data collection and other relevant info
    blob_name = f'{execution_date}_{ticker}_{exchange}_processed_stock_data'
    
    hook = WasbHook(wasb_conn_id='azure_storage_blob')
    hook.load_file(file_path, container_name, blob_name, overwrite=False)
