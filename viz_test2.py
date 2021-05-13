# -*- coding: utf-8 -*-
"""
Created on Thu May 13 05:48:42 2021

@author: Dell
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://bootswatch.com/lumen/']

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
df_monde = pd.read_csv(covid_monde_url, sep=",")
df_monde['Date_reported'] = pd.to_datetime(df_monde['Date_reported'], format='%Y-%m-%d')
available_indicators = df_monde['Country'].unique()


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(dcc.RadioItems(id='global_format',
            options=[{'label': i, 'value': i} for i in df_monde['WHO_region'].unique()],
            value='Monde',
            labelStyle={'float': 'center', 'display': 'inline-block'}
            ), style={'textAlign': 'center',
                'color': dash_colors['text'],
                'width': '100%',
                'float': 'center',
                'display': 'inline-block'
            }
        ),

    html.Div(dcc.Graph(id='new_cases'),
        style={
            'textAlign': 'center',
            'color': dash_colors['red'],
            'width': '25%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),

    html.Div(dcc.Graph(id='total_cases'),
        style={
            'textAlign': 'center',
            'color': dash_colors['red'],
            'width': '25%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),

    html.Div(dcc.Graph(id='new_deaths'),
        style={
            'textAlign': 'center',
            'color': dash_colors['red'],
            'width': '25%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),
    html.Div(html.Div(dcc.Slider(id='date_slider',
                min=list(range(len(df_monde['Date_reported'].unique())))[0],
                max=list(range(len(df_monde['Date_reported'].unique())))[-1],
                value=list(range(len(df_monde['Date_reported'].unique())))[-1],
                # marks={(idx): {'label': date.format(u"\u2011", u"\u2011") if
                #     (idx-4)%7==0 else '', 'style':{'transform': 'rotate(30deg) translate(0px, 7px)'}} for idx, date in
                #     enumerate(sorted(set([item.strftime("%m{}%d{}%Y") for
                #     item in df_worldwide['date']])))},  # for weekly marks,
                marks={(idx): {'label': date.format(u"\u2011", u"\u2011") if
                    date[4:6] in ['01', '15'] else '', 'style':{'transform': 'rotate(30deg) translate(0px, 7px)'}} for idx, date in
                    enumerate(sorted([item.strftime("%m{}%d{}%Y") for
                    item in pd.Series(df_monde['Date_reported'].unique())],
                    key=lambda date: datetime.strptime(date, '%m{}%d{}%Y')))},  # for bi-monthly marks
                step=1,
                vertical=False,
                updatemode='mouseup'),
            style={'width': '94.74%', 'float': 'left'}),  # width = 1 - (100 - x) / x
        style={'width': '95%', 'float': 'right'})
    ])


@app.callback(
    Output('new_cases', 'figure'),
    [Input('global_format', 'value')])

def confirmed(view):
    '''
    creates the CUMULATIVE CONFIRMED indicator
    '''

    value = df_monde[df_monde['Date_reported'] == df_monde['Date_reported'].iloc[-1]]['New_cases'].sum()
    delta = df_monde[df_monde['Date_reported'].unique()[-2]]['New_cases'].sum()
    return {
            'data': [{'type': 'indicator',
                    'mode': 'number+delta',
                    'value': value,
                    'delta': {'reference': delta,
                              'valueformat': ',g',
                              'relative': False,
                              'increasing': {'color': dash_colors['blue']},
                              'decreasing': {'color': dash_colors['green']},
                              'font': {'size': 25}},
                    'number': {'valueformat': ',',
                              'font': {'size': 50}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                title={'text': "Nombre de cas confimés"},
                font=dict(color=dash_colors['red']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }

@app.callback(
    Output('total_cases', 'figure'),
    [Input('global_format', 'value')])
def active(view):
    '''
    creates the CURRENTLY ACTIVE indicator
    '''

    value = df_monde[df_monde['Date_reported'] == df_monde['Date_reported'].iloc[-1]]['Cumulative_cases'].sum()
    delta = df_monde[df_monde['Date_reported'] == df_monde['Date_reported'].unique()[-2]]['Cumulative_cases'].sum()
    return {
            'data': [{'type': 'indicator',
                    'mode': 'number+delta',
                    'value': value,
                    'delta': {'reference': delta,
                              'valueformat': ',g',
                              'relative': False,
                              'increasing': {'color': dash_colors['blue']},
                              'decreasing': {'color': dash_colors['green']},
                              'font': {'size': 25}},
                    'number': {'valueformat': ',',
                              'font': {'size': 50}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                title={'text': "total cases"},
                font=dict(color=dash_colors['red']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }



if __name__ == '__main__':
    app.run_server(debug=True, port= '8888')