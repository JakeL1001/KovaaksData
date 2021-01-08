import pandas as pd
import datetime as dt
import os.path

csvRetry = "None"                                                                                   # Used to reattempt the failed opening of a csv file
counter = 0                                                                                         # Counter to ensure no infinite looping in reattempted openings

print("Running...")
def insert_row(row_number, df, row_value):                                                          # Function to insert rows into specific locations in a dataframe
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

path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\FPSAimTrainer\\FPSAimTrainer\\stats"     # Path storing the scenario files, must be customizable in GUI
with os.scandir(path) as it:
    for entry in it:                                                                                # Loops through all scenario files in the folder
        try:
            if entry.name.endswith(".csv") and entry.is_file():                                     # Checks that the current item is a csv file, and if so, adds the filename to the path
                if (csvRetry != "None"):                                                            # If the previous file failed, it will attempt to open it again
                    csv = csvRetry
                else:
                    csv = path + "\\" + entry.name

                #print(csv)
                df = pd.read_csv(csv, error_bad_lines=False, header=None, usecols=[0,1,2,3,4])      # Reads the scenario csv into the dataframe
                df = df.tail(31)                                                                    # Retreiving only important data
                df = df.reset_index(drop=True)

                complete = 0
                while(complete == 0):                                                               # Removes the first line until usuable data is reached, as different scenarios
                    try:                                                                            # can have different weapons, which are not used, which can misshape the data
                        int(df.at[0, 1])
                        complete = 1
                    except ValueError:
                        df = df.drop(0)
                    except KeyError:
                        df = df.drop(0)
                    df = df.reset_index(drop=True)

                if (int(df.at[0, 1]) == 0):                                                         # If the first weapon listed is not used, it will have 0 shots fired, so it is dropped
                    df = df.drop(0)
                    df = df.reset_index(drop=True)

                Shots = df[1].iloc[0]                                                               # Saves poorly formatted data before dropping unneccesary columns
                Hits = df[2].iloc[0]
                damageDone = df[3].iloc[0]
                damagePossible = df[4].iloc[0]
                df = df.drop(columns=[2,3,4])
                df.columns = ["CATEGORY","VALUE"]                                                   # Formats the important data into 2 columns
                df = df.drop(1, axis=0)

                df['CATEGORY'] = df['CATEGORY'].str.replace(":", '')

                toInsert = ["Shots", Shots]                                                        # Inserts the Shots taken, Shots hit, and calculates the accuracy
                df = insert_row(0, df, toInsert)

                toInsert = ["Hits", Hits]
                df = insert_row(1, df, toInsert)

                toInsert = ["Accuracy", int(Hits) / int(Shots)]
                df = insert_row(2, df, toInsert)

                if (float(damageDone) == 0 and float(damagePossible) == 0):                         # Calculates the Damage Efficiency if the scenario records damage 
                    toInsert = ["Damage Efficiency", "Data not recorded"]
                else:
                    toInsert = ["Damage Efficiency", float(damageDone) / float(damagePossible)]
                df = insert_row(3, df, toInsert)

                strs = csv.split(" ")                                                               # Splits up the csv file name so the date and time can be accessed and recorded
                dateNtime = strs[-2].split("-")
                dateSplit = dateNtime[0].split(".")
                timeSplit = dateNtime[1].split(".")
                date = dt.datetime(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]), int(timeSplit[0]), int(timeSplit[1]), int(timeSplit[2]))

                dateInsert = ["Time", date]                                                        # Inserts the date and time into the df
                df = insert_row(0, df, dateInsert)
                try:
                    df.iloc[33]
                    df = df.head(30)
                    #print(df.to_string())
                except IndexError:
                    pass
                dfReady = df.set_index('CATEGORY').T


                scenario = entry.name.split("-")[0].split(" ")[0]                                   # Creates the name of the file to be created 
                for x in range(1,len(entry.name.split("-")[0].split(" "))-1):
                    scenario = scenario + "_" + entry.name.split("-")[0].split(" ")[x]

                outputPath = "C:\\Users\\jakee\\Desktop\\Kovaaks\\" + scenario + ".csv"             # Output path of the final csv for each scenario - MAKE CUSTOMIZABLE

                if os.path.isfile(outputPath):                                                      # Checks if file already exists, if it doesn't include the header, if it does, just append
                    dfReady.to_csv(path_or_buf= outputPath, mode='a' ,index=False, header=False)
                else:
                    dfReady.to_csv(path_or_buf= outputPath, mode='a' ,index=False)

            csvRetry = "None"                                                                       # Resets the reattempt mechanism and the counter, so when the file opens successfully
            counter = 1                                                                             # The loop is prepared for a failure of a different file

        except IOError:                                                                             # If the file fails to open, it retrys the same file until it opens correctly, or
            print("FAILED =", csv)                                                                  # Fails 500 times (I had up to 120 failures if the file was open on my PC before it
            print("Retrying... |", counter, "attempts")                                             # Successfully opened
            counter += 1
            if (counter >= 500):                                                                    # Exit failure if the file cannot be opened 500 times
                print("too many failures")
                exit(1)
            csvRetry = csv

print("Complete :)")
