import sys
import os
from time import sleep
import json
"""
Course: cmps 4883
Assignemt: A03
Date: 2/10/19
Github username: acdczlc
Repo url: https://github.com/acdczlc/4883-SWTools-Conley
Name: Zac Conley
Description: 
  Separates stats into groups to make calculations easier

"""
print("Fetching FG stats, this may take a minute.")
#fetch all needed field goal stats
path= os.path.dirname(os.path.abspath(__file__)) + "/stats/" # sets path as stats folder
writepath=os.path.dirname(os.path.abspath(__file__))
FG={} # starts Field goal dictionary
for gamefile in os.listdir(path):
    with open(path+gamefile) as json_file:
        try:
            data=json.load(json_file)
        except: #if game file doesn't load
            pass
        else:
            for gameid in data: #navigate jsons
                if(gameid!="nextupdate"):
                    for driveid, drive in data[gameid]["drives"].items():
                        if(driveid!="crntdrv"):
                            for playid, play in drive["plays"].items():
                                for playername,player in play["players"].items():
                                    for playerinfo in player:
                                        if(playerinfo["statId"]==69 or playerinfo["statId"]==70 or
                                         playerinfo["statId"]==71 or playerinfo["statId"]==88):
                                            if(playername not in FG.keys()):
                                                FG[playername]={}
                                                FG[playername]["FG"]=0
                                                FG[playername]["MFG"]=0
                                                FG[playername]["Name"]=playerinfo["playerName"] #add player to dict
                                                FG[playername]["Long"]=0
                                            if(playerinfo["statId"]==70) : # get players longest field goal
                                                currentlong=FG[playername]["Long"]
                                                FG[playername]["FG"]+=1 #increment number of fgs
                                                if(playerinfo["yards"]>currentlong and playerinfo["yards"]>0 ):
                                                    FG[playername]["Long"]=playerinfo["yards"] 
                                            else:
                                                FG[playername]["MFG"]+=1 #increment missed field goals
print("Fetching off and def stats, this may take a while. (~20 minutes)")
offanddef={} #fetch all offense and defense stats

for gamefile in os.listdir(path): 
    with open(path+gamefile) as json_file:
        try:
            data=json.load(json_file)
        except:
            pass
        else:
            for gameid in data:
                if(gameid!="nextupdate"):
                    year=gameid[0:4]
                    for drives, drivedata in data[gameid]["drives"].items():
                        if(drives!="crntdrv"): #ignore current drive indicator
                            for play, playdata in drivedata["plays"].items():
                                for player, playerdata in playdata["players"].items():
                                    for playerinfo in playerdata:
                                        if(player not in offanddef.keys()): #add player
                                            offanddef[player]={}
                                            offanddef[player]["name"]=playerinfo["playerName"]
                                            offanddef[player]["Drops"]=0 
                                            offanddef[player]["Teams"]=[] 
                                            offanddef[player]["PassForLoss"]=0
                                            offanddef[player]["NegRushYards"]=0
                                            offanddef[player]["NegRush"]=0
                                        if(year not in offanddef[player].keys()): #add year for player
                                            offanddef[player][year]=[]
                                        if(playerinfo["statId"]==115 and ("drop" in playdata["desc"].lower())):
                                            offanddef[player]["Drops"]+=1 # add drops
                                        if(playerinfo["statId"]==10 and playerinfo["yards"]!=None and  playerinfo["yards"]<0):
                                            offanddef[player]["NegRush"]+=1 #add a negative rush
                                            offanddef[player]["NegRushYards"]+=playerinfo["yards"] #add negative rush yards
                                        if(playerinfo["clubcode"] not in offanddef[player][year]):
                                            offanddef[player][year].append(playerinfo["clubcode"])
                                        if(playerinfo["clubcode"] not in offanddef[player]["Teams"]): 
                                            offanddef[player]["Teams"].append(playerinfo["clubcode"]) 
                                        if(playerinfo["statId"]==15 and playerinfo["yards"]<0) and playerinfo["yards"]!=None:
                                            offanddef[player]["PassForLoss"]+=1 #add passes for loss
                                        
print("Fetching penalty stats, this may take a minute.")
penalties={} # get all needed team penalties
valid=json.load(open(writepath+"/Valid_Teams.json"))
for gamefile in os.listdir(path):
    with open(path+"/"+gamefile,"r") as json_file:
        try:
            data=json.load(json_file)
        except:
            pass
        else:
           for gameid in data:
                if(gameid!="nextupdate"):
                    awayteam=data[gameid]["away"]["abbr"]
                    hometeam=data[gameid]["home"]["abbr"]
                    if(awayteam in valid.keys() and hometeam in valid.keys()):
                        hometeam=valid[hometeam] 
                        awayteam=valid[awayteam]
                        hometeamscore=data[gameid]["home"]["score"]["T"]
                        awayteamscore=data[gameid]["away"]["score"]["T"]
                        if(hometeam not in penalties.keys()):
                            penalties[hometeam]={}
                            penalties[hometeam]["Wins"]=0
                            penalties[hometeam]["Losses"]=0
                            penalties[hometeam]["PenaltyYards"]=0
                            penalties[hometeam]["Penalties"]=0
                        if(awayteam not in penalties.keys()): #create teams
                            penalties[awayteam]={}
                            penalties[awayteam]["Wins"]=0
                            penalties[awayteam]["Losses"]=0
                            penalties[awayteam]["PenaltyYards"]=0
                            penalties[awayteam]["Penalties"]=0
                        if(awayteamscore>hometeamscore):
                            penalties[awayteam]["Wins"]+=1
                            penalties[hometeam]["Losses"]+=1
                        if(hometeamscore>awayteamscore): #calculate total w-l record
                            penalties[hometeam]["Wins"]+=1
                            penalties[awayteam]["Losses"]+=1    
                        for drives in data[gameid]["drives"].items():
                            if(drives[0]!="crntdrv"): #ignore current drive indicator
                                for play, playdata in drives[1]["plays"].items():
                                    for player in playdata["players"]:
                                        if(player!="0" and player != None):
                                            for playerinfo in playdata["players"][player]:
                                                if(playerinfo["statId"]==93): # penalty
                                                    if(playerinfo["yards"]!=None):
                                                        try: # add penalties
                                                            penalties[valid[playerinfo["clubcode"]]]["PenaltyYards"]+=(playerinfo["yards"])
                                                            penalties[valid[playerinfo["clubcode"]]]["Penalties"]+=1 
                                                        except:
                                                            pass
#writes stats to files to be used in calculations
print("Writing Stats to Files.")
x=open(writepath+"/Penalties.json","w")
x.write(json.dumps(penalties))
x.close()  
y=open(writepath+"/OffAndDef.json","w")
y.write(json.dumps(offanddef))
y.close()                                            
z=open(writepath+"/FG.json","w")
z.write(json.dumps(FG))
z.close() 
print("File writing complete!")