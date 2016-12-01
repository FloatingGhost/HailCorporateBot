#!/usr/bin/env python3
import praw
import pickle
from pyaml import yaml

#Load config
with open("config.yaml", "r") as f:
    config = yaml.load(f)["api"]

#Load brandlist
with open("brandlist.txt", "r") as f:
    brands = [x.lower() for x in f.read().split("\n") if x != ""]

print("Loaded {} brands".format(len(brands)))

def save_scanned(scanned):
    """
        Save the posts we've already scanned
    """

    with open("already_scanned.dat", "wb") as f:
        pickle.dump(scanned, f)

#Try to load the things we've seen before
#Avoids replying to the same posts 
try:
    with open("already_scanned.dat", "rb") as f:
        already_scanned = pickle.load(f)
except Exception:
    already_scanned = []
    save_scanned(already_scanned)

print("Identifying as {}".format(config["username"]))

reddit = praw.Reddit(
                    client_id     = config["clientid"],
                    client_secret = config["secret"],
                    username      = config["username"],
                    password      = config["password"],
                    user_agent    = config["uagent"] 
                )

def test_post(submission):
    if submission.id not in already_scanned:
        # Make sure we don't see it again
        already_scanned.append(submission.id)
        save_scanned(already_scanned)

        for brand in brands:
            if brand in submission.title.lower():
                print("Possible match: {} [{}]".format(submission.title, brand))


        
while 1:
    # Retrieve r/all
    subreddit = reddit.get_subreddit("all")

    for post in subreddit.get_new():
        test_post(post)
