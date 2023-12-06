# MAKE YOUR OWN VERSION OF THIS
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx
import plotly.graph_objects as go
import dash
import datapackage
import json
import geopandas as gpd
import dash_bootstrap_components as dbc
import webbrowser
import numpy as np
import multi


df=pd.read_csv("pre_ages_loc.csv")  # INSERT NEWEST VERSION OF DATASET - AT LEAST V4
df.head(6)


# Adding interaction with a lineplot - removing and adding countries

# Adding interaction with a lineplot - removing and adding countries

import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import json

with open('countries.geojson', 'r') as f:
    geojson_data = json.load(f)

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='choropleth-map', style={'width': '65%', 'display': 'inline-block'}),
        dcc.Graph(id='sunburst', style={'width': '35%', 'display': 'inline-block'})
    ]),
    html.Div([
        html.Button('1917-1921', id='button-1', n_clicks=0),
        html.Button('1939-1945', id='button-2', n_clicks=0),
        html.Button('1980-1985', id='button-3', n_clicks=0),
        dcc.RangeSlider(
            id='year-slider',
            min=-1000,
            max=2021,
            value=[-1000, 2021],
            marks={str(year): str(year) for year in range(-1000, 2021, 200)},
            step=None
        ),
        dcc.Graph(id='line-plot')  # New line plot graph component
    ], style={'width': '100%', 'margin': 'auto'})
])


@app.callback(
    Output('year-slider', 'value'),
    [Input('button-1', 'n_clicks'),
     Input('button-2', 'n_clicks'),
     Input('button-3', 'n_clicks')]
)
def update_slider(button_1, button_2, button_3):
    clicked_button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if clicked_button_id == 'button-1':
        return [1917, 1921]
    elif clicked_button_id == 'button-2':
        return [1939, 1945]
    elif clicked_button_id == 'button-3':
        return [1980, 1985]
    else:
        return [df['Birth year'].min(), df['Birth year'].max()]

# callback to update the choropleth map based on slider and button clicks
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('year-slider', 'value')]
)

def update_map(year_range):
    # special attention here to birth and death range
    # do we want hard borders or just who was alive in this period?
    filtered_df = df[(df['Birth year'] <= year_range[1]) & (df['Death year'] >= year_range[0])]
    
        # count the number of observations per country
    country_counts = filtered_df['AssociatedModernCountry'].value_counts().reset_index()
    country_counts.columns = ['AssociatedModernCountry', 'Observation_Count']

    # merging counts back into the original DataFrame
    filtered_df = pd.merge(filtered_df, country_counts, on='AssociatedModernCountry')
    
    # working with latitude and longitude
    fig = px.choropleth_mapbox(filtered_df, geojson=geojson_data, locations='AssociatedModernCountry', featureidkey="properties.ADMIN",
                               color='Observation_Count', hover_data=['AssociatedModernCountry', 'Observation_Count'],
                               mapbox_style="carto-positron", zoom=1.5, center={'lat': 20, 'lon': 0},
                               color_continuous_scale="Viridis")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

selected_countries = []
# @app.callback(
#     Output('bar-plot', 'figure'),
#     [Input('choropleth-map', 'clickData'),
#      Input('year-slider', 'value')]
# )
# def update_bar_plot(clickData, year_range):  # error when bar plot becomes empy
#     if clickData is not None:
#         clicked_country = clickData['points'][0]['location']
        
#         if clicked_country in selected_countries:
#             selected_countries.remove(clicked_country)
#         else:
#             selected_countries.append(clicked_country)
#         # print(selected_countries)

#         # Filter data for the clicked country and the selected year range
#         filtered_df = df[(df['AssociatedModernCountry'].isin(selected_countries)) & 
#                          (df['Birth year'] <= year_range[1]) & 
#                          (df['Death year'] >= year_range[0])]

#         # Calculate population or any relevant data for the bar plot
#         # Example assuming 'Population' column exists
#         country_counts = filtered_df['AssociatedModernCountry'].value_counts().reset_index()
#         country_counts.columns = ['AssociatedModernCountry', 'Observation_Count']
#         # print(country_counts)

#         # Create bar plot for population
#         fig = px.bar(x=country_counts['AssociatedModernCountry'], y=country_counts['Observation_Count'], labels={'x': 'Country', 'y': 'Population'})
#         fig.update_layout(title=f'Population of {clicked_country}')
#         return fig

#     # If no country is clicked, return an empty figure
#     return {}

selected_countries = []    
@app.callback(
    Output('sunburst', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('year-slider', 'value')]
)
def update_sunburst(clickData, year_range):
    
#     if clickData is not None:
#         clicked_country = clickData['points'][0]['location']
        
#         if clicked_country in selected_countries:
#             selected_countries.remove(clicked_country)
#         else:
#             selected_countries.append(clicked_country)
#         # print(selected_countries)

#             # Filter data for the clicked country and the selected year range
#         filtered_df = df[(df['AssociatedModernCountry'].isin(selected_countries)) & 
#                          (df['Birth year'] <= year_range[1]) & 
#                          (df['Death year'] >= year_range[0])]
#         occupation_data = filtered_df[['Occupation', 'Gender', 'Name']]

#     else:
    occupation_data = df[['Occupation', 'Gender', 'Name']]
    # Create the sunburst chart for Occupation
    fig = px.sunburst(
        occupation_data,
        path=['Occupation', 'Gender'],
        title="Occupation Distribution by Gender",
        width=800,
        height=800
    )
    return fig
    

# Run the app
# app.run_server(mode='external', port = 8090, dev_tools_ui=True, #debug=True,
#               dev_tools_hot_reload =True, threaded=True)
if __name__ == '__main__':
    app.run_server(mode='external', port = 8090, dev_tools_ui=True, #debug=True,
              dev_tools_hot_reload =True, threaded=True)
    # app.run_server(port="8050")
    # app.run_server(debug=True, port = 1086)
    # app.run_server(debug=True, port=1086, dev_tools_ui=False, dev_tools_props_check=False, mode='external')
    # viewer.show(app)
