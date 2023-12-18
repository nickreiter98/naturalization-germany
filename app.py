from dash import Dash, html, dash_table, dcc, callback, State, Input, Output
from datetime import date
from dateutil.relativedelta import relativedelta

import plotly.express as px


from data import Naturalization

naturalization = Naturalization()
data = naturalization.get_amount_per_region(['westafrika'])

regions = naturalization.get_regions()
gender = naturalization.get_gender()

fig = px.line(data, x=data.index, y='westafrika')


app = Dash(__name__)

app.layout = html.Div([
    html.Div(children="Einbürgerung in Deutschland"),
    dcc.Graph(figure=fig, id='graph-naturalization'),
    dcc.Dropdown(gender, id='dropdown-gender'),
    dcc.Dropdown(regions, 0, id='dropdown-regions', multi=True),
    html.Button('Update', id='button-update', n_clicks=0),
])


@callback(
    Output('graph-naturalization', 'figure'), 
    Input('button-update', 'n_clicks'),
    [State('dropdown-regions', 'value'),
    State('dropdown-gender', 'value')],
    prevent_initial_call=True
    )
def update_figure(n_clicks, region, gender):
    data = naturalization.get_amount_per_region(region, gender=gender)
    fig = px.line(data, x=data.index, y=region)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    