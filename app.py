from dash import Dash, html, dash_table, dcc, callback, State, Input, Output
from datetime import date
from dateutil.relativedelta import relativedelta

import plotly.express as px


from data import Naturalization

naturalization = Naturalization()
data = naturalization.get_amount_per_region(['westafrika'])
for key in data:
    df = data[key]

regions = naturalization.get_regions()
gender = naturalization.get_gender()

fig = px.line(df, x=df.index, y='gesamt', title='Naturalization in Westafrika')


app = Dash(__name__)

app.layout = html.Div([
    html.Div(children="Einbürgerung in Deutschland"),
    dcc.Graph(figure=fig, id='graph-naturalization'),
    dcc.Dropdown(gender, id='dropdown-gender'),
    dcc.Dropdown(regions, 0, id='dropdown-regions')
])


@callback(
    Output('graph-naturalization', 'figure'), 
    [Input('dropdown-regions', 'value'),
    Input('dropdown-gender', 'value')]
    )
def update_figure(region, gender):
    data = naturalization.get_amount_per_region([region], gender=gender)
    for key in data:
        df = data[key]
        fig = px.line(df, x=df.index, y='gesamt')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    