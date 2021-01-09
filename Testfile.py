import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
import mplcursors

def just_date(x):
    return x[0:10]

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure()

df = pd.read_csv("C:\\Users\\jakee\\Desktop\\Kovaaks\\1wall9000targets.csv")
df = df.reset_index()
df["Time"] = df["Time"].apply(just_date)
count = df.count
a = fig.add_subplot(111)
#dots = a.scatter(x=df["index"],y=df["Score"])
dots = a.scatter(x=df["Time"],y=df["Score"])
a.plot(df["index"],df["Score"])
a.grid()
a.tick_params(axis="x", direction="out", labelrotation=90, length=10)

canvas = FigureCanvasTkAgg(fig, master=root)

c1 = mplcursors.cursor(dots, hover=True)

canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()
    root.destroy()  

button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
