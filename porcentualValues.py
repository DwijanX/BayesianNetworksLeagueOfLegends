import pandas as pd

df = pd.read_csv('DataSetLeagueOfLegends1.csv')

#print(df)
def getBalanceTwoColumns(column1,column2,df):
    return df[column1]-df[column2]

totalData = 2865


damageDataFrame=pd.DataFrame()
damageDataFrame["win"]=df["win"]
#golddamageDataFrame["balanceGold"]=getBalanceTwoColumns("TeamBlueTopDamageDealt","TeamRedTopDamageDealt",df)
#damageDataFrame["balanceGold"]=getBalanceTwoColumns("TeamBlueTopGoldEarned","TeamRedTopGoldEarned",df)
damageDataFrame["probabilitiesTop"]=getBalanceTwoColumns("TeamBlueTopDamageDealt","TeamRedTopDamageDealt",df)
damageDataFrame["probabilitiesJg"]=getBalanceTwoColumns("TeamBlueJungleDamageDealt","TeamRedJungleDamageDealt",df)
damageDataFrame["probabilitiesMid"]=getBalanceTwoColumns("TeamBlueMidDamageDealt","TeamRedMidDamageDealt",df)
damageDataFrame["probabilitiesADC"]=getBalanceTwoColumns("TeamBlueADCDamageDealt","TeamRedADCDamageDealt",df)
damageDataFrame["probabilitiesSupp"]=getBalanceTwoColumns("TeamBlueSupportDamageDealt","TeamRedSupportDamageDealt",df)
print(damageDataFrame)
probabilitiedDF=pd.DataFrame()

redTopAdvantage=0
blueTopAdvantage=0

redJgAdvantage=0
blueJgAdvantage=0

redMidAdvantage=0
blueMidAdvantage=0

redADCAdvantage=0
blueADCAdvantage=0

redSuppAdvantage=0
blueSuppAdvantage=0

for index, row in damageDataFrame.iterrows():
    if row['probabilitiesTop'] > 0:
        blueTopAdvantage += 1
    else:
        redTopAdvantage += 1
            
    if row['probabilitiesJg'] > 0:
        blueJgAdvantage += 1
    else:
        redJgAdvantage += 1
            
    if row['probabilitiesMid'] > 0:
        blueMidAdvantage += 1
    else:
        redMidAdvantage += 1
            
    if row['probabilitiesADC'] > 0:
        blueADCAdvantage += 1
    else:
        redADCAdvantage += 1
            
    if row['probabilitiesSupp'] > 0:
        blueSuppAdvantage += 1
    else:
        redSuppAdvantage += 1

print("Red Top Advantage:", round(redTopAdvantage/totalData, 5))
print("Blue Top Advantage:", round(blueTopAdvantage/totalData, 5))

print("Red Jg Advantage:", round(redJgAdvantage/totalData, 5))
print("Blue Jg Advantage:", round(blueJgAdvantage/totalData, 5))

print("Red Mid Advantage:", round(redMidAdvantage/totalData, 5))
print("Blue Mid Advantage:", round(blueMidAdvantage/totalData, 5))

print("Red ADC Advantage:", round(redADCAdvantage/totalData, 5))
print("Blue ADC Advantage:", round(blueADCAdvantage/totalData, 5))

print("Red Supp Advantage:", round(redSuppAdvantage/totalData, 5))
print("Blue Supp Advantage:", round(blueSuppAdvantage/totalData, 5))