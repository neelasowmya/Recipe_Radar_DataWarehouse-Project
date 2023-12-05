from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator

default_args = {
    'owner': 'tianyu.wang@sjsu.edu',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define DAG
dag = DAG(
    'recipesql',
    default_args=default_args,
    description='Execute BigQuery SQL Query',
    schedule_interval=None,
    max_active_runs=1,  # Set max_active_runs to 1 for running only once
)

# Cloud Storage path 
gcs_data_path = 'gs://archive_recipes/recipes.csv'

# Define the task to import data into BigQuery
import_to_bigquery = GoogleCloudStorageToBigQueryOperator(
    task_id='import_to_bigquery',
    bucket='archive_recipes',
    source_objects=[gcs_data_path],
    destination_project_dataset_table='integral-plexus-406801.archiveRecipe.loadrecipe',  # Removed extra quotes
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_TRUNCATE',
    skip_leading_rows=1,  # Corrected parameter name
    field_delimiter=',',  # Adjust based on the delimiter of your data file
    dag=dag,
)

# define BigQueryOperator 
sql_query = """
SELECT
RecipeId, Name, AuthorId, DatePublished, RecipeCategory, Keywords, 
RecipeIngredientQuantities, RecipeIngredientParts, AggregatedRating, 
ReviewCount, Calories, FatContent, SaturatedFatContent, CholesterolContent, SodiumContent, 
CarbohydrateContent, FiberContent, SugarContent, ProteinContent,
RecipeServings, CookTimeInMinutes, PrepTimeInMinutes, TotalTimeInMinutes
FROM `integral-plexus-406801.archiveRecipe.Recipes`
WHERE RecipeId IS NOT NULL
  AND Name IS NOT NULL
  AND AuthorId IS NOT NULL
  AND DatePublished IS NOT NULL
  AND RecipeCategory IS NOT NULL
  AND Keywords IS NOT NULL
  AND RecipeIngredientQuantities IS NOT NULL
  AND RecipeIngredientParts IS NOT NULL
  AND AggregatedRating IS NOT NULL
  AND ReviewCount IS NOT NULL
  AND Calories IS NOT NULL
  AND FatContent IS NOT NULL
  AND SaturatedFatContent IS NOT NULL
  AND CholesterolContent IS NOT NULL
  AND SodiumContent IS NOT NULL
  AND CarbohydrateContent IS NOT NULL
  AND FiberContent IS NOT NULL
  AND SugarContent IS NOT NULL
  AND ProteinContent IS NOT NULL
  AND RecipeServings IS NOT NULL
  AND CookTimeInMinutes IS NOT NULL
  AND PrepTimeInMinutes IS NOT NULL
  AND TotalTimeInMinutes IS NOT NULL;
"""

# BigQueryExecuteQueryOperator
recipesql = BigQueryOperator(
    task_id='execute_bigquery_sql11',
    sql=sql_query,
    use_legacy_sql=False,  
    destination_dataset_table='integral-plexus-406801.archiveRecipe.Cleandata',
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',
    dag=dag,
)

# Set the import data task to run before the SQL query task
import_to_bigquery >> recipesql
