from beautifulscraper import BeautifulScraper
from pprint import pprint
import urllib
import json
import sys
from time import sleep
from random import shuffle
import os
stats_url = "http://www.nfl.com/liveupdate/game-center/"
name = "gameids_from_2009_to_2019.json" #file full of game ids
sleeper=.01 #sleep duration
ids = os.path.dirname(os.path.abspath(__file__)) + "/games/" #path to all game ids
stats = os.path.dirname(os.path.abspath(__file__)) + "/stats/" #path to where stats will be
if os.path.exists(ids)==False: #if there are no game ids make a folder
    os.makedirs(ids)
if os.path.exists(stats)==False: #if there are no stats make a folder
    os.makedirs(stats)
with open(ids + name) as readfile: #open file of ids
    data = json.load(readfile)
print("Please wait while game stats are downloaded. A confirmation will appear at the end.")
for s_type, subdictionary in data.items(): #preseason
    if s_type == "preseason":
        for year, weeks in subdictionary.items():
            print("Downloading "+str(year)+" preseason") 
            for week, gameids in weeks.items(): # get data from web based on gameid from file
                for gameid in gameids:
                    newurl = stats_url + "%s/%s_gtd.json" % (gameid, gameid)
                    urllib.urlretrieve(newurl, stats + gameid + ".json")
                    sleep(sleeper) #sleep for an amount of time
                    
    if s_type == "regular_season":
        for year, weeks in subdictionary.items():
            print("Downloading "+str(year)+" regular season")
            for week, gameids in weeks.items(): # get data from web based on gameid from file
                for gameid in gameids:
                    newurl = stats_url + "%s/%s_gtd.json" % (gameid, gameid)
                    urllib.urlretrieve(newurl, stats + gameid + ".json")
                    sleep(sleeper) #sleep for an amount of time

    if s_type == "playoffs":
        for year, gameids in subdictionary.items():
            print("Downloading "+str(year)+" playoffs")
            for gameid in gameids:  # get data from web based on gameid from file
                newurl = stats_url + "%s/%s_gtd.json" % (gameid, gameid)
                urllib.urlretrieve(newurl, stats + gameid + ".json")
                sleep(sleeper) #sleep for an amount of time
              
print("Done! A stats folder has been created with all of the requested data.")