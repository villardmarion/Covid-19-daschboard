# -*- coding: utf-8 -*-
"""
Created on Mon May 10 16:51:24 2021

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


app.layout = html.Div([
    html.H1('Covid 19'),
    dcc.Tabs(id='tabs-world', value='World Data', children=[
       html.Div([
           # formatting the table
           dash_table.DataTable(
               data=data.to_dict('rows'),
               columns=[
                   {'name': i, 'id': i} for i in data.columns
                   ],
               style_data_conditional=[
                   {
                       'if': {
                           'column_id': 'WHO Region',
                           'filter': 'WHO Region eq "Europe"'
                           },
                       'backgroundColor': '#3D9970',
                       'color': 'white',
                       },
                   {
                       'if': {
                           'column_id': 'Cases - newly reported in last 24 hours',
                           'filter': 'Cases - newly reported in last 24 hours > num(100)'
                           },
                       'backgroundColor': '#3D9970',
                       'color': 'orange',
                       },
                    {
                        'if': {
                            'column_id': 'Deaths - newly reported in last 24 hours',
                            'filter': 'Deaths - newly reported in last 24 hours > num(100)'
                            },
                        'backgroundColor': '#3D9970',
                        'color': 'red',
                        }
            ]),
            dash_table.DataTable(
                id= 'data-who',
                columns=[{"names":i,"id":i,"deletable":True} for i in data_columns],
                editable= True,
                #n_fixed_columns=2,
                style_table = {'maxWidth':'1500px'},
                row_selectable= "multi",
                selected_rows =[0],
                style_cell = {"fontFamily":"Arial","size":10,"textAligh":"left"}
                )
                ],className="Twelve columns"),
            # Download button
        html.Div([
            html.A(html.Button('Télécharger les données', id ='download-button'), id='download-link-who')
            ]),
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label':'Condensed Data Table', 'value':'Condensé'},
                    {'label':'Complete Data Table', 'value':'Complet'},
                    ], value='Condensé',
                labelStyle={'display':'inline-block', 'width':'20%', 'margin':'auto', 'marginTop':15, 'paddingLeft':15},
                id='radio-button'
                )]),
        #Graphs
        html.Div([
            html.Div([
                dcc.Graph(id='covid-world'),
                ], className="Twelve columns"
                ) 
                ],className="row")
                ], className="subpage"),
        html.Div(id='tab-world-content'),
        dcc.Tabs(id='tabs-france', value='France', children=[
                    dcc.Tab(label='Tab one', value='réanimation'),
                    dcc.Tab(label='Tab two', value='décès'),
                    dcc.Tab(label='Tab three', value='vaccination'),
    ]),
    html.Div(id='tabs-france-content')
])

@app.callback(Output('tabs-world-content', 'children'),
              Input('tabs-world', 'World Data'))

@app.callback(Output('tabs-france-content', 'children'),
              Input('tabs-france', 'France'))

@app.callback(
	Output('graph1','figure'),
	[Input('dropdown1','value')])
    
@app.callback(Output('data-who', 'columns'),
    [Input('radio-button', 'value')])

@app.callback(Output('covid-world','figure'),
    [Input('data','selected_rows')])


def render_content(tab1): # a revoir
    return html.Div([html.H3(tab1)])

def render_content1(tab): # a revoir
    if tab =='France':
        return html.Div([
            html.H3('France')
        ])

    elif tab == 'France': ## a revoir
        return html.Div([
            html.H3('France')
        ])
def update_columns(value):
    if value=='Complet':
        column_set=[{"name":i,"id":i,"deletable":True} for i in data_columns]
    elif value=='Condensé':
        column_set=[{"name":i,"id":i,"deletable":True} for i in data_columns]
    return column_set
    
def update_graph(new_dropdown_value):
	return {
		'data':[{
			'x':[1,3,3],
			'y':eval(new_dropdown_value)
		}]
}


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8080)
    