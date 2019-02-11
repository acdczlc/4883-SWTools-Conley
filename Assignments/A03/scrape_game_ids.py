from beautifulscraper import BeautifulScraper
from pprint import pprint
import urllib
import json
import sys
from time import sleep
from random import shuffle
import os
"""
Course: cmps 4883
Assignemt: A03
Date: 2/10/19
Github username: acdczlc
Repo url: https://github.com/acdczlc/4883-SWTools-Conley
Name: Zac Conley
Description: 
  scrapes ids from internet

"""
sleeper=.01 #set sleep timer to prevent over requesting server
scraper = BeautifulScraper() #initialize scraper
sch = "http://www.nfl.com/schedules/" #url of schedules
firstyear=2009 #first year searching
lastyear=2019 #last year to search (up to year before)
preseason = [x for x in range(0, 5)] 
regseason = [x for x in range(1, 18)]
years = [x for x in range(firstyear, lastyear)] #sets ranges for years and weeks of season
print("Fetching all gameids from "+str(firstyear)+"-"+str(firstyear+1)+" to "+str(lastyear-1)+"-"+str(lastyear))
print("This will take several minutes, please be patient.") #user message
print("This program will let you know when it is done.")
gameids = { #3 types in a season
        "preseason": {},
        "regular_season": {},
        "playoffs": {}
    }
   
for year in years: #for each year searching
       # gameids['preseason'][year] = {} #creates dictionary to hold weeks for each year
        print("Fetching ids from year "+str(year)) #user message

        #for week in preseason: #for each preseason game
          #  gameids['preseason'][year][week] = [] # creates list to hold gameids
          #  url = sch + '%d/PRE%s' % (year, week) 
          #  scrapegames = scraper.go(url)
           # weekgames = scrapegames.find_all( #scrapes all games
            #    'div', {'class': 'schedules-list-content'})
            #for slot in weekgames:   #for each game add to weekly list
               # gameids['preseason'][year][week].append(slot['data-gameid'])
              #  sleep(sleeper)

        gameids['regular_season'][year] = {} #creates dictionary to hold weeks for each year
        for week in regseason:
            gameids['regular_season'][year][week] = [] # creates list to hold gameids
            url = sch + '%d/REG%s' % (year, week)
            scrapegames = scraper.go(url)
            weekgames = scrapegames.find_all( #scrapes all games
                'div', {'class': 'schedules-list-content'})
            for slot in weekgames:  #for each game add to weekly list
                gameids['regular_season'][year][week].append(slot['data-gameid'])
                sleep(sleeper)

        gameids['playoffs'][year] = [] # one list for all playoff games
        url = sch + '%d/POST' % (year)
        scrapegames = scraper.go(url)
        weekgames = scrapegames.find_all( #get all playoff games
            'div', {'class': 'schedules-list-content'})
        for slot in weekgames: #add all games to list
            gameids['playoffs'][year].append(slot['data-gameid'])
            sleep(sleeper)

path = os.path.dirname(os.path.abspath(__file__)) + '/games/' #sets path with new games folder
filename = 'gameids_from_%s_to_%s' % (firstyear, lastyear) + '.json' #names file
if os.path.exists(path)==False: #if file doesn't exist
    os.makedirs(path)
f = open(path + filename, 'w+')
f.write(json.dumps(gameids))
f.close()
print("Done")
print("Saved "+filename+" in the current directory in the folder: games")
