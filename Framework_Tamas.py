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
#import multi


df=pd.read_csv("Data/AgesDatasetV4.csv")
df.head(6)

df['AssociatedModernCountry'] = df['AssociatedModernCountry'].apply(lambda x: x.strip("[]'"))
df['AssociatedModernCountry'] = df['AssociatedModernCountry'].str.replace('"', "")


replacements = {
    'Czechia': 'Czech Republic',
    'United States': 'United States of America',
    "Côte d'Ivoire": 'Ivory Coast',
    'Tanzania': 'United Republic of Tanzania',
    'Serbia': 'Republic of Serbia',
    'North Macedonia': 'Macedonia'  # I know this is incorrect but the GEOjson was made earlier than 2019
}

df['AssociatedModernCountry'] = df['AssociatedModernCountry'].replace(replacements)

# Adding interaction with a lineplot - removing and adding countries

import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import json

with open('countries.geojson', 'r') as f:
    geojson_data = json.load(f)

# Create the Dash app
app = dash.Dash(__name__)


#From{
#### Country ####
# sort unique associated modern country
unique_country = df['AssociatedModernCountry'].unique()
unique_country.sort()

# Load the Natural Earth dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create a dictionary mapping continents to lists of countries
continents_countries = {}
for continent in world['continent'].unique():
    countries_in_continent = world[world['continent'] == continent]['name'].tolist()
    continents_countries[continent] = countries_in_continent
continents_countries = {continent: sorted(countries) for continent, countries in continents_countries.items()}

# add to list together
country_list = sorted(world['continent'].unique().tolist()) + unique_country.tolist() 

# add 'all' to the beginning country_list
country_list.insert(0, 'All')


#### Occupation ####
# get unique Occupaion list
unique_occupation = df['Occupation'].unique()
unique_occupation.sort()
# add 'all' to the beginning of the unique_occupation
unique_occupation = np.insert(unique_occupation, 0, 'All')

#### Gender ####
# get gender list
gender_list = sorted(df['Gender'].unique().tolist())
# add 'all' to the beginning of the gender list
gender_list.insert(0, 'All')

# create a dictionary of eras
eras = {
    'Viking Era': [793, 1066],
    'Ancient Greece': [-800, 400],
    'Maurya Empire': [-322,-185],
    'Silk Road Establishment': [130,130],
    'Roman Empire': [27,476],
    'Great Wall of China': [700,1700],
    'Mongol Empire': [1206,1368],
    'Reneissance': [1300,1700],
    'Age of Exploration': [1400,1700],
    'Sengoku Period': [1400,1700],
    'French Revolution': [1789,1799],
    'Opium Wars': [1839,1860],
    'Industrial Revolution': [1750,1850],
    'Meiji Restoration': [1868,1868],
    'Napoleonic Wars': [1789,1815],
    'American Civil War': [1861,1865],
    'World War I': [1914,1918],
    'Interwar Period': [1918,1939],
    'World War II': [1939,1945],
    'Korean War': [1950,1953],
    'Cold War': [1947,1991],
    'Digital age': [1980,2021],
    'Vietnam War': [1955,1975],
    
}

# sort eras by start year
eras = {era: start_year for era, start_year in sorted(eras.items(), key=lambda item: item[1])}



filters =html.Div([
    html.H2("Filters"),
    html.Hr(),
    #dbc.Button(id='gender-button', n_clicks=0, children='Both'),
    # add dropdown gender instead of button
    html.P("Select gender"),
    dcc.Dropdown(
        options=
        [{'label':gender,'value': gender} for gender in gender_list],
        multi = True,
        id = 'dropdown-gender',
        placeholder="Select options...",
        style={'width': '100%'}
    ),
    html.Div(id='output-gender'),
    #html.Div(id='current-state-div', style={'margin-top': '10px'}),
    html.Hr(),
    html.P("Select the countries you want to compare"),
    dcc.Dropdown(
        # add continents from continents_countries and unique countries to the dropdown
        options=
            [{'label': continent, 'value': continent} for continent in country_list],
        multi=True,
        id='dropdown-countries',
        placeholder="Select options...",
        style={'width': '100%'}
    ),
    html.Div(id='output-country'),
    html.Hr(),
    html.P("Select the occupation you want to compare"),
    # occupation dropdown
    dcc.Dropdown(
        options=
            [{'label': occupation, 'value': occupation} for occupation in unique_occupation],
        multi=True,
        id='dropdown-occupation',
        placeholder="Select options...",
        style={'width': '100%'}
        ),
    html.Div(id='output-occupation'),
    html.Hr(),
                        
    ], style={'width': '100%', 'margin': 'auto'})

year_select_boxes = html.Div(
    [
        dbc.Input(id="year_select_min",  type="number", min = df['Birth year'].min(), max = 2023, step=1),
        dbc.Input(id="year_select_max",  type="number", min = df['Birth year'].min(), max = 2023, step=1),
        html.Br(),
        html.P(id="output_min"),
        html.P(id="output_max"),
    ]
)

# create a button for born/died/alive and change the button title based on the callback

state_button = dbc.Button(id='state-button', n_clicks=0, children='Born')



##
eras_panel = dbc.Col([
    # add eras dropdown
    html.P("Select an era"),
    
    dcc.Dropdown(
        options=
            [{'label': era, 'value': era} for era in eras.keys()],
        multi=False,
        id='dropdown-era',
        placeholder="Select options...",
        style={'width': '60%'}
        ),
    html.Div(id='output-era'),

    dcc.RangeSlider(
        id='year-slider',
        min=-1000,
        max=2021,
        value=[-1000, 2021],
        marks={str(year): str(year) for year in range(-1000, 2021, 200)},
        step=None
    ),
    year_select_boxes,
    dcc.Graph(id='line-plot')  # New line plot graph component
], style={'width': '80%', 'margin': 'auto'})




#}to here
#generate the same app layout but with Bootstrap CSS and add a widget on the right so I can put my filters there in the future
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
#dcc.Graph(id='choropleth-map', style={'width': '70%', 'display': 'inline-block'}),
#                   dcc.Graph(id='bar-plot', style={'width': '30%', 'display': 'inline-block'})
                dcc.Store(id='store_map', storage_type='memory'),

                ])
            ], style={'width': '60%', 'margin': 'auto'}),
            dbc.Row([
                eras_panel,
            ], style={'width': '60%', 'margin': 'auto'}),       
        ]),
        #add a widget on the right so I can put my filters there in the future

        dbc.Col([
            dbc.Row([
                dbc.Col([filters


                ], style={'width': '100%', 'margin': 'auto'})
            ], style={'width': '100%', 'margin': 'auto'}),
        ], style={'width': '100%', 'margin': 'auto'}),
        ]),
    ], style={'width': '100%', 'margin': 'auto'}, fluid=True)

#from{


# callback for country dropdown checklist to update the store_map
@app.callback(
    Output('store_map', 'data'),
    Input('dropdown-countries', 'value')
)
def update_store_map(selected_options):
    if selected_options:
        # check if selected options has continents
        continents = [option for option in selected_options if option in continents_countries.keys()]
        # check if selected options has countries
        countries = [option for option in selected_options if option in continents_countries.values()]
        # if continents are selected, add all countries in the continent to the selected options
        if continents:
            for continent in continents:
                selected_options.extend(continents_countries[continent])
        # if countries are selected, add all continents of the countries to the selected options
        if countries:
            for country in countries:
                selected_options.extend(world[world['name'] == country]['continent'].tolist())
        # remove duplicates in selected options
        selected_options = list(set(selected_options))
        # sort selected options
        selected_options.sort()
        #return f'Selected options: {", ".join(selected_options)}'
        return selected_options
    else:
        # if no options selected, return all countries
        selected_options = unique_country
        # remove all from selected options
        selected_options.lower().remove('all')


        return selected_options
    
#callback for the choropleth map to save selected countries to the store_map
@app.callback(
    Output('store_map', 'data'),
    Input('choropleth-map', 'clickData')
)
def update_store_map(clickData):
    if clickData is not None:
        clicked_country = clickData['points'][0]['location']
        #print(clicked_country)
        return clicked_country
    else:
        return dash.no_update
    






# callback for country dropdown checklist 
@app.callback(
    Output('output-country', 'children'),
    #Input('dropdown-checklist', 'value')
)
def update_country_list(selected_options):
    if selected_options:
        # check if selected options has continents
        continents = [option for option in selected_options if option in continents_countries.keys()]
        # check if selected options has countries
        countries = [option for option in selected_options if option in continents_countries.values()]
        # if continents are selected, add all countries in the continent to the selected options
        if continents:
            for continent in continents:
                selected_options.extend(continents_countries[continent])
        # if countries are selected, add all continents of the countries to the selected options
        if countries:
            for country in countries:
                selected_options.extend(world[world['name'] == country]['continent'].tolist())
        # remove duplicates in selected options
        selected_options = list(set(selected_options))
        # sort selected options
        selected_options.sort()
        #return f'Selected options: {", ".join(selected_options)}'
        return selected_options
    else:
        # if no options selected, return all countries
        selected_options = unique_country
        # remove all from selected options
        selected_options.lower().remove('all')


        return selected_options

# callback for occupation dropdown checklist

@app.callback(
    Output('output-occupation', 'children'),
    Input('dropdown-occupation', 'value')
)
def update_occupation_list(selected_options):
    # if selected_options does not have all
    if selected_options:
        # remove duplicates in selected options
        selected_options = list(set(selected_options))
        # sort selected options
        selected_options.sort()
        #return f'Selected options: {", ".join(selected_options)}'
        return selected_options
    else:
        selected_options = unique_occupation
        # remove all from selected options
        selected_options.lower().remove('all')

        return selected_options
    
# gender callback
@app.callback(
    Output('output-gender', 'children'),
    Input('dropdown-gender', 'value')
)
def update_gender(selected_options):
    # if selected_options does not have all
    if selected_options:
        # remove duplicates in selected options
        selected_options = list(set(selected_options))
        # sort selected options
        selected_options.sort()
        #return f'Selected options: {", ".join(selected_options)}'
        return selected_options
    else:
        selected_options = gender_list
        # remove all from selected options
        selected_options.lower().remove('all')

        return selected_options




# eras callback
"""@app.callback(
    [Output('output-era', 'children'),
    Output('choropleth-map', 'figure')],
    Input('dropdown-era', 'value')
)

def update_era(selected_option):
    if selected_option:
        # get the values from eras dictionary
        year_range = eras[selected_option]
    return update_map(year_range)
"""
"""
# eras callback with object store
@app.callback(
    [Output('output-era', 'children'),
    Output('object-store_year_min', 'data'),
    Output('object-store_year_max', 'data')],
    Input('dropdown-era', 'value')
)

def update_era(selected_option):
    if selected_option:
        # get the values from eras dictionary
        year_range = eras[selected_option]
        return selected_option, year_range[0], year_range[1]
    else:
        return dash.no_update, dash.no_update, dash.no_update
    
# year select box callback
@app.callback(
    [Output("year_select_min", "value"),
    Output("year_select_max", "value")],
    [Input("object-store_year_min", "data"),
        Input("object-store_year_max", "data")],
)
def update_output_min(value_min, value_max):
    if value_min is None:
        value_min = df['Birth year'].min()
    if value_max is None:
        value_max = 2023
    if value_min > value_max:
        value_min = value_max
    if value_max < value_min:
        value_max = value_min
    return value_min, value_max

# change the year select box when the era is selected
@app.callback(
    [Output("year_select_min", "value"),
    Output("year_select_max", "value")],
    [Input("object-store_year_min", "data"),
        Input("object-store_year_max", "data"),
        Input("dropdown-era", "value")],
)
"""

# create callback for the era selection and the year box in a way, that if the era is selected, the year box will be updated



"""
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
"""
# Callback to update the choropleth map based on slider and button clicks
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('year-slider', 'value')]
)

def update_map(year_range,):
    # special attention here to birth and death range
    # do we want hard borders or just who was alive in this period?
    filtered_df = df[(df['Birth year'] <= year_range[1]) & (df['Death year'] >= year_range[0])]
    
        # Count the number of observations per country
    country_counts = filtered_df['AssociatedModernCountry'].value_counts().reset_index()
    country_counts.columns = ['AssociatedModernCountry', 'Observation_Count']

    # Merge counts back into the original DataFrame
    filtered_df = pd.merge(filtered_df, country_counts, on='AssociatedModernCountry')
    
    # working with latitude and longitude
    fig = px.choropleth_mapbox(filtered_df, geojson=geojson_data, locations='AssociatedModernCountry', featureidkey="properties.ADMIN",
                               color='Observation_Count', hover_data=['AssociatedModernCountry', 'Observation_Count'],
                               mapbox_style="carto-positron", zoom=1.5, center={'lat': 20, 'lon': 0},
                               color_continuous_scale="Viridis")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

selected_countries = []
@app.callback(
    Output('bar-plot', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('year-slider', 'value')]
)
def update_bar_plot(clickData, year_range):  # error when bar plot becomes empy
    if clickData is not None:
        clicked_country = clickData['points'][0]['location']
        
        if clicked_country in selected_countries:
            selected_countries.remove(clicked_country)
        else:
            selected_countries.append(clicked_country)
        # print(selected_countries)

        # Filter data for the clicked country and the selected year range
        filtered_df = df[(df['AssociatedModernCountry'].isin(selected_countries)) & 
                         (df['Birth year'] <= year_range[1]) & 
                         (df['Death year'] >= year_range[0])]

        # Calculate population or any relevant data for the bar plot
        # Example assuming 'Population' column exists
        country_counts = filtered_df['AssociatedModernCountry'].value_counts().reset_index()
        country_counts.columns = ['AssociatedModernCountry', 'Observation_Count']
        # print(country_counts)

        # Create bar plot for population
        fig = px.bar(x=country_counts['AssociatedModernCountry'], y=country_counts['Observation_Count'], labels={'x': 'Country', 'y': 'Population'})
        fig.update_layout(title=f'Population of {clicked_country}')
        return fig

    # If no country is clicked, return an empty figure
    return {}

# Run the app
# app.run_server(mode='external', port = 8090, dev_tools_ui=True, #debug=True,
#               dev_tools_hot_reload =True, threaded=True)
if __name__ == '__main__':
    app.run_server(#mode='external',
         port = 8090, dev_tools_ui=True, #debug=True,
              dev_tools_hot_reload =True, threaded=True)
    # app.run_server(port="8050")
    # app.run_server(debug=True, port = 1086)
    # app.run_server(debug=True, port=1086, dev_tools_ui=False, dev_tools_props_check=False, mode='external')
    # viewer.show(app)