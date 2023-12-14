# Author: Xiaoyang Zhang

# This time I have to add the interaction between the map plot to the line plot. For instance, if Brazil is clicked on the map, the line plot will show the average age of death in Brazil across centuries. I have to adapt my current code for line plot.

# Show the x-axis as years instead of centuries

# Remove dots from the choropleth map

# Aggegate different countries' lines

# Reference:
# https://plotly.com/python/aggregations/#aggregate-functions
# https://plotly.com/python/range-slider/?fbclid=IwAR0psKdYC0DRJLplIj-EsHwt_B1HN-QR0bEyhZ17gcNvXvfFhoKNl4zLe9Q


import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load the dataset
file_path = 'ageDatasetV4.csv'
df = pd.read_csv(file_path)

# Example list of countries to line chart
countries_to_plot = ['France', 'Germany', 'Italy', 'Togo', 'Spain']  # Example countries

# Initialize Plotly figure
fig = go.Figure()

# Processing data for each country
for country in countries_to_plot:
    # Filter data for the selected country
    country_df = df[df['Country'] == country]

    # Create a DataFrame for each year
    start_year = country_df['Birth year'].min()
    end_year = country_df['Death year'].max()
    years = np.arange(start_year, end_year + 1)

    # Initialize an empty DataFrame to store the results
    yearly_data = pd.DataFrame({'Year': years})
    yearly_data.set_index('Year', inplace=True)

    # Calculate the average age of death for each year
    for year in years:
        yearly_births = country_df[country_df['Birth year'] == year]
        yearly_deaths = country_df[country_df['Death year'] == year]
        total_people = pd.concat([yearly_births, yearly_deaths])
        average_age = total_people['Age of death'].mean()
        yearly_data.loc[year, 'Average Age of Death'] = average_age

    # Filter out years with no data
    yearly_data.dropna(inplace=True)

    # Add the line plot for this country
    fig.add_trace(go.Scatter(x=yearly_data.index, y=yearly_data['Average Age of Death'], mode='lines', name=country))

# Customize layout with title, axes labels, and grid
fig.update_layout(title= f'Average Age of Death Across Years in {", ".join(countries_to_plot)}',
                  xaxis_title='Year',
                  yaxis_title='Average Age of Death',
                  xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightPink'),
                  yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightPink'),
                  plot_bgcolor='white')

# Add range slider and selectors for years
fig.update_layout(xaxis=dict(
    rangeselector=dict(
        buttons=list([
            dict(count=10, label='Last 10 Years', step='year', stepmode='backward'),
            dict(count=50, label='Last 50 Years', step='year', stepmode='backward'),
            dict(step='all', label='All Years')
        ])
    ),
    rangeslider=dict(visible=True)
))

# Show figure
fig.show()
