#!/usr/bin/env python3
import praw
import pickle
from pyaml import yaml
import time

#Load config
with open("config.yaml", "r") as f:
    config = yaml.load(f)["api"]

reddit = praw.Reddit(
                    client_id     = config["clientid"],
                    client_secret = config["secret"],
                    username      = config["username"],
                    password      = config["password"],
                    user_agent    = config["uagent"] 
                )

reddit.login(config["username"], config["password"])

with open("ads-{}".format(time.strftime("%Y-%m-%d")), "r") as f:
  data = f.read()

reddit.submit("PotentialHailCorp", "Ads for {}".format(time.strftime("%Y-%m-%d")), text=data)
