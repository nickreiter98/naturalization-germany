import pandas as pd
import plotly.graph_objs as go
import numpy as np
from dash import dcc
import plotly.express as px


def get_graph_population_pyramid(data):

    women_bins = np.array(data[1])*-1
    men_bins = np.array(data[0])

    y = list(range(0, 100, 5))

    layout = go.Layout(yaxis=go.layout.YAxis(title='Age'),
                    xaxis=go.layout.XAxis(title='Number'),
                    barmode='overlay',
                    bargap=0.1)

    data = [go.Bar(y=y,
                x=men_bins,
                orientation='h',
                name='Men',
                hoverinfo='x',
                text=men_bins.astype('int'),
                marker=dict(color='#AC3E31')
                ),
            go.Bar(y=y,
                x=women_bins,
                orientation='h',
                name='Women',
                text=-1 * women_bins.astype('int'),
                hoverinfo='text',
                marker=dict(color='#202020')
                )]

    return go.Figure(data=data, layout=layout)


def get_graph_heatmap(data):


    fig = px.imshow(data,
            labels=dict(x="Familienstand", y="Jahr", color="Einbürgerungen"),
            x=data.columns,
            y=data.index
        )
    fig.update_xaxes(side="top")
    return fig
    









