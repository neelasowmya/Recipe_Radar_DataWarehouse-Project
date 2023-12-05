import base64
import pandas as pd 
import io
import os
from google.cloud import storage
from google.cloud import bigquery
from datetime import datetime

def main(event, context):

  food_porn = read_file('realtime_recipe','FoodPorn')
  food = read_file('realtime_recipe','food')

  print(food_porn.shape)
  print(food)


def get_latest_file(bucket_name, folder_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_name)
    latest_blob = max(blobs, key=lambda x: x.updated)
    return latest_blob.name

def read_file(bucket_name, folder_name):
  base = "gs://realtime_recipe/"
  file_name = get_latest_file(bucket_name,folder_name)
  csv = pd.read_csv(base + file_name,encoding='utf-8',
                    header=None, sep=',')
  csv = csv.T
  csv.columns = ['dish_name']
  date = file_name[10:20]
  csv['created_dt'] = datetime.strptime(date,'%Y-%m-%d').date()

  return csv

def hello_gcs(df):  
   ## Get BiqQuery Set up
   client = bigquery.Client()
   table = client.get_table(table_id)
   errors = client.insert_rows_from_dataframe(table, df)  # Make an API request.
   if errors == []:
        print("Data Loaded")
        return "Success"
   else:
        print(errors)
        return "Failed"