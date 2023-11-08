import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

import pandas as pd
import geopandas as gpd


color_scale = [(0.0, 'white'), (1.0, 'red')]

spain_coordinates = {
    "Madrid": {"latitude": 40.5, "longitude": -3.7038},
    "Barcelona": {"latitude": 41.7, "longitude": 2.1734},
    "Valencia/València": {"latitude": 39.4699, "longitude": -0.3763},
    "Sevilla": {"latitude": 37.3891, "longitude": -5.9845},
    "Bizkaia": {"latitude": 43.2630, "longitude": -2.9350}
}


MADRID_AC = gpd.read_file('data/MADRID_AC.json')
df_votos_mesas = pd.read_csv('data/votos_mesas')

df_votes = pd.read_csv('data/votes_wealth')
df_votes['size'] = df_votes['Votos a candidaturas'].apply(lambda x: '<5K' if x < 5000 else '>5K')

#need to enforce CODIGOINE to be read as a string
dtype_mapping1 = {
    'Código de Provincia': str    # Column 1 as string
}
#df_spain = pd.read_csv('df_spain.csv', dtype=dtype_mapping1)
df_madrid = pd.read_csv('data/df_madrid.csv', dtype=dtype_mapping1)

SPAIN_map = gpd.read_file('data/spain-provinces.geojson')
MADRID_map = gpd.read_file('data/municipalities.json')

#need to enforce CODIGOINE to be read as a string
dtype_mapping1 = {
    'Código de Provincia': str    # Column 1 as string
}
df_spain = pd.read_csv('data/df_spain.csv', dtype=dtype_mapping1)

# Define the Dash app and external CSS stylesheets
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

load_figure_template("MORPH")

# Sample data for charts (replace with your own data)
# ...

# Create a map using Plotly Express
fig_map = px.choropleth_mapbox(
  df_spain,
  locations="Código de Provincia",
  geojson=SPAIN_map,
  featureidkey="properties.cod_prov",
  color='%PSOE',
  mapbox_style="carto-darkmatter",
  hover_name="Nombre de Provincia",
  color_continuous_scale=color_scale,
  center={"lat": 40.4168, "lon": -3.7038},
  zoom=5,
  # range_color=[0, 0.4],
  width=1000,
  height=600
)

fig_map2 = px.choropleth_mapbox(
  df_votos_mesas, locations='CUSEC', 
  geojson='assets/MADRID_AC.json', 
  featureidkey='properties.CUSEC', color="%PSOE",
  mapbox_style="carto-darkmatter",
  hover_name="Municipio",
  hover_data=["Renta media por hogar","VotosObtenidos"],
  opacity=0.5,
  color_continuous_scale=color_scale,
  center={"lat": 40.4168, "lon": -3.70}, zoom=8,
  # range_color=[0, 0.4],
  width=1000,
  height=500
)

fig_map3 = px.choropleth_mapbox(
  df_votes, locations=df_votes.COD_POSTAL, geojson=MADRID_map, 
  featureidkey="properties.id", color='%PSOE',
  mapbox_style="carto-darkmatter",
  hover_name="Municipio",
  hover_data=["%PSOE"],
  color_continuous_scale=color_scale,
  center={"lat": 40.4168, "lon": -3.70}, 
  zoom=7,
  # range_color=[0, 0.4],
  # width=1000,
  height=500
)

bubble_fig = px.scatter(df_votes, x="Renta media por hogar", y="%PSOE",
size="Votos a candidaturas",
hover_name="Municipio", size_max=60,
height=500
)

table = dash_table.DataTable(
    columns=[
        {'name': 'Municipio', 'id': 'Municipio'},
        {'name': 'Votos a candidaturas', 'id': 'Votos a candidaturas'},
        {'name': 'PSOE', 'id': 'PSOE'},
        {'name': '%PSOE', 'id': '%PSOE'}
    ],
    data=df_votes.to_dict("records"),
    filter_action="native",
    sort_action="native",
    sort_mode="single",  # Allow only one column to be sorted at a time
    sort_by=[{'column_id': 'Votos a candidaturas', 'direction': 'desc'}],  # Initial sorting by 'Votos a candidaturas' in descending order
    style_table={'height': '150px', 'overflowY': 'auto'},
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'lightgrey',
        'font-family': "Arial"
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'grey',
        'font-family': "Arial"
    }
)

kpi_perc= df_votos_mesas['VotosObtenidos'].sum()/df_votos_mesas['VotosCandidaturas'].sum()
kpi_votes= df_votos_mesas['VotosCandidaturas'].sum()

# Define the layout of the Dash app with charts
app.layout = dbc.Container([
    dcc.Tabs(className="dbc", children=[
       #Tab1
        dbc.Tab(label="Mapa General", children=[
            html.H1("Resultados elecciones generales 2019", style={"text-align": "center"}),
            dcc.Dropdown(
            id='location-dropdown',
                options=[
                {'label': 'Provincias', 'value': 'provincias'},
                {'label': 'Municipios', 'value': 'municipios'},
                ],
                value='provincias',  # Default selection
                style={'width': '50%'}  # Set the width to 30%
            ),
            dcc.Graph(id="region-map")
        ]),
        #Tab2
        dbc.Tab(label="Provincia por municipios", children=[
            
            dbc.Row([html.H1("Resultados por municipios", style={"text-align": "center"})]),
            dcc.Dropdown(
            id='provincia-dropdown',
                options=[
                {'label': 'Madrid', 'value': 'Madrid'},
                {'label': 'Barcelona', 'value': 'Barcelona'},
                {'label': 'Valencia', 'value': 'Valencia/València'},
                {'label': 'Sevilla', 'value': 'Sevilla'},
                {'label': 'Bilbao', 'value': 'Bizkaia'},
                ],
                value='Madrid',  # Default selection
                style={'width': '50%'}  # Set the width to 30%
            ),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig_map3, id="fig_map3")
                ], width=6),
                dbc.Col([
                    dcc.Graph(figure=bubble_fig, id="bubble_fig")
                ], width=6),
            ]),
            html.Div([table], id="table"),
        ]),
        #Tab3
dbc.Tab(label="Mapa de Madrid por secciones censales", children=[
    dbc.Row([html.H1("Resultados por secciones censales", style={"text-align": "center"}),
        dbc.Col([
           dbc.Col(style={'height': '10%'}),
            # Create a row for KPIs
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("%PSOE"),
                        dbc.CardBody([
                            html.Div(kpi_perc, className="card-title"),  # Replace with your actual data
                        ], id="kpi_perc"),
                    ], style={"height": "80%"}),  # Set the height to 50%
                ], width=6),  # KPI column for %PSOE

                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Votos"),
                        dbc.CardBody([
                            html.Div(kpi_votes, className="card-title"),  # Replace with your actual data
                        ], id="kpi_votes"),
                    ], style={"height": "80%"}),  # Set the height to 50%
                ], width=6),  # KPI column for Total Votes
            ]),
                dbc.Col([
                    html.H3("Renta por hogar"),  # Add a title above the radio items
                    dcc.RadioItems(
                        id='income',
                        options=[
                            {'label': ' Todo', 'value': '%PSOE'},
                            {'label': ' Renta baja', 'value': 'PSOE_poor'},
                            {'label': ' Renta media', 'value': 'PSOE_mid'},
                            {'label': ' Renta media-alta', 'value': 'PSOE_uppermid'},
                            {'label': ' Renta alta', 'value': 'PSOE_rich'}
                        ],
                        value='%PSOE',
                        inline=True,
                        labelStyle={'display': 'block'}  # Display labels on separate lines
                    )
                ], width=12),  # Full width for radio items
        ], width=3),  # Left column for KPIs and radio items

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig_map2, id="section-map")
                ], width=12)  # Full width for the map
            ]),
        ], width=9)  # Right column for the map
    ])
]),

])
], style={"width": 1300})


#Callbacks to add interactivity to the app

#Tab 1
@app.callback(
    Output("region-map", "figure"),
    Input("location-dropdown", "value"))

def general_map(value):
    if value == 'provincias':
      geojson_path = 'assets/spain-provinces.geojson'

      fig_map = px.choropleth_mapbox(
      df_spain,
      locations="Código de Provincia",
      geojson=geojson_path,
      featureidkey="properties.cod_prov",
      color='%PSOE',
      mapbox_style="carto-darkmatter",
      hover_name="Nombre de Provincia",
      color_continuous_scale=color_scale,
      center={"lat": 40.4168, "lon": -3.7038},
      zoom=5,
      # range_color=[0, 0.4],
      width=1000,
      height=600
      )

    else:
      geojson_path = 'assets/Municipios_light2.json'
      df_municipios_spain = pd.read_csv('data/municipios_spain')
      df_municipios_spain['COD_POSTAL'] = df_municipios_spain['COD_POSTAL'].astype(str).str.zfill(5)

      fig_map = px.choropleth_mapbox(
        df_municipios_spain, locations=df_municipios_spain.COD_POSTAL, 
        geojson=geojson_path, 
        featureidkey="properties.CODIGOINE", color='%PSOE',
        mapbox_style="carto-darkmatter",
        hover_name="Municipio",
        hover_data=["%PSOE"],
        color_continuous_scale=color_scale,
        center={"lat": 40.4168, "lon": -3.70}, 
        zoom=5,
        range_color=[10, 50],
        width=1000,
        height=600
      )

    return fig_map

#Tab 2
@app.callback(
    Output("fig_map3", "figure"),
    Output("bubble_fig", "figure"),
    Output("table", "children"),
    Input("provincia-dropdown", "value"))

def report_card(value):
    df_municipios_spain = pd.read_csv('data/municipios_spain')
    df_municipios_spain['COD_POSTAL'] = df_municipios_spain['COD_POSTAL'].astype(str).str.zfill(5)
    df_filtered = df_municipios_spain[df_municipios_spain['Provincia'] == value]

    geojson_path = 'assets/Municipios_light2.json'

    fig_map3 = px.choropleth_mapbox(
      df_filtered, locations=df_filtered.COD_POSTAL, 
      geojson=geojson_path, 
      featureidkey="properties.CODIGOINE", color='%PSOE',
      mapbox_style="carto-darkmatter",
      hover_name="Municipio",
      hover_data=["%PSOE"],
      color_continuous_scale=color_scale,
      center={"lat": spain_coordinates[value]["latitude"], "lon": spain_coordinates[value]["longitude"]}, 
      zoom=7,
      #range_color=[10, 50],
    )

    bubble_fig = px.scatter(df_filtered, x="Renta media por hogar", y="%PSOE",
    size="Votos a candidaturas",
    hover_name="Municipio", size_max=60,
    height=500
    )

    table = dash_table.DataTable(
    columns=[
        {'name': 'Municipio', 'id': 'Municipio'},
        {'name': 'Votos a candidaturas', 'id': 'Votos a candidaturas'},
        {'name': 'PSOE', 'id': 'PSOE'},
        {'name': '%PSOE', 'id': '%PSOE'}
    ],
    data=df_filtered.to_dict("records"),
    filter_action="native",
    sort_action="native",
    sort_mode="single",  # Allow only one column to be sorted at a time
    sort_by=[{'column_id': 'Votos a candidaturas', 'direction': 'desc'}],  # Initial sorting by 'Votos a candidaturas' in descending order
    style_table={'height': '150px', 'overflowY': 'auto'},
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'lightgrey',
        'font-family': "Arial"
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'grey',
        'font-family': "Arial"
    }
)
    
    return fig_map3, bubble_fig, table


#Tab 3
@app.callback(
    Output("section-map", "figure"),
    Output("kpi_perc", "children"),
    Output("kpi_votes", "children"),
    Input("income", "value"))

def report_card(value):
    
    df_votos_mesas = pd.read_csv('data/votos_mesas')

    fig_map2 = px.choropleth_mapbox(
      df_votos_mesas, locations='CUSEC', 
      geojson='assets/MADRID_AC.json', 
      featureidkey='properties.CUSEC', color=value,
      mapbox_style="carto-darkmatter",
      hover_name="Municipio",
      hover_data=["Renta media por hogar","VotosObtenidos"],
      opacity=0.5,
      color_continuous_scale=color_scale,
      center={"lat": 40.4168, "lon": -3.70}, zoom=8,
      # range_color=[0, 0.4],
      width=1000,
      height=700
    )

    df_filtered = df_votos_mesas[pd.notna(df_votos_mesas[value])]
    kpi_num= df_filtered['VotosObtenidos'].sum()/df_filtered['VotosCandidaturas'].sum()
    kpi_votes= df_filtered['VotosObtenidos'].sum()
    kpi_perc= '{:,.2%}'.format(kpi_num)
    # kpi_votes= 1000000
    
    # return kpi_perc, kpi_votes
    return fig_map2, kpi_perc, kpi_votes


if __name__ == "__main__":
    app.run_server(debug=True, port=8000)
