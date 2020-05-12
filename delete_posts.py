# created by u/kungming2 - modified to use botconfig.ini by u/CatFlier

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import datetime
import praw
import requests
import time
import os
import configparser

script_dir = os.path.dirname(os.path.realpath(__file__))  # get where the script is
botconfig = configparser.ConfigParser()
botconfig.read(script_dir + "/botconfig.ini")

reddit = praw.Reddit(client_id=botconfig["user"]["client_id"],
                     client_secret=botconfig["user"]["client_secret"],
                     username=botconfig["user"]["username"],
                     password=botconfig["user"]["password"],
                     user_agent=botconfig["useragent"]["user_agent"])

r = reddit.subreddit(botconfig["subname"]["subreddit"])

date_range = botconfig.get("date", "date_range")

def convert_to_unix(date_string):
    """Converts a date formatted as YYYY-MM-DD into a Unix integer of
    its equivalent UTC time.
    :param date_string: Any date formatted as YYYY-MM-DD.
    :return: The string timestamp of MIDNIGHT that day in UTC.
    """
    year, month, day = date_string.split('/')
    dt = datetime.datetime(int(year), int(month), int(day))
    utc_timestamp = int(dt.replace(tzinfo=datetime.timezone.utc).timestamp())
    return utc_timestamp

time_boundary = convert_to_unix(date_range)


def subreddit_pushshift_access(query_string, retries=3):
    """This function is called by others as the main point of query to
    Pushshift. It contains code to account for JSON decoding errors and
    to retry if it encounters such problems. It also converts JSON data
    into a Python dictionary.

    :param query_string: The exact API call we want to make.
    :param retries: The number of times (as an integer) that we want to
                    try connecting to the API. Default is 3.
    :return: An empty dictionary if there was a connection error,
             otherwise, a dictionary.
    """
    for _ in range(retries):
        try:
            returned_data = requests.get(query_string)
            returned_data = returned_data.json()
            return returned_data  # Return data as soon as it is found.
        except:
            continue

    return {}


def access_old_posts():
    all_posts = []

    query = "https://api.pushshift.io/reddit/search/submission/?subreddit={}&before={}&limit=1000&sort=asc&fields=id,created_utc"
    
    # Fetch the initial set of results.
    first_query = query.format(r, time_boundary)
    first_set = subreddit_pushshift_access(first_query)
    first_data = first_set['data']
    last_time = first_data[-1]['created_utc']
    first_posts = list(reddit.info(["t3_" + x['id'] for x in first_data]))  # Reddit fullnames.
    all_posts.extend(first_posts)
    
    for post in first_posts:
        print(post.title)
        if post.created_utc < time_boundary:
            post.mod.remove()

    # Cycle through the remainder, if there are more than 1000.
    if len(first_posts) == 1000:
        while last_time < time_boundary:
            new_query = query.format(r, time_boundary) + "&after={}".format(last_time)
            new_data = subreddit_pushshift_access(new_query)['data']
            new_posts = list(reddit.info(["t3_" + x['id'] for x in new_data]))  # Reddit fullnames.
            if not len(new_posts):
                break
                
            new_posts.sort(key=lambda y: y.id)
            last_time = int(new_posts[-1].created_utc)
            all_posts.extend(new_posts)
            
            for post in new_posts:
                print(post.title)
                if post.created_utc < time_boundary:
                    post.mod.remove()

    print("{:,} posts retrieved and removed".format(len(all_posts)))
    print("Done.")

    return
    

access_old_posts()