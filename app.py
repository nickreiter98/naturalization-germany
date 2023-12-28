from dash import Dash, html, dash_table, dcc, callback, State, Input, Output
from datetime import date
from dateutil.relativedelta import relativedelta

import plotly.express as px

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from data import Naturalization

naturalization = Naturalization()

regions = naturalization.get_regions()
gender = naturalization.get_gender()
age = naturalization.get_age_classes()

load_figure_template('LUX')


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
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
                html.Button('Update', id='button-update-age', n_clicks=0)

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
                dcc.Graph(id='graph-age')
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

if __name__ == '__main__':
    app.run_server(debug=True)

    
    