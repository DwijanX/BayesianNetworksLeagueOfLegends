from apiConfig import api_key
from riotwatcher import LolWatcher, ApiError
import pandas as pd

watcher = LolWatcher(api_key)
region = 'la1'
#Solo se puede hacer hasta 20 requests por segundo y 100 requests cada 2 minutos

def getSummonerInfoBySummonerName(SmmName,region):
    summonerData=watcher.summoner.by_name(region, SmmName)
    return summonerData

def getLastMatchesByPuuid(region,puuid):
    matches=watcher.match.matchlist_by_puuid(region,"JbBO0nxCXqBI86m1yqpd-rBkGv7Y5k-n6Qirky8kTtrzD_90V6VuTqiSLD1PHo1JjESOC49ApD67Cw")
    return matches
def getMatchInfo(region,matchID):
    matchInfo=watcher.match.by_id(region,"LA1_1379648863")
    return matchInfo