# 代码生成时间: 2025-10-02 17:05:48
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
import requests

# Define the layout of the dashboard
def create_layout():
    # Create a simple layout with a title and a dropdown for selecting the sensor
    return html.Div(children=[
        html.H1(children='Agricultural IoT Dashboard'),
        html.Div(children=dcc.Dropdown(
            id='sensors-dropdown',
            options=[{'label': f'Sensor {i}', 'value': i} for i in range(1, 11)],
            value=[1, 2, 3],  # Default value
            multi=True
        )),
        dcc.Graph(id='live-update-graph')
    ])

# Define the callback to update the graph
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('sensors-dropdown', 'value')]
)
def update_graph(selected_sensors):
    # Prevent the callback from updating if there are no sensors selected
    if not selected_sensors:
        raise PreventUpdate()
    
    # Fetch data from the API for the selected sensors
    try:
        # Simulate API call with a sleep
        # In a real scenario, replace this with an actual API request
        import time; time.sleep(1)
        data = {'sensors': selected_sensors}  # Simulated data
    except Exception as e:
        # Handle any errors that occur during the API call
        return px.line().update_layout(title_text=f'Error: {str(e)}')
        
    # Create a line chart with the fetched data
    figure = px.line(data, x='timestamp', y='value', color='sensors').update_layout(title_text='Sensor Data')
    return figure

# Create the Dash application
app = dash.Dash(__name__)
app.layout = create_layout()

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)