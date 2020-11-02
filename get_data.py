# Standards
import pandas as pd
import numpy as np

# API
import requests

# Automating
import time
import datetime
import warnings
import sys

# Set base url
# url = 'https://api.pushshift.io/reddit/search/submission/?subreddit='

# # Set params
# params = {
#     'subreddit': 'fallout',
#     'size': 50,
#     'lang': True,
#     'before': 1601384439
# }

# # Make request
# res = requests.get(url, params)

# **Write Function**

def get_posts(subreddit, n_iter, epoch_right_now): # subreddit name and number of times function should run
    '''pulls comments from subreddit'''
    # store base url variable
    base_url = 'https://api.pushshift.io/reddit/search/submission/?subreddit='
    # instantiate empty list    
    df_list = []
    # save current epoch, used to iterate in reverse through time
    current_time = epoch_right_now
    # set up for loop
    for post in range(n_iter):
        # instantiate get request
        res = requests.get(
            # requests.get takes base_url and params
            base_url,
            # parameters for get request
            params = {    
                # specify subreddit
                'subreddit' : subreddit,
                # specify number of posts to pull
                'size' : 100,
                # ???
                'lang': True,
                # pull everything from current time backward
                'before': current_time
            }
        )
        
        # take data from most recent request, store as df
        df = pd.DataFrame(res.json()['data'])
        
        # pull specific columns from dataframe for analysis
        df = df.loc[:, ['title', 
                       'created_utc',
                       'selftext',
                       'subreddit',
                       'author',
                       'media_only',
                       'permalink']
                   ]
        
        # append to empty dataframe list
        df_list.append(df)
        
        # add wait time
        time.sleep(15)
        
        # set current time counter back to last epoch in recently grabbed df
        current_time = df['created_utc'].min()
    # return one dataframe for all requests
    
    return pd.concat(df_list, axis=0)

time_now = 1601670694
n_iters = 50

# **Use function on Fallout subreddit**
fallout = get_posts('Fallout', n_iters, time_now)

# **Use function on Star Trek subreddit**

startrek = get_posts('startrek', n_iters, time_now)

# # **Combine the DataFrames**
both = pd.concat([fallout, startrek])

both.to_csv('./data/test_posts4.csv', index=False)

# **Note: you can automate this to function to run as a script**
# 
# 1. Add in time breaks between loops to not overload the API
# 2. Convert to .py
# 3. Utilize `caffienate` on terminal