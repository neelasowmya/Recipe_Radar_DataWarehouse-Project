import praw
import datetime
import requests
import json
import time
import numpy as np
import pandas as pd
import keys as key

reddit = praw.Reddit(client_id = key.client_id,          # your client id
                      client_secret = key.secret,        # your client secret
                      user_agent = key.agent,            # user agent name,
                      username = key.username,           # your reddit username
                      password = key.password,      )    # your reddit password


#Start the clock
start = datetime.datetime.now()


#Get the post ID:
reddit_post_url = "https://www.reddit.com/r/AskReddit/comments/lvbv6v/for_five_minutes_you_get_transported_30_years/"
post_id = reddit.submission(url=reddit_post_url).id
print(post_id)

#PSAW to get all of the comment ID's
url = 'https://api.pushshift.io/reddit/submission/comment_ids/{}'.format(post_id)

json_ids = json.loads(requests.get(url).text)

print(json_ids)

comment_ids = json_ids['data']


#Create an empty list to house all of the comments
master_comment_list=[]

#Increment through the comments by 1000 (maximum size of a request i can use on PSAW)
step_counter = np.arange(0,len(comment_ids),1000)

#Have a list of the id strs that for some reason had a JSON Decode Error
error_links = []

remove_words = ['[removed]','[deleted]']

if not json_ids['data']:
    print("No data available for this post yet")
else:
    #Check if we have a tail
    if len(comment_ids) > step_counter[-1]:
        tail = len(comment_ids) - step_counter[-1]
    
    
    #Loop through the comment ids to extact the comments
    for count,item in enumerate(step_counter):
        #Need to clear the comment list each time
        comment_list=[]
        
        if count != len(step_counter) - 1: #Account for everything but the tail
            id_str = ','.join(comment_ids[item:step_counter[count+1]]) #Go from 0:1000, 1000:2000, 2000:3000, etc.
            
            
        else: #Account for the tail
            last_grouping = step_counter[count-1]
            id_str = ','.join(comment_ids[last_grouping : last_grouping + tail])
        
        #Load up the URL and get the JSON of comments
        test_url = 'https://api.pushshift.io/reddit/comment/search?ids={}'.format(id_str)
        
        try:
            json_comments = json.loads(requests.get(test_url).text)
            
            #Extract the comments from the JSON
            comment_list = [thing['body'] for thing in json_comments['data'] if thing['body'] not in remove_words]
            
            #Add comments to master list
            master_comment_list += comment_list
            
            print("Finished set {}".format(count))
            print("Sleeping for 3 seconds")
            time.sleep(3)
        
        except (RuntimeError, TypeError, NameError, ValueError):
            print("There was an error on count: {}".format(count))
            error_links.append([count,id_str])
            
    
    #Revisit any links that threw a JSON Decoding Error. Will continue until there are no more errors
    while error_links:
        print('\n',"Attempting to revisit URL's that provided an error",'\n')
        for count,things in enumerate(error_links):
            comment_list = []
            
            test_url = 'https://api.pushshift.io/reddit/comment/search?ids={}'.format(things[1])
            
            try:
                json_comments = json.loads(requests.get(test_url).text)
                
                #Extract the comments from the JSON
                comment_list = [thing['body'] for thing in json_comments['data'] if thing['body'] not in remove_words]
                
                #Add comments to master list
                master_comment_list += comment_list
                
                print("Finished set {}".format(things[0]))
                print("Removing this from the error list")
                
                error_links.pop(count)
                print("Sleeping for 3 seconds")
                time.sleep(3)
            
            except (RuntimeError, TypeError, NameError, ValueError):
                print("There's still an error on count: {}".format(things[0]))


    print(datetime.datetime.now() - start)
    
    #Make dataframe of comments
    comment_df = pd.DataFrame(master_comment_list)
    
    #Save Dataframe
    comment_df.to_csv('Master_Comment_List.csv',index = False) #index_col = 0 to make the first column in the csv the index