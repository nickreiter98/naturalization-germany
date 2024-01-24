from dash import Dash, html, dash_table, dcc, callback, State, Input, Output
from datetime import date
from dateutil.relativedelta import relativedelta

import plotly.express as px

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from data import Naturalization

import graphics
import os

naturalization = Naturalization()

regions = naturalization.get_regions()
gender = naturalization.get_gender()
age = naturalization.get_age_classes()
years = naturalization.get_years()

data_population_pyramid = naturalization.get_data_population_pyramid('europa', 2020)
population_pyramid = graphics.get_graph_population_pyramid(data_population_pyramid)

heatmap = []
for i in ['männlich', 'weiblich']:
    data_heatmap = naturalization.get_data_heatmap('europa', i)
    graph_heatmap = graphics.get_graph_heatmap(data_heatmap)
    heatmap.append(dcc.Graph(figure=graph_heatmap, id = 'heatmap-'+i))

load_figure_template('LUX')


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}


sidebar = html.Div(
    [
        html.H2("Filterauswahl"),
        html.Hr(),
        dbc.Nav(
            [
                html.H3('Figure 1'),
                dcc.Dropdown(gender, 'insgesamt', id='dropdown-gender-region'),
                html.Br(),
                dcc.Dropdown(regions, ['europa'], id='dropdown-regions-region', multi=True),
                html.Br(),
                html.Button('Update', id='button-update-region', n_clicks=0),
                html.Br(),
                html.Hr(),
                html.H3('Figure 2'),
                dcc.Dropdown(age, ['5_bis_unter_10_jahre'], id='dropdown-age-age', multi=True),
                html.Br(),
                dcc.Dropdown(gender, ['insgesamt'], id='dropdown-gender-age', multi=True),
                html.Br(),
                dcc.Dropdown(regions, 'europa', id='dropdown-regions-age'),
                html.Br(),
                html.Button('Update', id='button-update-age', n_clicks=0),
                html.Br(),
                html.Hr(),
                html.H3('Figure 3'),
                dcc.Dropdown(years, 2020, id='dropdown-year-pyramid'),
                html.Br(),
                dcc.Dropdown(regions, 'europa', id='dropdown-regions-pyramid'),
                html.Br(),
                html.Button('Update', id='button-update-pyramid', n_clicks=0),
                html.Br(),
                html.Hr(),
                html.H3('Figure 4'),
                html.Br(),
                dcc.Dropdown(regions, 'europa', id='dropdown-regions-heatmap'),


            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


app = Dash(external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div([
    dbc.Row(
            [dbc.Col(sidebar),
            dbc.Col(html.Div([
                dcc.Graph(id='graph-region'),
                dcc.Graph(id='graph-age'),
                dcc.Graph(figure = population_pyramid, id= 'figure-population-pyramid'),
                html.Div(id='heatmap-marital-status', children=heatmap)
            ]), width = 9, style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px'})
            ]
    )
])



@callback(
    Output('graph-region', 'figure'), 
    Input('button-update-region', 'n_clicks'),
    [State('dropdown-regions-region', 'value'),
    State('dropdown-gender-region', 'value'),],
    )
def update_figure_region(n_clicks, regions, genders):
    data = naturalization.get_amount_per_region(regions, gender=genders)
    fig = px.line(data, x=data.index, y=regions)
    return fig

@callback(
    Output('graph-age', 'figure'), 
    Input('button-update-age', 'n_clicks'),
    [State('dropdown-regions-age', 'value'),
    State('dropdown-gender-age', 'value'),
    State('dropdown-age-age', 'value')],
    )
def update_figure_age(n_clicks, region, genders, ages):
    print((region, gender, ages))
    data, columns = naturalization.get_amount_per_age_class(region, genders, ages)
    fig = px.line(data, x=data.index, y=columns)
    return fig

@callback(
    Output('figure-population-pyramid', 'figure'), 
    Input('button-update-pyramid', 'n_clicks'),
    [State('dropdown-regions-pyramid', 'value'),
    State('dropdown-year-pyramid', 'value')],
    )
def update_figure_pyramid(n_clicks, region, year):
    data = naturalization.get_data_population_pyramid(region, year)
    fig = graphics.get_graph_population_pyramid(data)
    return fig

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)

    
    