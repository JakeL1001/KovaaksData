# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
#from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
import numpy as np
import mplcursors
import matplotlib.animation as animation
import datetime as dt
import os.path
import time # REMOVE LATER ################################################################

import warnings
warnings.simplefilter('ignore', np.RankWarning)

from os import listdir
from os.path import isfile, join
mypath = "C:\\Users\\jakee\\Desktop"#\\Kovaaks\\"
OPTIONS = [f for f in listdir(mypath) if isfile(join(mypath, f))]

LARGE_FONT= ("Verdana", 12)
selection = OPTIONS[0]
scenariolocation = "LOCATION NOT ENTERED" 

fig = Figure()
a = fig.add_subplot(111)

def graph_it(yaxis):
    a.cla()
    df = pd.read_csv(mypath + selection).reset_index()
    dots = a.scatter(x=df["Time"],y=df[yaxis])
    dotsfake = a.scatter(x=df["Time"],y=df[yaxis])
    a.plot(df["Time"],df[yaxis], color="blue")
    items = df[yaxis].to_numpy()
    numitems = np.arange(1, len(items)+1, 1)
    m,b = np.polyfit(numitems, items, 1)
    a.plot(numitems,m*numitems + b, color="green")
    a.set_title("\"" + selection + "\"" + " Scores")
    a.grid()
    fig.autofmt_xdate()
    a.format_coord = lambda x,y: f"x={x:.0f}, y={y:.2f}" ###########################################################
    c1 = mplcursors.cursor(dots, hover=True)
    @c1.connect("add")
    def _(sel):
        sel.annotation.get_bbox_patch().set(fc="white")
        sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white")
    return [dotsfake]



class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs,)

        #tk.Tk.iconbitmap(self, default="D:\Downloads\o1fYFR7.png")
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.graph_button = ttk.Button(self, text="Graph", command=lambda: controller.show_frame(PageThree))
        self.graph_button.pack()
        
        self.PageOneButton = ttk.Button(self, text="Compile", command=lambda: controller.show_frame(PageOne))
        self.PageOneButton.pack()

        self.close_button = ttk.Button(self, text="Close", command=self.quit)
        self.close_button.pack()
"""
        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
"""

class PageOne(tk.Frame):    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Select Scenario Folder", command=self.browseFiles)
        button2.pack()

        button3 = ttk.Button(self, text="Select Output Folder", command=self.outputFiles)
        button3.pack()

        button4 = ttk.Button(self, text="Compile Scores", command=self.CompileScores)
        button4.pack()

    def outputFiles(self):
        global mypath
        mypath = tk.filedialog.askdirectory()
        mypath = mypath.replace("/","\\") + "\\"
        print(mypath)

    def browseFiles(self):
        global scenariolocation
        filename = tk.filedialog.askdirectory()
        scenariolocation = filename.replace("/","\\")
        #filename = filename.replace(" ","")
        print(scenariolocation)

    def CompileScores(self):
        start = time.time()

        csvRetry = "None"                                                                                   # Used to reattempt the failed opening of a csv file
        counter = 0                                                                                         # Counter to ensure no infinite looping in reattempted openings
        indexerrors = 0
        processed = 0

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

        path = scenariolocation #"C:\\Program Files (x86)\\Steam\\steamapps\\common\\FPSAimTrainer\\FPSAimTrainer\\stats"     # Path storing the scenario files, must be customizable in GUI
        with os.scandir(path) as it:
            for entry in it:
                exitcond = False
                scenario = entry.name.split("-")[0].split(" ")[0]                                   # Creates the name of the file to be created 
                for x in range(1,len(entry.name.split("-")[0].split(" "))-1):
                    scenario = scenario + "_" + entry.name.split("-")[0].split(" ")[x]

                outputPath = "C:\\Users\\jakee\\Desktop\\Kovaaks\\" + scenario + ".csv"             # Output path of the final csv for each scenario - MAKE CUSTOMIZABLE                                                                                # Loops through all scenario files in the folder
                try:
                    if entry.name.endswith(".csv") and entry.is_file():                                     # Checks that the current item is a csv file, and if so, adds the filename to the path
                        if (csvRetry != "None"):                                                            # If the previous file failed, it will attempt to open it again
                            csv = csvRetry
                        else:
                            csv = path + "\\" + entry.name

                        df = pd.read_csv(csv, error_bad_lines=False, header=None, usecols=[0,1,2,3,4])      # Reads the scenario csv into the dataframe
                        #df = df.tail(31)                                                                    # Retreiving only important data
                        for x in range(0, len(df.index)):
                            if (df.iloc[x,0] == "Weapon"):
                                useless = x
                                continue
                        df = df.tail(len(df.index) - useless)
                        df = df.reset_index(drop=True)

                        for x in range(0, len(df.index)):
                            if (df.iloc[x,0] == "Kills:"):
                                numWeaps = x-1
                                continue

                        strs = csv.split(" ")                                                               # Splits up the csv file name so the date and time can be accessed and recorded
                        dateNtime = strs[-2].split("-")
                        dateSplit = dateNtime[0].split(".")
                        timeSplit = dateNtime[1].split(".")
                        date = dt.datetime(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]), int(timeSplit[0]), int(timeSplit[1]), int(timeSplit[2]))
                        try:
                            df2 = pd.read_csv(outputPath, error_bad_lines=False, warn_bad_lines=False)
                            df2 = df2.reset_index(drop=True)
                            for x in range(0, len(df2.index)):
                                try:
                                    if(str(date) == df2.iloc[x,0]):
                                        processed += 1
                                        exitcond = True
                                        break
                                except IndexError:
                                    indexerrors += 1
                                    pass
                        except IOError:
                            #print("IOERROR")
                            pass

                        if(exitcond == True):
                            #print("continue")
                            continue

                        def findStats(stat, column):
                            for x in range(0, len(df.index)):
                                if (df[column].iloc[x] == stat):
                                    #print(df[column].iloc[x])
                                    total = 0
                                    for y in range(0, numWeaps):
                                        total += float(df[column].iloc[x+1+y])
                                    return total
                        
                        Shots = findStats("Shots", 1)
                        Hits = findStats("Hits", 2)
                        damageDone = findStats("Damage Done", 3)
                        damagePossible = findStats("Damage Possible", 4)

                        df = df.tail(len(df.index) - (numWeaps + 1))
                        df = df.drop(columns=[2,3,4])
                        df.columns = ["CATEGORY","VALUE"]                                                   # Formats the important data into 2 columns

                        df['CATEGORY'] = df['CATEGORY'].str.replace(":", '')

                        toInsert = ["Shots", Shots]                                                        # Inserts the Shots taken, Shots hit, and calculates the accuracy
                        df = insert_row(0, df, toInsert)

                        toInsert = ["Hits", Hits]
                        df = insert_row(1, df, toInsert)

                        try:
                            toInsert = ["Accuracy", int(Hits) / int(Shots)]
                            df = insert_row(2, df, toInsert)
                        except ZeroDivisionError:
                            df = insert_row(2, df, 0)
                            
                        if (float(damageDone) == 0 and float(damagePossible) == 0):                         # Calculates the Damage Efficiency if the scenario records damage 
                            toInsert = ["Damage Efficiency", "Data not recorded"]
                        else:
                            toInsert = ["Damage Efficiency", float(damageDone) / float(damagePossible)]
                        df = insert_row(3, df, toInsert)

                        dateInsert = ["Time", date]                                                        # Inserts the date and time into the df
                        df = insert_row(0, df, dateInsert)
                        try:
                            df.iloc[33]
                            df = df.head(30)
                        except IndexError:
                            pass
                        dfReady = df.set_index('CATEGORY').T

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

            end = time.time()
            timetaken = end - start
            print("Complete :) | Time Taken: " + str(round(timetaken,2)), "seconds | index errors: ", indexerrors, "| Already processed: ", processed)



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        self.button1.pack()

        self.button2 = ttk.Button(self, text="Drop Down Box", command=self.combobox)
        self.button2.pack()

        self.button3 = ttk.Button(self, text="Y Axis", command=self.combobox2)
        self.button3.pack()

        self.ok_button = ttk.Button(self, text="OK", command=self.ok)
        self.ok_button.pack()

        canvas = FigureCanvasTkAgg(fig, self)

        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def combobox(self):
        global OPTIONS
        global selection
        OPTIONS = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        selection = OPTIONS[0]
        self.button2.pack_forget()
        #self.selectionbox.pack_forget()
        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.selectionbox = ttk.Combobox(self, textvariable=self.variable, values=OPTIONS)
        self.selectionbox.pack()

    def combobox2(self):
        YaxisOptions = ["Score", "Hits", "Accuracy", "Damage Efficiency", "Kills", "Damage Done"]
        self.button3.pack_forget()
        self.variable2 = tk.StringVar(self)
        self.variable2.set(YaxisOptions[0])
        self.selectionbox2 = ttk.Combobox(self, textvariable=self.variable2, values=YaxisOptions)
        self.selectionbox2.pack()

    def ok(self):
        print("value is: " + self.variable.get())
        global selection
        selection = self.variable.get()
        yaxis = self.variable2.get()
        #print("YAXIS :", yaxis, type(yaxis))
        ani = animation.FuncAnimation(fig, graph_it,blit=True)
        fig.canvas.draw()
        ani.event_source.stop()

app = SeaofBTCapp()
app.geometry("800x800")
app.mainloop()
        