#Zac Conley
#A06 - Emoji Scraper
#Grabs all emojis from site.

from bs4 import BeautifulSoup
import urllib2
import os
import requests
url = 'https://www.webfx.com/tools/emoji-cheat-sheet/' #url where emojis are
# Use beatiful soup to read the page
# then loop through the page with the following
print("\nZac Conley")
print("A06 - Emoji Scraper")
print("Grabs all emojis from site.\n")
newurl = urllib2.urlopen(url).read() #processes url
page = BeautifulSoup(newurl,'html.parser') # uses html parser to get rid of warning
path = os.path.dirname(os.path.abspath(__file__)) + '/emojis/' #sets path to emoji folder
if os.path.exists(path)==False: #if folder doesn't exist
    os.makedirs(path)
count=0
for emoji in page.find_all("span",{"class":"emoji"}): # find all emojis on site
    emoji_path = emoji['data-src'] 
    feedback = requests.get(url+emoji_path, stream=True)
    emoji_name=emoji_path.split("/") #gets name of emoji for file naming
    if feedback.status_code != 200: #if error
        print("Failure getting emoji!")
    else: #if emoji is found
        count+=1
        print("Downloading emoji "+str(count)+". "+emoji_name[2]) 
        with open(path+emoji_name[2], 'w+') as f: # save emoji in folder
            f.write(feedback.content)
            f.close()
print(str(count)+" images have been downloaded to your emoji folder!")