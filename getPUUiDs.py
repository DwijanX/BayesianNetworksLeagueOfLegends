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

summonersPUUID = []

for player in top200PlayersEUW["entries"]:
   summonersPUUID.append(getPUUIDPerPlayer(region, player["summonerId"]))
   time.sleep(10)

with open('summonersPUUID.json', 'w') as f:
   json.dump(summonersPUUID, f)