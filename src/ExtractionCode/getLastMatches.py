from apiConfig import api_key
from riotwatcher import LolWatcher, ApiError
import json
import time
watcher = LolWatcher(api_key)
region = 'euw1'
regionMatches='EUROPE'
def getMatches(region,puuid):
    matches = watcher.match.matchlist_by_puuid(region,puuid)
    return matches

with open('summonerInfo.json', 'r') as f:
    summonersInfo = json.load(f)

matchesSet=set()
counter=0
for summonerID in summonersInfo:
    puuid=summonersInfo[summonerID]["puuid"]
    matchList=getMatches(regionMatches,puuid)
    print("Got matches of",puuid)
    for match in matchList:
        matchesSet.add(match)
    print("Matches Registered",matchesSet.__len__())
    time.sleep(1)
    if(counter==95 or counter==190):
        time.sleep(120)
    counter+=1

json_object = json.dumps(list(matchesSet), indent=4)

with open("matchesIDS.json", "w") as outfile:
    outfile.write(json_object)
