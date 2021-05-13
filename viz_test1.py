# -*- coding: utf-8 -*-
"""
Created on Thu May 13 04:40:37 2021

@author: Dell
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import datetime

external_stylesheets = ['https://bootswatch.com/lumen/']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

covid_monde_url = ("https://covid19.who.int/WHO-COVID-19-global-data.csv")
df_monde = pd.read_csv(covid_monde_url, sep=",")
df_monde['Date_reported'] = pd.to_datetime(df_monde['Date_reported'], format='%Y-%m-%d')

available_indicators = df_monde['Country'].unique()

#columns= df_monde['New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Country'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Country'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': '#e5e5ff',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Country'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(id='date_slider',
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
                key=lambda date: datetime.datetime.strptime(date, '%m{}%d{}%Y')))},  # for bi-monthly marks
        step=1,
        vertical=False,
        updatemode='mouseup'),
        style={'width': '94.74%', 'float': 'left'})])

@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-xaxis-type', 'value'),
     Input('crossfilter-yaxis-type', 'value'),
     Input('date_slider', 'value')])


def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, year_value):
    df1 = df_monde[df_monde['Date_reported'] == year_value]
    fig = px.scatter(x=df1[df1['Country'] == xaxis_column_name]['New_cases'],
            y=df1[df1['Country'] == yaxis_column_name]['New_cases'],
            hover_name=df1[df1['Country'] == yaxis_column_name]['Country']
            )

    fig.update_traces(customdata=df1[df1['Country'] == yaxis_column_name]['Country'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(df1, axis_type, title):

    fig = px.scatter(df1, x='Date_reported', y='New_cases')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

@app.callback(
    Output('x-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-xaxis-type', 'value')])
    
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    region_name = hoverData['points'][0]['customdata']
    df1 = df_monde[df_monde['WHO_region'] == region_name]
    df1 = df1[df1['Country'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(region_name, xaxis_column_name)
    return create_time_series(df1, axis_type, title)

@app.callback(
    Output('y-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-yaxis-type', 'value')])
    
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    df1 = df_monde[df_monde['WHO_region'] == hoverData['points'][0]['customdata']]
    df1 = df1[df1['Country'] == yaxis_column_name]
    return create_time_series(df1, axis_type, yaxis_column_name)

if __name__ == '__main__':
    app.run_server(debug=True)