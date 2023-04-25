import pandas as pd
import itertools

df = pd.read_csv('DataSetLeagueOfLegends1.csv')
def calculateWinsBalance(df):
    positions=["Top","Jungle","Mid","ADC","Support",]
    for position in positions:
        df[f'TeamBlue{position}winxWr']=df[f'TeamBlue{position}Wins']*df[f'TeamBlue{position}WinRate']-df[f'TeamBlue{position}Losses']*df[f'TeamBlue{position}WinRate']
        df[f'TeamRed{position}winxWr']=df[f'TeamRed{position}Wins']*df[f'TeamRed{position}WinRate']-df[f'TeamRed{position}Losses']*df[f'TeamRed{position}WinRate']
calculateWinsBalance(df)

def getBalanceTwoColumns(column1,column2,df):
    return df[column1]-df[column2]

totalData = 2866


def sumToPositionSideIfPosOrNeg(balance,positionWinsList:list):

    if balance> 0:
        positionWinsList[1] += 1
    else:
        positionWinsList[0] += 1

def getProbabilitiesOfStats(stat,srcDf,statDataFrame):
    positions=["Top","Jungle","Mid","ADC","Support",]
    for position in positions:
        statDataFrame[f'balance{position}{stat}']=getBalanceTwoColumns(f'TeamBlue{position}{stat}',f'TeamRed{position}{stat}',srcDf)
    Sums={"Top":[0,0],"Jungle":[0,0],"Mid":[0,0],"ADC":[0,0],"Support":[0,0]}

    for index, row in statDataFrame.iterrows():
        sumToPositionSideIfPosOrNeg(row[f'balanceTop{stat}'],Sums["Top"])
        sumToPositionSideIfPosOrNeg(row[f'balanceJungle{stat}'],Sums["Jungle"])
        sumToPositionSideIfPosOrNeg(row[f'balanceMid{stat}'],Sums["Mid"])
        sumToPositionSideIfPosOrNeg(row[f'balanceADC{stat}'],Sums["ADC"])
        sumToPositionSideIfPosOrNeg(row[f'balanceSupport{stat}'],Sums["Support"])
    Probs={}
    for position in positions:
        Probs[position]=[round(Sums[position][0]/totalData, 5),round(Sums[position][1]/totalData, 5)]
    return Probs

resultDataFrame=pd.DataFrame()
resultDataFrame["win"]=df["win"]
def createCombinationOfTrueFalse(nStates):
    states=[True,False]
    labels=[]
    for combination in itertools.product("TF", repeat=nStates):
        labels.append("".join(combination))
    return labels
def returnBoolForPosNegativeNumbers(number):
    if number>0:
        return "T"
    else:
        return "F"
def calculateProbsForComplexDF(df,stat):
    positions=["Top","Jungle","Mid","ADC","Support",]
    labels=createCombinationOfTrueFalse(5)
    stats={}
    for label in labels:
        stats[label]=0
    for index, row in df.iterrows():
        key=""
        for position in positions:
            key+=returnBoolForPosNegativeNumbers(row[f'balance{position}{stat}'])
        stats[key]+=1
    return stats
def calculateProbForGoldDmgWr(df):
    labels=createCombinationOfTrueFalse(4)
    stats={}
    for label in labels:
        stats[label]=0
    for index, row in df.iterrows():
        key=""
        if row["totalBalanceGoldEarned"]>0:key+="T" 
        else: key+="F"
        if row["totalBalanceDamageDealt"]>0:key+="T" 
        else: key+="F"
        if row["totalBalancewinxWr"]>0:key+="T" 
        else: key+="F"
        if row["win"]==1:key+="T" 
        else: key+="F"
        stats[key]+=1
    return stats
def calculateTeamBalance(stat,df:pd.DataFrame):
    df[f'totalBalance{stat}']=df[f'balanceTop{stat}']+df[f'balanceMid{stat}']+df[f'balanceJungle{stat}']+df[f'balanceADC{stat}']+df[f'balanceSupport{stat}']
    df.drop([f'balanceTop{stat}',f'balanceMid{stat}',f'balanceJungle{stat}',f'balanceADC{stat}',f'balanceSupport{stat}'], inplace=True,axis=1)

ProbGold=getProbabilitiesOfStats("GoldEarned",df,resultDataFrame)
probDmg=getProbabilitiesOfStats("DamageDealt",df,resultDataFrame)
probWR=getProbabilitiesOfStats("winxWr",df,resultDataFrame)
calculateTeamBalance('GoldEarned',resultDataFrame)
calculateTeamBalance('DamageDealt',resultDataFrame)
calculateTeamBalance('winxWr',resultDataFrame)
probs=calculateProbForGoldDmgWr(resultDataFrame)
print(probs)
testSeries=pd.Series(probs)
print((testSeries/totalData))
#print(ProbGold)
#statsGold=calculateProbsForComplexDF(resultDataFrame,'winxWr')
#print(statsGold.values())

#testSeries=pd.Series(statsGold)
#print((testSeries/totalData))