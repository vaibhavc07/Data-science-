# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown for Launch Site
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # Pie chart
    dcc.Graph(id='success-pie-chart'),
    html.Br(),

    html.P("Payload range (Kg):"),

    # Payload slider
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),

    # Scatter chart
    dcc.Graph(id='success-payload-scatter-chart'),
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site):
    if site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Success Launches By Site')
    else:
        df_site = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(df_site, names='class',
                     title=f'Total Success vs Failure for site {site}')
    return fig

# Callback for scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(site, payload_range):
    low, high = payload_range
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    if site == 'ALL':
        fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Correlation Between Payload and Success for All Sites')
    else:
        df_site = df_filtered[df_filtered['Launch Site'] == site]
        fig = px.scatter(df_site, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Correlation Between Payload and Success for {site}')
    return fig

# Run the app
# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)

