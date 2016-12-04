#!/usr/bin/env python3
import praw
import pickle
from pyaml import yaml
import time

#Load config
with open("config.yaml", "r") as f:
    config = yaml.load(f)["api"]

#Load brandlist
with open("brandlist.txt", "r") as f:
    brands = [x for x in f.read().split("\n") if x != ""]

#Defaults
with open("defaults.txt", "r") as f:
    defaults = [x for x in f.read().split("\n") if x != ""]

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

reddit.login(config["username"], config["password"])
def test_post(submission):
    if submission.id not in already_scanned:
        # Make sure we don't see it again
        already_scanned.append(submission.id)
        save_scanned(already_scanned)

        for brand in brands:
            if " {} ".format(brand) in submission.title:
                print("Possible match: {} [{}]".format(submission.title, brand))
                with open("ads-{}".format(time.strftime("%Y-%m-%d")), "a+") as f:
                  f.write("[{} :: {}]({})\n\n".format(submission.subreddit, submission.title,submission.permalink))

        
while 1:
    # Retrieve r/all
    for sub in defaults:
      subreddit = reddit.get_subreddit(sub)
      for post in subreddit.get_new():
        test_post(post)
