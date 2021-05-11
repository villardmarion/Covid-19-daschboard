# -*- coding: utf-8 -*-
"""
Created on Sun May  9 15:55:59 2021

@author: Naima
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime

#import warnings
#from six import PY3
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_colors = {
    'background': '#f2ffff',
    'text': '#101b32',
    'grid': '#333333',
    'red': '#BF0010',
    'blue': '#809cd5',
    'green': '#46c299'
}

covid_monde_url = ("https://covid19.who.int/WHO-COVID-19-global-data.csv")


covid_url = (
    "https://www.data.gouv.fr/fr/datasets/r/900da9b0-8987-4ba7-b117-7aea0e53f530"
)
def dataload(data):
    pd.read_csv(data, sep=",") 


#warnings.filterwarnings("ignore")

#données OMS
data =dataload(covid_monde_url)

data_columns = ['Date_reported','Country_code','Country','WHO_region','New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']

df= pd.DataFrame(data, columns =data_columns)
df['date'] = pd.to_datetime(df['Date_reported'])
#données france: vaccins
data_fr = dataload(covid_url)

data_fr_columns = ['reg', 'vaccin','jour','n_dose1','n_dose2','n_cum_dose1','n_cum_dose2']

df_fr= pd.DataFrame(data_fr, columns =data_fr_columns)

# styling the tabs
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1175ff',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    html.H1('Covid-19 Dasboard'),
    dcc.Tabs(id='tabs-world', value='world-data', children=[ 
        dcc.Tab(label='Monde', value='world-data', style=tab_style, selected_style=tab_selected_style,children=[
           dash_table.DataTable(# voir pourquoi les données ne s'affichent pas
               data=df.to_dict('records'),
               sort_action='native',
               sort_mode="multi",
               column_selectable="single",
               row_selectable="multi",
               columns=[{'id': c, 'name': c} for c in df.columns],
               fixed_rows={'headers': True, 'data': 1},
               selected_columns=[],
               selected_rows=[],
               page_action="native",
               page_current= 0,
               page_size=10,
               css=[{
                   'selector': '.dash-spreadsheet td div',
                   'rule': '''
                   line-height: 15px;
                   max-height: 30px; min-height: 30px; height: 30px;
                   display: block;
                   overflow-y: hidden;
                   '''
            }],
              tooltip_data=[
                {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            }   for row in df.to_dict('records')
            ],
            tooltip_duration=None,

            style_cell={'textAlign': 'left'}
    ),  
        ]),
        dcc.Tab(label='France', value='France-data', style=tab_style, selected_style=tab_selected_style,children=[
            ]),
        dcc.Tab(label='France Réanimation', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=[
            ]),
        dcc.Tab(label='France Décès', value='tab-2', style=tab_style, selected_style=tab_selected_style,children=[
            ]),
        dcc.Tab(label='France Vaccination', value='tab-3', style=tab_style, selected_style=tab_selected_style,children=[
                    ]),
        ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-world', 'value'))

def render_content(tab):
    if tab == 'world-data':
        return html.Div([
            html.H3('Données mondiales')
        ])
    elif tab == 'France-data':
        return html.Div([
            html.H3('Données de la France')
        ])
    elif tab == 'tab-1':
        return html.Div([
            html.H3('Données réanimation')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Données décès')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Données vaccination')
        ])
    
if __name__ == '__main__':
    app.run_server(debug=True)
