from datetime import datetime,timedelta
import json
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.functions import CloudFunctionInvokeFunctionOperator

default_args = {
    'owner': 'sowmya.neela@sjsu.edu',
    'start_date': datetime(2023, 1, 1),
    'retries': 5,
    'email_on_failure': 'sowmya.neela@sjsu.edu',
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'cloud_functions_orchestration',
    default_args=default_args,
    description='Orchestrate two Google Cloud Functions',
    schedule_interval='0 12 * * *',
    catchup=False
)

input_json_data = {
  "data": {
    "data": "SGVsbG8gV29ybGQ="
  }
}
payload = json.dumps(input_json_data)
start_pipeline = DummyOperator(
        task_id = 'start_pipeline',
        dag = dag,
        )
trigger_cloud_function_1 = CloudFunctionInvokeFunctionOperator(
    task_id='trigger_cloud_function_1',
    project_id='integral-plexus-406801',  # Your Google Cloud project ID
    location='us-east1',  # The location of your Cloud Function
    function_id='web_scraping',  # The ID of your Cloud Function
    input_data = {"data": payload},
    dag=dag,
)
trigger_cloud_function_2 = CloudFunctionInvokeFunctionOperator(
    task_id='trigger_cloud_function_2',
    project_id='integral-plexus-406801',  # Your Google Cloud project ID
    location='us-east1',  # The location of your Cloud Function
    function_id='load_file_from_bucket_to_bigquery',  # The ID of your Cloud Function
    input_data = {"data": payload},
    dag=dag,
)

finish_pipeline = DummyOperator(
        task_id = 'finish_pipeline',
        dag = dag
        )
start_pipeline >> trigger_cloud_function_1 >> trigger_cloud_function_2 >> finish_pipeline