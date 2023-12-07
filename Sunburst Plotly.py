# Author: Xiaoyang Zhang

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)


# Add file_path
file_path = 'Data/AgesDatasetV4.csv'
data = pd.read_csv(file_path)

# Filter the dataset for necessary columns
occupation_data = data[['Occupation', 'Gender', 'Name']]

# Create the sunburst chart for Occupation
fig_sunburst = px.sunburst(
    occupation_data,
    path=['Occupation', 'Gender'],
    title="Occupation Distribution by Gender",
    width=800,
    height=800
)

# Show the figure
fig_sunburst.show()

# Prepare data for the line chart
# Count the number of births and deaths per year
birth_counts = data['Birth year'].value_counts().sort_index()
death_counts = data['Death year'].value_counts().sort_index()

# Convert the series to a DataFrame
birth_df = birth_counts.reset_index()
death_df = death_counts.reset_index()

# Rename columns
birth_df.columns = ['Year', 'Births']
death_df.columns = ['Year', 'Deaths']

# Merge the dataframes on year
population_trends = pd.merge(birth_df, death_df, on='Year', how='outer').fillna(0)

# Assuming you have already prepared map_data as shown previously
# This is the code to create fig_map
fig_map = px.scatter_geo(
    lat='Latitude',
    lon='Longitude',
    color='Occupation',  # Differentiate points by occupation
    hover_name='Name',  # Display names on hover
    hover_data=['Occupation', 'Gender'],  # Additional info to display on hover
    title='World Map of Individuals by Occupation',
    width=800,
    height=600
)

# Now, this is the code to set up your Dash app layout with fig_map defined
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig_sunburst),
    dcc.Graph(figure=fig_map),
    # Add additional components for interactivity here
])


app.layout = html.Div([
    dcc.Graph(figure=fig_sunburst),
    dcc.Graph(figure=fig_map),
    # Add additional components for interactivity here
])

@app.callback(
    dash.dependencies.Output('output-plot', 'figure'),
    [dash.dependencies.Input('input-plot', 'selectedData')]
)
def update_output(selectedData):
    # Logic to update one plot based on selection from another plot
    pass

if __name__ == '__main__':
    app.run_server(debug=True)
