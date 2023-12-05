from web_scrapper import title_scrapper

if __name__ == "__main__":

    subreddits = ['FoodPorn','Food']
    
    for subreddit in subreddits:
        for delta  in range(1,31,1):
            title_scrapper(subreddit,delta)






