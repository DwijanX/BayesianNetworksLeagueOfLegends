from apiConfig import api_key
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import json
import time

watcher = LolWatcher(api_key)
region = 'EUW1'

def getPUUIDPerPlayer(region,id):
    puuid = watcher.summoner.by_id(region,id)
    return puuid

with open('top200PlayersEUW.json', 'r') as f:
    top200PlayersEUW = json.load(f)

print(top200PlayersEUW["entries"][0]["summonerId"])

summonerInfo ={}
counter=0
for player in top200PlayersEUW["entries"]:
    summonerInfoRetrieved=getPUUIDPerPlayer(region, player["summonerId"])
    print("got ",summonerInfoRetrieved["name"])
    summonerInfo[player["summonerId"]]=summonerInfoRetrieved
    time.sleep(1)
    if(counter==98 or counter==196):
        time.sleep(120)
    counter+=1


json_object = json.dumps(summonerInfo, indent=4)

with open("summonerInfo.json", "w") as outfile:
    outfile.write(json_object)