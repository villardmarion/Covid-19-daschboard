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

#import warnings
#from six import PY3
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#app = dash.Dash("covid")

covid_monde_url = (
    "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    )

def dataload():
    pd.read_csv(covid_monde_url, sep=",", encoding= 'utf-8') 


#warnings.filterwarnings("ignore")
data =dataload()


data_columns = ['Name',	'WHO Region' 'Cases - cumulative total','Cases - cumulative total per 100000 population','Cases - newly reported in last 7 days', 
'Cases - newly reported in last 7 days per 100000 population',	'Cases - newly reported in last 24 hours','Deaths - cumulative total',	
'Deaths - cumulative total per 100000 population','Deaths - newly reported in last 7 days','Deaths - newly reported in last 7 days per 100000 population',	
'Deaths - newly reported in last 24 hours','Transmission Classification']

df= pd.DataFrame(data, columns =data_columns)

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
    html.H1('Covid 19 Dasboard'),
    dcc.Tabs(id='tabs-world', value='world-data', children=[
        dcc.Tab(label='Monde', value='world-data', style=tab_style, selected_style=tab_selected_style,children=[
           dash_table.DataTable(
               data=df.to_dict('records'),
               columns=[{'id': c, 'name': c} for c in df.columns],
               page_size=10
               ) 
        ]),
        dcc.Tab(label='France', value='France-data', style=tab_style, selected_style=tab_selected_style,children=[
            ]),
        dcc.Tab(label='France réanimation', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=[
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
