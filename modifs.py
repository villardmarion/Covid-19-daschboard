# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import dash_bio as dashbio

# import warnings
# from six import PY3

app = dash.Dash('Covid')

covid_monde_url = (
    "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    )

covid_monde = pd.read_csv(covid_monde_url, sep=";", parse_dates=True, index_col=2,encoding= 'utf-8')
covid_monde.sort_index(inplace=True)

covid_url = (
    "https://www.data.gouv.fr/fr/datasets/r/900da9b0-8987-4ba7-b117-7aea0e53f530"
)

df = pd.read_csv(covid_url, sep=";", parse_dates=True, index_col=2,encoding= 'utf-8')
df.sort_index(inplace=True)

# warnings.filterwarnings("ignore")
data = df

app.layout = html.Div(children=[
    dcc.Tabs([
        dcc.Tab(label='Situation dans le monde', children=[
            html.Div([
                dashbio.AlignmentChart(
                    id='my-alignment-viewer',
                    data=data),
                html.Div(id='alignement-viewver-output')
                ]),

            html.Div([
                html.H1('Covid19 Dashboard'),
                dcc.Dropdown(
                    id='dropdown1',
                    options=[
                    {'label':'France', 'value': '[3,1,3]'},
                    {'label': 'India', 'value': '[5,15,3]'},
                    {'label': 'USA', 'value': '[3,15,3]'}
                    ],
                    value='[3,1,3]'
                    ),
                dcc.Graph(id='graph1')
                ])]),
        dcc.Tab(label='Situation globale en France'),
        dcc.Tab(label='Les réanimations'),
        dcc.Tab(label='Les décès'),
        dcc.Tab(label='La vaccination')
        ])
    ])

@app.callback(
    Output('graph1', 'figure'),
    [Input('dropdown1', 'value')])
def update_graph(new_dropdown_value):
    return {
        'data': [{
            'x': [1, 3, 3],
            'y': eval(new_dropdown_value)
        }]
    }

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8080)
