import praw
import datetime
import keys as key
import extarct_food_name as AI
import pandas as pd
from google.cloud import storage


reddit = praw.Reddit(client_id = key.client_id,          # your client id
                      client_secret = key.secret,        # your client secret
                      user_agent = key.agent,            # user agent name,
                      username = key.username,           # your reddit username
                      password = key.password) 


# add the subreddit name we want to scrape 


def title_scrapper(subreddit,delta):
    subreddit = reddit.subreddit(subreddit)

    latest_date = datetime.datetime.utcnow().date() - datetime.timedelta(days=delta) # as we want to scrape last day
    todays_title = []

    for submission in subreddit.new(limit=None):
        if datetime.datetime.fromtimestamp(submission.created_utc).date() == latest_date:
            todays_title.append(submission.title)
   

    str_todays_title = ' '.join(todays_title)

    response = AI.generate_restaurant_name_and_item(str_todays_title)

    cleaned_data = response['food_items'].strip()

    # create_file_on_gcp(subreddit,latest_date,cleaned_data)

    print("original data ")
    print(todays_title)

    print("cleaned data")
    print(cleaned_data)

def create_file_on_gcp(subreddit, latest_date, data):
    # Create a storage client
    client = storage.Client()
    file_name  =  str(subreddit) + "/" + str(subreddit) + "_" + str(latest_date) + ".csv" 

    file_name  =  "/" + str(subreddit) + "/" + str(latest_date) + ".csv" 

    # Create a bucket
    bucket = client.bucket('realtime_recipe')

    # Create a blob
    blob = bucket.blob(file_name)

    # Write some data to the blob
    blob.upload_from_string(data)



