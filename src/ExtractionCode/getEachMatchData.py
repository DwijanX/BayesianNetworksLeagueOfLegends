from apiConfig import api_key
from riotwatcher import LolWatcher, ApiError
import json
import time
watcher = LolWatcher(api_key)
region = 'euw1'
regionMatches='EUROPE'

def extractImportantTeamInfo(teamInfo):
    ImportantTeamInfo={}
    ImportantTeamInfo["win"]=teamInfo["win"]
    ImportantTeamInfo["teamId"]=teamInfo["teamId"]
    return ImportantTeamInfo

def extractImportantParticipantsInfo(participantsInfo):
    ImportantParticipantsInfo={}
    ImportantParticipantsInfo["summonerName"]=participantsInfo["summonerName"]
    ImportantParticipantsInfo["teamPosition"]=participantsInfo["teamPosition"]
    ImportantParticipantsInfo["goldEarned"]=participantsInfo["goldEarned"]
    ImportantParticipantsInfo["championName"]=participantsInfo["championName"]
    ImportantParticipantsInfo["totalDamageDealtToChampions"]=participantsInfo["totalDamageDealtToChampions"]
    ImportantParticipantsInfo["win"]=participantsInfo["win"]
    return ImportantParticipantsInfo
    
    
def extractInfoMatch(matchInfo):
    importantInfo={}
    importantInfo["gameDuration"]=matchInfo["gameDuration"]
    importantInfo["participants"]=[]
    for participant in matchInfo["participants"]:
        importantInfo["participants"].append(extractImportantParticipantsInfo(participant))
    importantInfo["teams"]=[]
    for team in matchInfo["teams"]:
        importantInfo["teams"].append(extractImportantTeamInfo(team))
    return importantInfo


def extractImportantDataFrom(Match):
    newMatchObj={}
    newMatchObj["metadata"]=Match["metadata"]
    newMatchObj["info"]=extractInfoMatch(Match["info"])
    return newMatchObj

def getMatchData(region,id):
    matches = watcher.match.by_id(region,id)
    return matches

with open('matchesIDS.json', 'r') as f:
    matchesIds = json.load(f)

matchesData={}
counter=1
for matchID in matchesIds:
    match=getMatchData(regionMatches,matchID)
    matchData=extractImportantDataFrom(match)
    matchesData[matchID]=matchData
    print("Got",matchID)
    print("Matches Registered",matchesData.__len__())
    time.sleep(1)
    if(counter%89==0):
        time.sleep(120)
    counter+=1

json_object = json.dumps(matchesData, indent=4)

with open("matchesData.json", "w") as outfile:
    outfile.write(json_object)
