import json
import os
import sys
"""
Course: cmps 4883
Assignemt: A03
Date: 2/10/19
Github username: acdczlc
Repo url: https://github.com/acdczlc/4883-SWTools-Conley
Name: Zac Conley
Description: 
   Calculates all stats for questions about stats

"""
##############################################################
# MostTeams(dict of off and def players)
# gets player who played for most teams
# 
# Params: 
#    dict of players
# Returns: 
#    player with most teams
def MostTeams(OffAndDef):
    most=[]
    count=0 # set comparison
    for playerid, playerdata in OffAndDef.items():
        if(playerdata['name']!=''): #only get real players
            if(len(playerdata['Teams'])>count):
                count=len(playerdata['Teams']) #get count
                most=[[playerdata['name'],len(playerdata['Teams'])]] # replace with player
            elif(len(playerdata['Teams'])==count):
                most.append([playerdata['name'],len(playerdata['Teams'])]) # add multiple teams
    return most

##############################################################
# MostTeamsOneYear(dict of off and def players)
# gets player who played for most teams in one year
# 
# Params: 
#    dict of players
# Returns: 
#    player with most teams
def MostTeamsOneYear(OffAndDef):
    teams={}
    maximum={}
    count=0
    for playerid, playerdata in OffAndDef.items():
        if(playerdata['name']!=''):
            for years in playerdata:  #avoids all keys except years 
                if(years!='Drops' and years!='NegRushYards' and years!='NegRush' and years!='Teams' and years!='PassForLoss' and years!="name"):
                    try: #try block to avoid nonplayers
                        if(len(playerdata[years])>count): # if player has most teams so far
                            if((len(playerdata[years]) not in teams.keys())): 
                                teams.clear() # delete all previous players
                                teams[len(playerdata[years])]={}
                            teams[len(playerdata[years])][playerdata['name']]=years
                            count=len(playerdata[years])
                        elif(len(playerdata[years])==count): #multiple players have the same number of teams
                            teams[len(playerdata[years])].append(playerdata['name'],years)
                    except:
                        pass

    return teams
##############################################################
# NegativeRushingYards(dict of off and def players)
# gets player with most negative rushing yards
# 
# Params: 
#    dict of players
# Returns: 
#    player with most negative rushing yards
def NegativeRushingYards(OffAndDef):
    NegRushYds=[]
    yds=0
    for playerid, playerdata in OffAndDef.items():
        if(playerdata['NegRushYards']<yds):
            yds=playerdata['NegRushYards']
            NegRushYds=[[playerdata['name'],playerdata['NegRushYards']]]
        elif(playerdata['NegRushYards']==yds):
            NegRushYds.append([playerdata['name'],playerdata['NegRushYards']])
    return NegRushYds
##############################################################
# NegativeRushes(dict of off and def players)
# gets player with most negative rushes
# 
# Params: 
#    dict of players
# Returns: 
#    player with most negative rushes
def NegativeRushes(OffAndDef):
    rushes=[]
    att=0 #attempts
    for player in OffAndDef:
        if(OffAndDef[player]['NegRush']>att):
            att=OffAndDef[player]['NegRush']
            rushes=[[OffAndDef[player]['name'],OffAndDef[player]['NegRush']]]
        elif(OffAndDef[player]['NegRush']==att):
            rushes.append([OffAndDef[player]['name'],OffAndDef[player]['NegRush']])
    return rushes   
##############################################################
# MostPassForLoss(dict of off and def players)
# gets player with most negative rushes
# 
# Params: 
#    dict of players
# Returns: 
#    player with most negative rushes
def MostPassForLoss(OffAndDef):
    PassForLoss=[]
    att=0 #attempts
    for player in OffAndDef:
        if(OffAndDef[player]['PassForLoss']>att):
            att=OffAndDef[player]['PassForLoss']
            PassForLoss=[[OffAndDef[player]['name'],OffAndDef[player]['PassForLoss']]]
        elif(OffAndDef[player]['PassForLoss']==att):
            PassForLoss.append([OffAndDef[player]['name'],OffAndDef[player]['PassForLoss']])
    return PassForLoss 

##############################################################
# MostPenalties(dict of team penalties)
# gets team with most penalties
# 
# Params: 
#    dict of teams
# Returns: 
#    player with most negative rushes
def MostPenalties(penalties):
    pens=[]
    num=0
    for teamname,teamdata in penalties.items():
        if(teamdata['Penalties']>num):
            num=teamdata['Penalties']
            pens=[[teamname,teamdata['Penalties']]]
        elif (teamdata['Penalties']==num):
            pens.append([teamname,teamdata['Penalties']])
    return pens
  
##############################################################
# TeamPenaltyYards(dict of team penalties)
# gets team with most penaltiy yards
# 
# Params: 
#    dict of teams
# Returns: 
#   team with most penalty yards
def TeamPenaltyYards(penalties):
    pens=[]
    num=0
    for teamname,teamdata in penalties.items():
        if(teamdata['PenaltyYards']>num):
            num=teamdata['PenaltyYards']
            pens=[[teamname,teamdata['PenaltyYards']]]
        elif (teamdata['PenaltyYards']==num):
            pens.append([teamname,teamdata['PenaltyYards']])
    return pens
##############################################################
# PenaltyWins(most penalized team,dict of team penalties)
# shows correlation between penalty and record
# 
# Params: 
#    dict of teams, most penalized team
# Returns: 
#   team with most penaltys and least
def PenaltyWins(penalties):
    x=MostPenalties(penalties) #calls function to get most penalized team
    mostPenalized=[]
    for temp in x:
        mostPenalized.append(team[0])
    least=penalties[mostPenalized[0]]['Penalties']
    mostandleast=[[mostPenalized[0],penalties[mostPenalized[0]]['Wins'],penalties[mostPenalized[0]]['Losses']]] # sets most penalized record
    leastTeam=[]
    for teamname, teamdata in penalties.items():
        if(teamdata['Penalties']<least):
            least=teamdata['Penalties']
            leastTeam=[[teamname,teamdata['Wins'],teamdata['Losses']]]
        elif (teamdata['Penalties']==least):
            leastTeam.append([teamname,teamdata['Wins'],teamdata['Losses']])
    mostandleast.append(leastTeam[0]) #adds team and record to list at end
    return mostandleast

##############################################################
# AverageNumberOfPlays()
# shows average number of plays
# 
# Params: 
#    none
# Returns: 
#  avg number of plays
def AverageNumberOfPlays():
    games=0
    plays=0
    for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))+'/stats'): # sets path to all stats
        with open(os.path.dirname(os.path.abspath(__file__))+"/stats/"+filename,"r") as json_file:
            try: #gets all stats and stores each game in a dict
                data=json.load(json_file)
            except:
                pass
            else:
                for gameid, gamedata in data.items(): 
                    if(gameid!="nextupdate"):
                       games+=1 #increment number of games
                       for driveid, drivedata in gamedata['drives'].items():
                            if(driveid!="crntdrv"):
                                plays+=drivedata['numplays'] #increment number of plays
    avgplays=plays/games
    return avgplays
##############################################################
# LongestFG(dict of fgs)
# longest field goal
# 
# Params: 
#    dict of fgs
# Returns: 
#  longest field goal and kicker
def LongestFG(fg):
    fgs=[]
    length=0 #longest fg
    for playerid,playerdata in fg.items():
        if(playerdata['Long']>length):
            length=playerdata['Long']
            fgs=[[playerdata['Name'],playerdata['Long']]]
        elif (playerdata['Long']==length):
            fgs.append([playerdata['Name'],playerdata['Long']])
    return fgs
##############################################################
# MostFG(dict of fgs)
# most made field goals
# 
# Params: 
#    dict of fgs
# Returns: 
#  most made field goals and kicker
def MostFG(fg):
    fgs=[]
    count=0 #sets counter to 0
    for playerid,playerdata in fg.items():
        if(playerdata['FG']>count): #if largest number of fg so far
            count=playerdata['FG']
            fgs=[[playerdata['Name'],playerdata['FG']]]
        elif (playerdata['FG']==count): #if same number of fg
            fgs.append([playerdata['Name'],playerdata['FG']])
    return fgs
##############################################################
# MostMFG(dict of fgs)
# most missed field goals
# 
# Params: 
#    dict of fgs
# Returns: 
#  most missed field goals and kicker
def MostMFG(fg):
    fgs=[]
    count=0 #set counter to 0
    for playerid,playerdata in fg.items():
        if(playerdata['MFG']>count): #if most misses so far
            count=playerdata['MFG']
            fgs=[[playerdata['Name'],playerdata['MFG']]]
        elif (playerdata['MFG']==count): #if same as most misses
            fgs.append([playerdata['Name'],playerdata['MFG']])
    return fgs
##############################################################
# MostDrops(dict of players)
# most drops
# 
# Params: 
#    dict of players
# Returns: 
#  most drops
def MostDrops(OffAndDef):
    drops=[] 
    count=0 #set drops to 0
    for player in OffAndDef:
        if(OffAndDef[player]['Drops']>count):
            count=OffAndDef[player]['Drops']
            drops=[[OffAndDef[player]['name'],OffAndDef[player]['Drops']]]
        elif(OffAndDef[player]['Drops']==count):
            drops.append([OffAndDef[player]['name'],OffAndDef[player]['Drops']])
    return drops

path= os.path.dirname(os.path.abspath(__file__)) #set path to current location
f=open(path+'/OffAndDef.json','r') #open separated files
OffAndDef=json.load(f)
f.close()
f=open(path+'/Penalties.json','r')    
penalties=json.load(f)
f.close()
f=open(path+'/FG.json','r')
fg=json.load(f)
f.close()
print("\n")
print("Name: Zac Conley")
print("Assignment: A03 - Nfl Stats")
print("Date: 2/10/19")
print("==================================================================================")
print("Question 1: Find the player(s) that played for the most teams.")
playerlist=MostTeams(OffAndDef)
for p in playerlist:
    print(str(p[0]) + ": "+ str(p[1]) +" teams\n")
print("==================================================================================")
print("Question 2: Find the player(s) that played for multiple teams in one year.")
ans=MostTeamsOneYear(OffAndDef)
count=0
for numteams in ans.items():
    for player in numteams[1].items():
        print(player[1]+": " +player[0]+" "+str(numteams[0])+" teams." )
print
print("==================================================================================")
print("Question 3: Find the player(s) that had the most yards rushed for a loss.")
ans=NegativeRushingYards(OffAndDef)
for player in ans:
    print(player[0]+": "+str(player[1])+" rushing yards.\n")
print("==================================================================================")
print("Question 4: Find the player(s) that had the most rushes for a loss.")
ans=NegativeRushes(OffAndDef)
for player in ans:
    print(player[0]+": "+str(player[1])+" negative rushes.\n")
print("==================================================================================")
print("Question 5: Find the player(s) with the most number of passes for a loss.")
ans=MostPassForLoss(OffAndDef)
for player in ans:
    print(player[0]+": "+str(player[1])+" negative passes.\n")
temp=[]
print("==================================================================================")
print("Question 6: Find the team with the most penalties.")
ans=MostPenalties(penalties)
for team in ans:
    print(str(team[0])+" had "+str(team[1])+" penalties.\n")
print("==================================================================================")
print("Question 7: Find the team with the most yards in penalties.")
ans=TeamPenaltyYards(penalties)
for team in ans:
    print(team[0]+": "+str(int(team[1]))+" penalty yards.\n")
print("==================================================================================")
print("Question 8: Find the correlation between most penalized teams and games won / lost.")
ans=PenaltyWins(penalties)
print("Most Penalties: "+ans[0][0]+": "+str(ans[0][1]) +"-" +str(ans[0][2]))
print("Least Penalties: "+ans[1][0]+" : "+str(ans[1][1])+"-" +str(ans[1][2])+"\n")
print("==================================================================================")
print("Question 9: Average number of plays in a game. (This may take up to a minute.)")
ans=AverageNumberOfPlays()
print("On average, there are " +str(ans) +" plays each game. \n")
print("==================================================================================")
print("Question 10: Longest field goal.")
ans=LongestFG(fg)
for player in ans:
    print(player[0]+": "+str(player[1])+" yards.\n")
print("==================================================================================")
print("Question 11: Most field goals.")
ans=MostFG(fg)
for player in ans:
    print(player[0]+": "+str(player[1])+" FGs.\n")
print("==================================================================================")
print("Question 12: Most missed field goals.")
ans=MostMFG(fg)
for player in ans:
    print(player[0]+": "+str(player[1])+" missed FGs.\n")
print("==================================================================================")
print("Question 13: Most dropped passes.")
ans=MostDrops(OffAndDef)
for player in ans:
    print(player[0]+": "+str(player[1])+" drops.")