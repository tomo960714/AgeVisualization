# testing with new filtered countries for sunburst:
# Adding interaction with a lineplot - removing and adding countries

# CHECK FOR COMMENT LINES TO SEE WHAT HAS CHANGED/WHAT TO ADD TO MAP

import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import json


# ==============OCCUPATIONS
# occupation categories
# dictionary mapping occupations to categories
# top 50 occupations
category_mapping = {
    'Arts and Entertainment': ['Artist', 'Novelist', 'Pianist', 'Film producer', 'Cinematographer', 'Designer', 'Playwright', 'Author'],
    'Politics and Public Service': ['Politician', 'Military personnel', 'Flying ace', 'Judge', 'Jurist', 'Police officer', 'Minister'],
    'Science and Academia': ['Researcher', 'Astronomer', 'Biologist', 'Academic', 'Anthropologist', 'Geographer', 'Psychologist', 'Philosopher'],
    'Religion': ['Religious figure', 'Rabbi'],
    'Sports': ['Athlete', 'Rower', 'Fencer', 'Amateur wrestler', 'Sailor'],
    'Business and Commerce': ['Businessperson', 'Entrepreneur', 'Banker', 'Merchant', 'Publisher'],
    'Healthcare': ['Physician', 'Surgeon', 'Psychiatrist'],
    'Law and Justice': ['Lawyer'],
    'Media and Communication': ['Journalist', 'Translator'],
    'Education': ['Teacher', 'Librarian'],
    'Engineering and Architecture': ['Architect', 'Engineer'],
    'Agriculture': ['Farmer'],
    'Others': ['Aristocrat', 'Inventor', 'Explorer', 'Unspecified'],
    # 'Unspecified': ['Unspecified']
}

# categorizing occupations
def categorize_occupations(occupation):
    for category, occupations_list in category_mapping.items():
        if occupation in occupations_list:
            return category
    return 'Others'  # if occupation doesn't match any category, assign it to 'Others' - maybe need better name, as some of the 'Others' fall under the rest of the categories (fx. athlete)

# Add a new column 'Occupation categories' based on categorization
df['Occupation categories'] = df['Occupation'].apply(categorize_occupations)

# ==========================================================================

with open('countries.geojson', 'r') as f:
    geojson_data = json.load(f)

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = dbc.Container([
    html.Div([
        dcc.Graph(id='choropleth-map', style={'width': '55%', 'display': 'inline-block'}),
        dcc.Graph(id='sunburst', style={'width': '45%', 'display': 'inline-block'})
    ]),
    html.Div([
        html.Button('Viking Era', id='button-viking', n_clicks=0),
        html.Button('Ancient Greece', id='button-greece', n_clicks=0),
        html.Button('Maurya Empire', id='button-maurya', n_clicks=0),
        html.Button('Silk Road Establishment', id='button-silk-road', n_clicks=0),
        html.Button('Roman Empire', id='button-roman', n_clicks=0),
        html.Button('Great Wall of China', id='button-great-wall', n_clicks=0),
        html.Button('Mongol Empire', id='button-mongol', n_clicks=0),
        html.Button('Renaissance', id='button-renaissance', n_clicks=0),
        html.Button('Age of Exploration', id='button-exploration', n_clicks=0),
        html.Button('Sengoku Period', id='button-sengoku', n_clicks=0),
        html.Button('French Revolution', id='button-french-revolution', n_clicks=0),
        html.Button('Opium Wars', id='button-opium-wars', n_clicks=0),
        html.Button('Industrial Revolution', id='button-industrial', n_clicks=0),
        html.Button('Meiji Restoration', id='button-meiji', n_clicks=0),
        html.Button('Napoleonic Wars', id='button-napoleonic', n_clicks=0),
        html.Button('American Civil War', id='button-american-civil-war', n_clicks=0),
        html.Button('World War I', id='button-world-war-i', n_clicks=0),
        html.Button('Interwar Period', id='button-interwar', n_clicks=0),
        html.Button('World War II', id='button-world-war-ii', n_clicks=0),
        html.Button('Korean War', id='button-korean-war', n_clicks=0),
        html.Button('Cold War', id='button-cold-war', n_clicks=0),
        html.Button('Digital Age', id='button-digital-age', n_clicks=0),
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
    [Input('button-viking', 'n_clicks'),
    Input('button-greece', 'n_clicks'),
    Input('button-maurya', 'n_clicks'),
    Input('button-silk-road', 'n_clicks'),
    Input('button-roman', 'n_clicks'),
    Input('button-great-wall', 'n_clicks'),
    Input('button-mongol', 'n_clicks'),
    Input('button-renaissance', 'n_clicks'),
    Input('button-exploration', 'n_clicks'),
    Input('button-sengoku', 'n_clicks'),
    Input('button-french-revolution', 'n_clicks'),
    Input('button-opium-wars', 'n_clicks'),
    Input('button-industrial', 'n_clicks'),
    Input('button-meiji', 'n_clicks'),
    Input('button-napoleonic', 'n_clicks'),
    Input('button-american-civil-war', 'n_clicks'),
    Input('button-world-war-i', 'n_clicks'),
    Input('button-interwar', 'n_clicks'),
    Input('button-world-war-ii', 'n_clicks'),
    Input('button-korean-war', 'n_clicks'),
    Input('button-cold-war', 'n_clicks'),
    Input('button-digital-age', 'n_clicks')
    ]
)
def update_slider(*button_clicks):
    
    button_names = [
        'button-viking', 'button-greece', 'button-maurya', 'button-silk-road', 'button-roman',
        'button-great-wall', 'button-mongol', 'button-renaissance', 'button-exploration',
        'button-sengoku', 'button-french-revolution', 'button-opium-wars', 'button-industrial',
        'button-meiji', 'button-napoleonic', 'button-american-civil-war', 'button-world-war-i',
        'button-interwar', 'button-world-war-ii', 'button-korean-war', 'button-cold-war',
        'button-digital-age'
    ]

    time_periods = [
        [800, 1100], [-800, 400], [-322, -185], [130, 130], [27, 476],
        [700, 1700], [1206, 1368], [1300, 1700], [1400, 1700], [1400, 1700],
        [1789, 1799], [1839, 1860], [1750, 1850], [1868, 1868], [1789, 1815],
        [1861, 1865], [1914, 1918], [1918, 1939], [1939, 1945], [1950, 1953],
        [1947, 1991], [1980, 2021]
    ]
    clicked_button_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if clicked_button_id in [
        'button-viking', 'button-greece', 'button-maurya', 'button-silk-road', 'button-roman',
        'button-great-wall', 'button-mongol', 'button-renaissance', 'button-exploration',
        'button-sengoku', 'button-french-revolution', 'button-opium-wars', 'button-industrial',
        'button-meiji', 'button-napoleonic', 'button-american-civil-war', 'button-world-war-i',
        'button-interwar', 'button-world-war-ii', 'button-korean-war', 'button-cold-war',
        'button-digital-age'
    ]:
        return time_periods[button_names.index(clicked_button_id)]
    
    return [-1000, 2021]  # df['Birth year'].min(), df['Death year'].max()

    #     idx = button_names.index(clicked_button_id)
    #     print("idx", idx)
    #     print("periods", time_periods[idx])
    #     return time_periods[idx]
    # except ValueError:
    #     return df['Birth year'].min(), df['Death year'].max()

# Callback to update the choropleth map based on slider and button clicks
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('year-slider', 'value'),
    Input('sunburst', 'clickData')]
)
def update_map(year_range, clickData):
    # special attention here to birth and death range
    # do we want hard borders or just who was alive in this period?
    filtered_df = df[(df['Birth year'] <= year_range[1]) & (df['Death year'] >= year_range[0])]
        # {'points': [{'curveNumber': 0, 'pointNumber': 0, 'currentPath': '/Arts and Entertainment/', 
        #'root': '', 'entry': '', 'percentRoot': 0.2765957446808511, 'percentEntry': 0.2765957446808511, 
        # 'percentParent': 1, 'parent': 'Arts and Entertainment', 'id': 'Arts and Entertainment/Artist', 
        #'label': 'Artist', 'value': 13}]} 
    
##===================UPDATED============================================================================
    if clickData is not None:
        clicked_occupation = clickData['points'][0]['label']
        if (clickData['points'][0]['label'] == clickData['points'][0]['id']) == False:  
            # print(clickData)
            filtered_df = filtered_df[filtered_df['Occupation'] == clicked_occupation]  # filtering data based on clicked occupation
##=====================================================================================================
        
            # Count the number of observations per country
    country_counts = filtered_df['AssociatedModernCountry'].value_counts().reset_index()
    country_counts.columns = ['AssociatedModernCountry', 'Observation_Count']

    # Merge counts back into the original DataFrame
    filtered_df = pd.merge(filtered_df, country_counts, on='AssociatedModernCountry')

    # working with latitude and longitude
    fig = px.choropleth_mapbox(filtered_df, geojson=geojson_data, locations='AssociatedModernCountry', featureidkey="properties.ADMIN",
                               color='Observation_Count', hover_data=['AssociatedModernCountry', 'Observation_Count'],
                               mapbox_style="carto-positron", zoom=1.5, center={'lat': 20, 'lon': 0},
                               color_continuous_scale="Viridis", height = 800)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# ====================================SUNBURST==================================
selected_countries = []
@app.callback(
    Output('sunburst', 'figure'),
    [Input('choropleth-map', 'clickData'), 
     Input('year-slider', 'value')]
)
def update_sunburst(clickData, year_range):  # maybe you're missing a filtered_df somewhere with the slicer?
    global selected_countries
    # filter based on year range
    filtered_df = df[(df['Birth year'] <= year_range[1]) & (df['Death year'] >= year_range[0])]
    
    if clickData is not None:
        clicked_country = clickData['points'][0]['location']
    
        if clicked_country not in selected_countries:
            selected_countries.append(clicked_country)
        else:
            selected_countries.remove(clicked_country)
            
            if len(selected_countries) == 0:
                title = 'Occupation Distribution by Category in the World'
                occupation_count = filtered_df.groupby(['Occupation categories', 'Occupation']).size().reset_index(name='count')
                fig = px.sunburst(occupation_count,
                                 path = ['Occupation categories', 'Occupation'], 
                                  values = 'count',
                                 title = title,
                                 width = 800,
                                 height = 800)
                # fig.update_layout(title = 'Occupation Sunburst Plot')
                return fig
                
        print(selected_countries, " + ", len(selected_countries))

        # Filter data for the clicked country
        filtered_df = filtered_df[(filtered_df['AssociatedModernCountry'].isin(selected_countries))]


        occupation_count = filtered_df.groupby(['Occupation categories', 'Occupation']).size().reset_index(name='count')
        
        if len(selected_countries) > 0:
            title = 'Occupation Distribution by Category in ' + ', '.join(selected_countries)
        else:
            title = 'Occupation Distribution by Category in the World'
            
        fig = px.sunburst(occupation_count,
                         path = ['Occupation categories', 'Occupation'], 
                          values = 'count',
                         title = title,
                         width = 800,
                         height = 800)
        # fig.update_layout(title = 'Occupation Sunburst Plot')
        return fig
    else:
        if len(selected_countries) == 0:
            title = 'Occupation Distribution by Category in the World'
            occupation_count = filtered_df.groupby(['Occupation categories', 'Occupation']).size().reset_index(name='count')
            fig = px.sunburst(occupation_count,
                             path = ['Occupation categories', 'Occupation'], 
                              values = 'count',
                             title = title,
                             width = 800,
                             height = 800)
            # fig.update_layout(title = 'Occupation Sunburst Plot')
            return fig
        else: 
            filtered_df = filtered_df[(filtered_df['AssociatedModernCountry'].isin(selected_countries))]
            occupation_count = filtered_df.groupby(['Occupation categories', 'Occupation']).size().reset_index(name='count')

            if len(selected_countries) > 0:
                title = 'Occupation Distribution by Category in ' + ', '.join(selected_countries)
            else:
                title = 'Occupation Distribution by Category in the World'

            fig = px.sunburst(occupation_count,
                             path = ['Occupation categories', 'Occupation'], 
                              values = 'count',
                             title = title,
                             width = 800,
                             height = 800)
            # fig.update_layout(title = 'Occupation Sunburst Plot')
            return fig

# ====================================================================================

# Callback to update the line plot based on slider range
@app.callback(
    Output('line-plot', 'figure'),
    [Input('year-slider', 'value')]
)
def update_line_plot(year_range):
    # count deaths per year
    df['Century'] = (df['Birth year'] // 100) * 100
    average_age_per_century = df.groupby('Century')['Age of death'].mean()

    fig = go.Figure()

    # line plot for average age per century
    fig.add_trace(go.Scatter(x=average_age_per_century.index, y=average_age_per_century.values,
                             mode='lines+markers', name='Average Age'))

    fig.update_layout(title='Average Age of Death Across Centuries',
                      xaxis_title='Century',
                      yaxis_title='Average Age of Death',
                      xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightPink'),
                      yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightPink'),
                      plot_bgcolor='white')

    # range slider and selectors
    fig.update_layout(xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(step='all', label='All Centuries'),
            ])
        ),
        rangeslider=dict(visible=True)
    ))

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
