import pandas as pd
import datetime as dt

def insert_row(row_number, df, row_value): 
    start_upper = 0
    end_upper = row_number 
    start_lower = row_number 
    end_lower = df.shape[0] 
    upper_half = [*range(start_upper, end_upper, 1)] 
    lower_half = [*range(start_lower, end_lower, 1)] 
    lower_half = [x.__add__(1) for x in lower_half] 
    index_ = upper_half + lower_half 
    df.index = index_ 
    df.loc[row_number] = row_value 
    df = df.sort_index() 
    return df 

#'1wall 6targets small - Challenge - 2020.11.10-10.44.00 Stats.csv'
#'Tile Frenzy - Challenge - 2020.12.04-01.33.01 Stats.csv'
#'Ascended Tracking 90 - Challenge - 2020.11.27-00.44.16 Stats.csv'
csv = 'Ascended Tracking 90 - Challenge - 2020.11.27-00.44.16 Stats.csv'

df = pd.read_csv(csv, error_bad_lines=False)

dftop = df.iloc[:-26,:]
dfbot = df.iloc[-25:,:2]
dfbot.columns = ["CATEGORY","VALUE"]

toInsert = ["Shots:", df.at[len(df) - 26, "Timestamp"] ]
dfbot = insert_row(0, dfbot, toInsert)

toInsert = ["Hits:", df.at[len(df) - 26, "Bot"]]
dfbot = insert_row(1, dfbot, toInsert)

toInsert = ["Accuracy:", int(dfbot.at[1, "VALUE"]) / int(dfbot.at[0, "VALUE"])]
dfbot = insert_row(2, dfbot, toInsert)

toInsert = ["Damage Efficiency:", float(df.at[len(df) - 26, "Weapon"]) / float(df.at[len(df) - 26, "TTK"])]
dfbot = insert_row(3, dfbot, toInsert)

print(df.to_string())
print(dftop.to_string())
print()
print(dfbot.to_string())

#Series to put in Master
#Get date and time from filename
#'Ascended Tracking 90 - Challenge - 2020.11.27-00.44.16 Stats.csv'
strs = csv.split(" ")
dateNtime = strs[-2].split("-")
dateSplit = dateNtime[0].split(".")
timeSplit = dateNtime[1].split(".")
print(dateNtime)
print(timeSplit)
date = dt.datetime(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]), int(timeSplit[0]), int(timeSplit[1]), int(timeSplit[2]))
print(date)

dfMaster = dfbot.iloc[:16:, 1]
#toInsert = ["Date and Time:", date]
dfMaster = insert_row(0, dfMaster, date)

print(type(dfMaster))
print(dfMaster.to_string())

scenario = csv.split("-")[0].split(" ")[0]
for x in range(1,len(csv.split("-")[0].split(" "))-1):
    scenario = scenario + "_" + csv.split("-")[0].split(" ")[x]
print(scenario)
outputPath = "C:\\Users\\jakee\\Desktop\\Kovaaks\\" + scenario + ".csv"
print(outputPath)
dfbot.to_csv(path_or_buf= outputPath ,index=False)
#print(stats.head(5))