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

import warnings
warnings.simplefilter('ignore', np.RankWarning)

from os import listdir
from os.path import isfile, join
mypath = "C:\\Users\\jakee\\Desktop\\Kovaaks\\"
OPTIONS = [f for f in listdir(mypath) if isfile(join(mypath, f))]

LARGE_FONT= ("Verdana", 12)
#csv = "C:\\Users\\jakee\\Desktop\\Kovaaks\\gp_far_long_strafes.csv"
selection = OPTIONS[0]

fig = Figure()
a = fig.add_subplot(111)
a.grid()
#df = pd.read_csv(mypath + selection).reset_index()
#a = fig.add_subplot(111)
#dots = a.scatter(x=df["Time"],y=df["Score"])

def graphIt(i):
    a.cla()
    df = pd.read_csv(mypath + selection).reset_index()
    dots = a.scatter(x=df["Time"],y=df["Score"])
    a.plot(df["Time"],df["Score"], color="blue")
    a.tick_params(axis="x", direction="out", labelrotation=90, length=1)
    items = df["Score"].to_numpy()
    numItems = np.arange(1, len(items)+1, 1)
    m,b = np.polyfit(numItems, items, 1)
    a.plot(numItems,m*numItems + b, color="green")
    a.set_title("\"" + selection + "\"" + " Scores")
    return [dots]

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

        #self.title("TEST :)")

        #self.label = Label(self, text="This is our first GUI!")
        #self.label.pack()

        self.graph_button = ttk.Button(self, text="Graph", command=lambda: controller.show_frame(PageThree))
        self.graph_button.pack()

        #animation.FuncAnimation(fig, graphIt, interval=10000)

        self.close_button = ttk.Button(self, text="Close", command=self.quit)
        self.close_button.pack()
"""
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()"""


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


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

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        #self.refresh_button = ttk.Button(self, text="refresh", command=self.generate)
        #self.refresh_button.pack()

        self.variable = tk.StringVar(self)
        self.variable.set(OPTIONS[0])
        self.selection = ttk.Combobox(self, textvariable=self.variable, values=OPTIONS)
        self.selection.pack()

        self.ok_button = ttk.Button(self, text="OK", command=self.ok)
        self.ok_button.pack()


        canvas = FigureCanvasTkAgg(fig, self)

        #c1 = mplcursors.cursor(dots, hover=True)

        canvas.draw()
        #canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
    def ok(self):
        print("value is: " + self.variable.get())
        global selection
        selection = self.variable.get()
        ani = animation.FuncAnimation(fig, graphIt,blit=True)
        #ani.event_source.start()
        fig.canvas.draw()
        #ani.event_source.stop()

app = SeaofBTCapp()
app.geometry("1600x800")
#ani = animation.FuncAnimation(fig, graphIt, interval=1000)
app.mainloop()
        