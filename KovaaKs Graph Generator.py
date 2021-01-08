import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

templocation = "C:\\Users\\jakee\\Desktop\\Kovaaks\\"
tempinput = "Cata_IC_Long_Strafes.csv"

scenario = templocation + tempinput
print(scenario)


thing = "C:\\Users\\jakee\\Desktop\\Kovaaks\\gp_far_long_strafes.csv"
thing = scenario
#thing = input("pog")
def create_graph(filepath):
    df = pd.read_csv(filepath)
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['Score'],
                        mode='lines+markers',
                        name='lines+markers'))
    fig.update_xaxes(rangeslider_visible=True)
    fig.show()
create_graph(thing)

