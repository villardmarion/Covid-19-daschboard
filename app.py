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
import warnings


app = dash.Dash("covid")

def dataload():
    pd.read_csv('https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-personnes-vaccinees-contre-la-covid-19-1/', sep = ';',encoding='latin-1')
    
warnings.filterwarnings("ignore")
data =dataload()

    
app.layout = html.Div([
	html.H1('Covid19 Dashboard'),
    	dcc.Dropdown(
			id='dropdown1',
			options=[
				{'label':'France','value':'[3,1,3]'},
				{'label':'India','value':'[5,15,3]'},
				{'label':'USA','value':'[3,15,3]'}
			],
		value='[3,1,3]'
	),
	dcc.Graph(id='graph1')
])

	
@app.callback(
	Output('graph1','figure'),
	[Input('dropdown1','value')])

def update_graph(new_dropdown_value):
	return {
		'data':[{
			'x':[1,3,3],
			'y':eval(new_dropdown_value)
		}]
}
	
if __name__== '__main__':
	app.run_server(debug=True)
