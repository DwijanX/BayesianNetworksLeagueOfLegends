from apiConfig import api_key
from riotwatcher import LolWatcher, ApiError
import json
import pandas as pd

watcher = LolWatcher(api_key)
region = 'euw1'

with open('top200PlayersEUW.json', 'r') as f:
    playersWinrate = json.load(f)

with open('summonerInfo.json', 'r') as f:
    playersInfo = json.load(f)

with open('matchesData.json', 'r') as f:
    matchesData = json.load(f)

with open('champs.txt', 'r') as f:
    champions = f.readlines()

def getChampionNameAsNumber():
    champion_dict = {champion.strip().replace(" ","").lower(): i+1 for i, champion in enumerate(champions)}
    return champion_dict


def getDataFromSingularPlayer(playersWinrate, summoner_name):
    for entry in playersWinrate["entries"]:
        if entry["summonerName"] == summoner_name:
            return entry
    baseJson = {
        "wins": 100,
        "losses": 100,
        "leaguePoints": 1000
    }
    return baseJson

#print(getDataFromSingularPlayer(playersWinrate,'1OnczcyU0FCm7sGiGAozd5ANwpYB5Ce3_6QmR-YZlS_ITAQJs3hKsVYQaQ'))

def find_position_by_summoner_name(teamPosition):

    position_map = {
    'TOP': 'Top',
    'JUNGLE': 'Jungle',
    'MIDDLE': 'Mid',
    'BOTTOM': 'ADC',
    'UTILITY': 'Support'
    }
    standardized_position = position_map.get(teamPosition, teamPosition)
    return standardized_position


def create_dataframe():
    columns = ['TeamBlueTopGoldEarned', 'TeamBlueTopChampionName', 'TeamBlueTopDamageDealt', 'TeamBlueTopWins', 'TeamBlueTopLosses','TeamBlueTopLeaguePoints'
                ,'TeamRedTopGoldEarned', 'TeamRedTopChampionName', 'TeamRedTopDamageDealt', 'TeamRedTopWins', 'TeamRedTopLosses','TeamRedTopLeaguePoints'
                ,'TeamBlueJungleGoldEarned', 'TeamBlueJungleChampionName', 'TeamBlueJungleDamageDealt', 'TeamBlueJungleWins', 'TeamBlueJungleLosses', 'TeamBlueJungleLeaguePoints'
                ,'TeamRedJungleGoldEarned', 'TeamRedJungleChampionName', 'TeamRedJungleDamageDealt', 'TeamRedJungleWins', 'TeamRedJungleLosses', 'TeamRedJungleLeaguePoints'
                ,'TeamBlueMidGoldEarned', 'TeamBlueMidChampionName', 'TeamBlueMidDamageDealt', 'TeamBlueMidWins', 'TeamBlueMidLosses', 'TeamBlueMidLeaguePoints'
                ,'TeamRedMidGoldEarned', 'TeamRedMidChampionName', 'TeamRedMidDamageDealt', 'TeamRedMidWins', 'TeamRedMidLosses', 'TeamRedMidLeaguePoints'
                ,'TeamBlueADCGoldEarned', 'TeamBlueADCChampionName', 'TeamBlueADCDamageDealt', 'TeamBlueADCWins', 'TeamBlueADCLosses', 'TeamBlueADCLeaguePoints'
                ,'TeamRedADCGoldEarned', 'TeamRedADCChampionName', 'TeamRedADCDamageDealt', 'TeamRedADCWins', 'TeamRedADCLosses', 'TeamRedADCLeaguePoints'
                ,'TeamBlueSupportGoldEarned', 'TeamBlueSupportChampionName', 'TeamBlueSupportDamageDealt', 'TeamBlueSupportWins', 'TeamBlueSupportLosses', 'TeamBlueSupportLeaguePoints'
                ,'TeamRedSupportGoldEarned', 'TeamRedSupportChampionName', 'TeamRedSupportDamageDealt', 'TeamRedSupportWins', 'TeamRedSupportLosses', 'TeamRedSupportLeaguePoints'
                ,'win'
               ]
    df = pd.DataFrame(columns=columns)
    return df

def add_Player_to_Dataframe(df, participant, side, position, player_data, index, champion_number):
    #definimos columnas de database al player
    gold_col = f'Team{side}{position}GoldEarned'
    champ_col = f'Team{side}{position}ChampionName'
    damage_col = f'Team{side}{position}DamageDealt'
    wins_col = f'Team{side}{position}Wins'
    losses_col = f'Team{side}{position}Losses'
    lp_col = f'Team{side}{position}LeaguePoints'
    
    df.loc[index, gold_col] = participant['goldEarned']
    df.loc[index, champ_col] = champion_number[participant['championName'].lower()]
    df.loc[index, damage_col] = participant['totalDamageDealtToChampions']
    df.loc[index, wins_col] =  player_data['wins']
    df.loc[index, losses_col] =  player_data['losses']
    df.loc[index, lp_col] =  player_data['leaguePoints']

    return df

champion_number = getChampionNameAsNumber()
print(champion_number)
df = create_dataframe()
print(df)
player = 0
index = 0
for matchKey in matchesData:
    match= matchesData[matchKey]
    side = "Blue"
    player = 0
    
    for participant in match['info']['participants']:
            #conseguimos ID de matches para usarlo en summonerInfo y topPlayers
        summoner_name = participant["summonerName"]

        player_data = getDataFromSingularPlayer(playersWinrate, summoner_name)
        position = find_position_by_summoner_name(participant['teamPosition'])
        if(position == ''):
            break

        df = add_Player_to_Dataframe(df, participant, side, position, player_data, index, champion_number)

        player += 1
        if (player>=5):
            if(side =="Blue"):
                side ="Red"
            else:
                side ="Blue"
            player = 0
            
    if(position != ''):
        if (match['info']['teams'][0]['win'] == True):
            df.loc[index, 'win'] =  1
        else:
            df.loc[index, 'win'] =  0
        index += 1
    
    print(index)

# save DataFrame to a CSV file
df.to_csv('DataSetLeagueOfLegends.csv', index=False)

json_object = json.dumps(champion_number, indent=4)

with open("champion_number.json", "w") as outfile:
    outfile.write(json_object)