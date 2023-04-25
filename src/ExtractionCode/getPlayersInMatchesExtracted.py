from apiConfig import api_key
from riotwatcher import LolWatcher, ApiError
import json
import time
watcher = LolWatcher(api_key)
region = 'euw1'
regionMatches='EUROPE'
def getSummonerIDByPuuid(region,puuid):
    summoner = watcher.summoner.by_puuid(region,puuid)
    return summoner
def getSummonerLeagueByID(region,id):
    summonerLeagueData=watcher.league.by_summoner(region,id)
    return summonerLeagueData
with open('summonerInfo.json', 'r') as f:
    summonersInfo = json.load(f)

playersAlreadyRegistered=set()

for id in summonersInfo:
    playersAlreadyRegistered.add(summonersInfo[id]["puuid"])


with open('matchesData.json', 'r') as f:
    matchesData = json.load(f)

Counter=1
playersThatAppearedInMatches=[]
for match in matchesData:
    participants=matchesData[match]["metadata"]["participants"]
    for participantPUUID in participants:
        if participantPUUID not in playersAlreadyRegistered:
            playersAlreadyRegistered.add(participantPUUID)
            summoner=getSummonerIDByPuuid(region,participantPUUID)
            summonerID=summoner["id"]
            playersThatAppearedInMatches.append(getSummonerLeagueByID(region,summonerID))
            print(Counter,"Got",summonerID)
            time.sleep(0.25)
            if Counter%90==0:
                time.sleep(120)
            Counter+=1

json_object = json.dumps(playersThatAppearedInMatches, indent=4)

with open("playersThatAppearedInMatches.json", "w") as outfile:
    outfile.write(json_object)


