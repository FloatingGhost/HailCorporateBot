#!/usr/bin/env python3
import praw
from pyaml import yaml

with open("config.yaml", "r") as f:
    config = yaml.load(f)["api"]

print("Identifying as {}".format(config["username"]))

reddit = praw.Reddit(
                    client_id     = config["clientid"],
                    client_secret = config["secret"],
                    username      = config["username"],
                    password      = config["password"],
                    user_agent    = config["uagent"] 
                )
