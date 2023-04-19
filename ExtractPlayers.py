from apiConfig import api_key
from riotwatcher import LolWatcher, ApiError
import json
 
watcher = LolWatcher(api_key)
region = 'euw1'

players=watcher.league.challenger_by_queue(region,"RANKED_SOLO_5x5")
json_object = json.dumps(players, indent=4)

with open("top200PlayersEUW.json", "w") as outfile:
    outfile.write(json_object)