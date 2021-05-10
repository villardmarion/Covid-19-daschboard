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

app = dash.Dash("covid")

def dataload():
    pd.read_csv('C:/Users/Dell/Downloads/WHO COVID-19 global table data May 7th 2021 at 2.07.36 PM.csv', sep = ';',encoding='latin-1')
    
#warnings.filterwarnings("ignore")
data =dataload()

data_columns = ['Name',	'WHO Region' 'Cases - cumulative total','Cases - cumulative total per 100000 population','Cases - newly reported in last 7 days', 
'Cases - newly reported in last 7 days per 100000 population',	'Cases - newly reported in last 24 hours','Deaths - cumulative total',	
'Deaths - cumulative total per 100000 population','Deaths - newly reported in last 7 days','Deaths - newly reported in last 7 days per 100000 population',	
'Deaths - newly reported in last 24 hours','Transmission Classification']

        
    
app.layout = html.Div([
	html.H1('Covid 19'),
    html.Div([
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
    ], className="page")

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
    ]
)

@app.callback(
	Output('graph1','figure'),
	[Input('dropdown1','value')])
    
@app.callback(Output('data-who', 'columns'),
    [Input('radio-button', 'value')])

@app.callback(Output('covid-world','figure'),
    [Input('data-who','selected_rows')])

    
def update_columns(value):
    if value=='Complet':
        column_set=[{"name":i,"id":i,"deletable":True} for i in complete_columns]
    elif value=='Condensé':
        column_set=[{"name":i,"id":i,"deletable":True} for i in condensed_columns]
    return column_set
    
def update_graph(new_dropdown_value):
	return {
		'data':[{
			'x':[1,3,3],
			'y':eval(new_dropdown_value)
		}]
}
	
if __name__== '__main__':
	app.run_server(debug=True)
