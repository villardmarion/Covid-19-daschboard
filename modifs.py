import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime
import numpy as np
import dash_bootstrap_components as dbc

#import warnings
#from six import PY3
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.GRID])
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

covid_monde_vaccination_url = ("https://covid19.who.int/who-data/vaccination-data.csv")
df_monde_vacc = pd.read_csv(covid_monde_vaccination_url, sep=",")

covid_url = ("https://www.data.gouv.fr/fr/datasets/r/900da9b0-8987-4ba7-b117-7aea0e53f530")
df = pd.read_csv(covid_url, sep=";")

covid_france_hosp_url = ("https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c")
covid_france_hosp = pd.read_csv(covid_france_hosp_url, sep=";")

covid_france_general_url = ("https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7")
covid_france_general = pd.read_csv(covid_france_general_url, sep=";")
covid_france_general_tot = covid_france_general[covid_france_general.sexe == 0]

#warnings.filterwarnings("ignore")

#données OMS

df_monde['date'] = pd.to_datetime(df_monde['Date_reported'])
#données france: vaccins


#df_fr= pd.DataFrame(data_fr, columns =data_fr_columns)

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

def create_card(title, content, date):
    card=[
        dbc.CardHeader([html.H2(title)]),
        dbc.CardBody(
            [   
                html.H3(content, className="card-title"),
                html.H5(date, className="card-text"),
            ]
        ),
        ]
    return(card)

#Données monde 
sum_cases_monde = df_monde['New_cases'].sum() 
sum_deaths = df_monde['New_deaths'].sum()
sum_vaccination = df_monde_vacc['TOTAL_VACCINATIONS'].sum()
date_recente = max(df_monde['date'])
covid_monde_last_day = df_monde[df_monde.date == date_recente]
sum_cases_last_day = covid_monde_last_day['New_cases'].sum()
sum_deaths_last_day = covid_monde_last_day['New_deaths'].sum()

date_recente_str = date_recente.strftime('%Y-%m-%d')

#Indicateurs du monde
card1=create_card("Nombre de cas", sum_cases_monde, date_recente_str)
card2=create_card("Nombre de décès", sum_deaths, date_recente_str)
card3=create_card("Nombre de vaccinations", sum_vaccination,date_recente_str)
card4=create_card("Nombre de cas du jour", sum_cases_last_day,date_recente_str)
card5=create_card("Nombre de décès du jour", sum_deaths_last_day,date_recente_str)

cards = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card1, color="#AED6F1", inverse=True)),
                dbc.Col(dbc.Card(card2, color="#85C1E9", inverse=True)),
                dbc.Col(dbc.Card(card3, color="#5DADE2", inverse=True)),
                dbc.Col(dbc.Card(card4, color="#3498DB", inverse=True)),
                dbc.Col(dbc.Card(card5, color="#2874A6", inverse=True)),
            ],
            className="mb-2",
        ),
    ]
)

# Données France 

total_deces_hosp = covid_france_hosp['incid_dc'].sum()
covid_france_general_total = covid_france_general_tot[covid_france_general_tot.jour == max(covid_france_general_tot['jour'])]
total_deces_general = covid_france_general_total['dc'].sum()
total_rea = covid_france_general_tot['rea'].sum()
total_hosp = covid_france_general_tot['hosp'].sum() 
dernier_jour = max(covid_france_general_tot['jour'])
covid_france_dernier_jour_hosp = covid_france_general_tot[covid_france_general_tot.jour == dernier_jour]
nombre_deces_jour = covid_france_dernier_jour_hosp['dc'].sum()
nombre_rea_jour = covid_france_dernier_jour_hosp['rea'].sum()
nombre_hosp_jour = covid_france_dernier_jour_hosp['hosp'].sum()

# Indicateurs France

card_fr1=create_card("Nombre de décès", f'{total_deces_general} dont {total_deces_hosp} en milieu hospitalier', dernier_jour)
card_fr2=create_card("Nombre de réanimations", total_rea,dernier_jour)
card_fr3=create_card("Nombre des hospitalisations", total_hosp,dernier_jour)

cards_fr = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_fr1, color="#C39BD3", inverse=True)),
                dbc.Col(dbc.Card(card_fr2, color="#AF7AC5", inverse=True)),
                dbc.Col(dbc.Card(card_fr3, color="#9B59B6", inverse=True)),
            ],
            className="mb-2",
        ),
    ]
)

# Données réanimations 

bbd_homme = covid_france_general[covid_france_general.sexe == 1]
bbd_femme = covid_france_general[covid_france_general.sexe == 2]

rea_homme = bbd_homme['rea'].sum()
rea_femme = bbd_femme['rea'].sum()

# Indicateurs réanimations

card_rea1=create_card("Nombre de réanimations", total_rea, dernier_jour)
card_rea2=create_card("Nombre de réanimations chez les hommes", rea_homme,dernier_jour)
card_rea3=create_card("Nombre de réanimations chez les femmes", rea_femme,dernier_jour)
card_rea4=create_card("Nombre de réanimations du jour", nombre_rea_jour,dernier_jour)

cards_rea = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_rea1, color="#FDEBD0", inverse=True)),
                dbc.Col(dbc.Card(card_rea2, color="#FAD7A0", inverse=True)),
                dbc.Col(dbc.Card(card_rea3, color="#F8C471", inverse=True)),
                dbc.Col(dbc.Card(card_rea4, color="#F5B041", inverse=True)),

            ],
            className="mb-2",
        ),
    ]
)

# Données décès 

deces_homme = bbd_homme['dc'].sum()
deces_homme = bbd_femme['dc'].sum()

# Indicateurs décès

card_dc1=create_card("Nombre de décès", f'{total_deces_general} dont {total_deces_hosp} en milieu hospitalier', dernier_jour)
card_dc2=create_card("Nombre de décès chez les hommes", deces_homme,dernier_jour)
card_dc3=create_card("Nombre de décès chez les femmes", deces_homme,dernier_jour)
card_dc4=create_card("Nombre de décès du jour", nombre_deces_jour,dernier_jour)

cards_dc = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_dc1, color="#EC7063", inverse=True)),
                dbc.Col(dbc.Card(card_dc2, color="#E74C3C", inverse=True)),
                dbc.Col(dbc.Card(card_dc3, color="#CB4335", inverse=True)),
                dbc.Col(dbc.Card(card_dc4, color="#B03A2E", inverse=True)),
            ],
            className="mb-2",
        ),
    ]
)

app.layout = html.Div([
    html.H1('Covid-19 Dasboard'),
    dcc.Tabs(id='tabs-world', value='world-data', children=[ 
        dcc.Tab(label='Monde', value='world-data', style=tab_style, selected_style=tab_selected_style,children=[
            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),

            html.Div(id='tabs-content-inline'),

           dash_table.DataTable(# voir pourquoi les données ne s'affichent pas
               data=df_monde.to_dict('records'),
               sort_action='native',
               sort_mode="multi",
               column_selectable="single",
               row_selectable="multi",
               columns=[{'id': c, 'name': c} for c in df_monde.columns],
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
            }   for row in df_monde.to_dict('records')
            ],
            tooltip_duration=None,

            style_cell={'textAlign': 'left'}
    ),  
        ]),
        dcc.Tab(label='France', value='France-data', style=tab_style, selected_style=tab_selected_style,children=[
             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards_fr,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            ]),
        dcc.Tab(label='France Réanimation', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=[
             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards_rea,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            ]),
        dcc.Tab(label='France Décès', value='tab-2', style=tab_style, selected_style=tab_selected_style,children=[
             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards_dc,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            ]),
        dcc.Tab(label='France Vaccination', value='tab-3', style=tab_style, selected_style=tab_selected_style,children=[
                    ]),
        ], style=tabs_styles),
    

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
    app.run_server(debug=True,host='localhost',port=8080)
