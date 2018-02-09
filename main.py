from credentials import *

import json
import os
import praw
import requests
import sqlite3
import time
import tweepy

def get_image_description(image_url):

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    params = {
        'visualFeatures': 'Description'
    }

    image_data = {
        'url': image_url
    }

    response = requests.request('POST', AZURE_URL, headers=headers, params=params, json=image_data, data=None)

    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8'))
        return content['description']['captions'][0]['text']
    
    return None

# Create db connection
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS descriptions
             (id text, url text, description text, posted text)''')

# Reddit auth
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='foodDescriptionBot v0.1')

# Twitter auth
twitter_auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
twitter_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(twitter_auth)

while True:

    submissions = reddit.subreddit('FoodPorn').hot(limit=20)

    for sbm in submissions:

        if sbm.url.endswith(('.jpg', '.png')):

            # Search if already tweeted
            id = (sbm.id, )
            c.execute('SELECT * FROM descriptions WHERE id=?', id)
            row = c.fetchone()

            if row is None:

                desc = get_image_description(sbm.url)

                if desc is not None:

                    row_to_save = (sbm.id, desc, sbm.url, False)
                    c.execute('INSERT INTO descriptions VALUES (?, ?, ?, ?)', row_to_save)
                    conn.commit()

                    # Download image
                    filename = 'temp_image.{}'.format(sbm.url[-3:])
                    request = requests.get(sbm.url, stream=True)
                    if request.status_code == 200:
                        with open(filename, 'wb') as image:
                            for chunk in request:
                                image.write(chunk)

                        error = False

                        # Tweet
                        try:
                            twitter_api.update_with_media(filename, status=desc)
                        except:
                            error = True
                        
                        # Remove image
                        os.remove(filename)

                        if not error:
                            pass
                        
                    else:
                        pass

                    time.sleep(10 * 60)
    
    time.sleep(45 * 60)

conn.close()