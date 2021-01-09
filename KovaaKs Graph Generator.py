from tkinter import *
from tkinter import ttk
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

mypath = "C:\\Users\\jakee\\Desktop\\Kovaaks\\"

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

OPTIONS = onlyfiles
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("TEST :)")

        self.label = Label(master, text="This is our first GUI!")
        #self.label.pack()

        self.generate_button = Button(master, text="Generate", command=self.generate)
        #self.greet_button.pack()

        self.variable = StringVar(master)
        self.variable.set(OPTIONS[0])
        self.selection = ttk.Combobox(master, textvariable=self.variable, values=OPTIONS)
        #self.selection.pack()

        self.ok_button = Button(master, text="OK", command=self.ok)
        #self.ok_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        #self.close_button.pack()

        self.label.grid(columnspan=2, sticky=W)
        self.generate_button.grid(row=1)
        self.ok_button.grid(row=1, column=1)
        self.selection.grid(rowspan=2, row=1)
        self.close_button.grid(row=2, column=1)

    def generate(self):
        location = "C:\\Users\\jakee\\Desktop\\Kovaaks\\"
        file = self.variable.get()
        filepath = location + file
        df = pd.read_csv(filepath)
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df['Score'],
                        mode='lines+markers',
                        name='lines+markers'))
        fig.update_xaxes(rangeslider_visible=True)
        fig.show()

    def ok(self):
        print ("value is: " + self.variable.get())

root = Tk()
root.geometry("300x300")
my_gui = MyFirstGUI(root)
root.mainloop()
