import pandas as pd
import json
data = pd.read_csv('DataSetLeagueOfLegends1.csv')

arr=['Top','Jungle','Mid','ADC','Support']
def getGoldBalance(position):
    bluePosGold=f'TeamBlue{position}GoldEarned'
    redPosGold=f'TeamRed{position}GoldEarned'
    return bluePosGold-redPosGold
    
df=pd.DataFrame()
for position in arr:
    df[f'GoldBalance{position}']=data.loc[:,f'TeamBlue{position}GoldEarned']-data.loc[:,f'TeamRed{position}GoldEarned']
for position in arr:
    df[f'DamageBalance{position}']=data.loc[:,f'TeamBlue{position}DamageDealt']-data.loc[:,f'TeamRed{position}DamageDealt']

dataToMergeWith = pd.read_csv('DataSetLeagueOfLegends2.csv')
YAxis=data.loc[:,"win"]
dataToMergeWith=dataToMergeWith.drop('win',axis=1)

headersToConcat = df.head() 
for header in headersToConcat:
    dataToMergeWith[header]=df.loc[:,header]
objToSave={'X':dataToMergeWith,'Y':YAxis}

dataToMergeWith.to_csv('XValuesDataSet.csv', index=False)
YAxis.to_csv('YValuesDataSet.csv', index=False)

"""
print(data)
bluePosDmg=f'TeamBlue{position}DamageDealt'
redPosDmg=f'TeamRed{position}DamageDealt'"""