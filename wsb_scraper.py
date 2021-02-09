from pmaw import PushshiftAPI
import psycopg2
import datetime
import pandas as pd
import re



api = PushshiftAPI()

start_time=int(datetime.datetime(2021, 2, 4).timestamp())


submissions = api.search_submissions(
                            after=start_time,
                            subreddit='wallstreetbets',
                            filter=['url', 'created_utc', 'author','title', 'selftext'],
                            limit=500)

cashtag_list = []
for submission in submissions:

    title_words = submission['title'].split()
    post_words = []
    if 'selftext' in submission:
        post_words = submission['selftext'].split()
    
    cashtags = list(set(filter(lambda word: word.startswith('$') and not word[1:2].isdigit() , title_words)))
    cashtags += list(set(filter(lambda word: word.startswith('$') and not word[1:2].isdigit(), post_words)))

    if len(cashtags) > 0:
        for cashtag in cashtags:
            if cashtag.lower() not in cashtag_list:
                cashtag = re.sub(r'[^\w\s]', '', cashtag)
                cashtag_list.append(cashtag.lower())
print(cashtag_list)

