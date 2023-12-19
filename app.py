from dash import Dash, html, dash_table, dcc, callback, State, Input, Output
from datetime import date
from dateutil.relativedelta import relativedelta

import plotly.express as px


from data import Naturalization

naturalization = Naturalization()

regions = naturalization.get_regions()
gender = naturalization.get_gender()
age = naturalization.get_age_classes()


app = Dash(__name__)

app.layout = html.Div([
    html.Div(children="Einbürgerung in Deutschland nach Ländern"),
    dcc.Graph(id='graph-region'),
    dcc.Dropdown(gender, 'insgesamt', id='dropdown-gender-region'),
    dcc.Dropdown(regions, ['europa'], id='dropdown-regions-region', multi=True),
    html.Button('Update', id='button-update-region', n_clicks=0),

    html.Div(children="Einbürgerung in Deutschland nach Land und Altersklassen"),
    dcc.Graph(id='graph-age'),
    dcc.Dropdown(age, ['5_bis_unter_10_jahre'], id='dropdown-age-age', multi=True),
    dcc.Dropdown(gender, ['insgesamt'], id='dropdown-gender-age', multi=True),
    dcc.Dropdown(regions, 'europa', id='dropdown-regions-age'),
    html.Button('Update', id='button-update-age', n_clicks=0),
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
    