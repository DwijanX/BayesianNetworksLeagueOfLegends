import pandas as pd

df = pd.read_csv('DataSetLeagueOfLegends1.csv')
def calculateWinsBalance(df):
    positions=["Top","Jungle","Mid","ADC","Support",]
    for position in positions:
        df[f'TeamBlue{position}winxWr']=df[f'TeamBlue{position}Wins']*df[f'TeamBlue{position}WinRate']-df[f'TeamBlue{position}Losses']*df[f'TeamBlue{position}WinRate']
        df[f'TeamRed{position}winxWr']=df[f'TeamRed{position}Wins']*df[f'TeamRed{position}WinRate']-df[f'TeamRed{position}Losses']*df[f'TeamRed{position}WinRate']
calculateWinsBalance(df)
print(df)
def getBalanceTwoColumns(column1,column2,df):
    return df[column1]-df[column2]

totalData = 2866
damageDataFrame=pd.DataFrame()
damageDataFrame["win"]=df["win"]

def sumToPositionSideIfPosOrNeg(balance,positionWinsList:list):

    if balance> 0:
        positionWinsList[0] += 1
    else:
        positionWinsList[1] += 1

def getProbabilitiesOfStats(stat,srcDf):
    statDataFrame=pd.DataFrame()
    positions=["Top","Jungle","Mid","ADC","Support",]

    statDataFrame["win"]=srcDf["win"]
    for position in positions:
        statDataFrame[f'balance{position}']=getBalanceTwoColumns(f'TeamBlue{position}{stat}',f'TeamRed{position}{stat}',srcDf)
    Sums={"Top":[0,0],"Jungle":[0,0],"Mid":[0,0],"ADC":[0,0],"Support":[0,0]}

    for index, row in statDataFrame.iterrows():
        sumToPositionSideIfPosOrNeg(row['balanceTop'],Sums["Top"])
        sumToPositionSideIfPosOrNeg(row['balanceJungle'],Sums["Jungle"])
        sumToPositionSideIfPosOrNeg(row['balanceMid'],Sums["Mid"])
        sumToPositionSideIfPosOrNeg(row['balanceADC'],Sums["ADC"])
        sumToPositionSideIfPosOrNeg(row['balanceSupport'],Sums["Support"])
    Probs={}
    for position in positions:
        Probs[position]=[round(Sums[position][0]/totalData, 5),round(Sums[position][1]/totalData, 5)]
    return Probs
#probGold=getProbabilitiesOfStats("GoldEarned",df)
#probDmg=getProbabilitiesOfStats("DamageDealt",df)

probWR=getProbabilitiesOfStats("winxWr",df)

print(probWR)