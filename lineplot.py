import pandas as pd
import plotly.graph_objects as go

# Load your dataset
df = pd.read_csv('ageDatasetV4.csv')

# Calculate the average age of death per century
df['Century'] = (df['Birth year'] // 100) * 100
average_age_per_century = df.groupby('Century')['Age of death'].mean()

# Create the main Plotly figure
fig = go.Figure()

# Add the line plot for average age per century
fig.add_trace(go.Scatter(x=average_age_per_century.index, y=average_age_per_century.values,
                         mode='lines+markers', name='Average Age'))

# Customize layout with title, axes labels, and grid
fig.update_layout(title='Average Age of Death Across Centuries',
                  xaxis_title='Century',
                  yaxis_title='Average Age of Death',
                  xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightPink'),
                  yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightPink'),
                  plot_bgcolor='white')

# Add range slider and selectors (if your x-axis is not date-based, you may need to adjust this)
fig.update_layout(xaxis=dict(
    rangeselector=dict(
        buttons=list([
            dict(step='all', label='All Centuries'),
            # Add other buttons as necessary for your data range
        ])
    ),
    rangeslider=dict(visible=True)
))

# Show figure
fig.show()
