# 代码生成时间: 2025-08-18 23:38:12
import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import ALL, MATCH, ALLSMALLER
import plotly.express as px
import pandas as pd

# Define the layout of the dashboard
def serve_layout():
    return html.Div(
        [   # Header
            html.H1("UI Component Library"),
            # Dropdown for selecting a component
            dcc.Dropdown(
                id='component-selector',
                options=[
                    {'label': component, 'value': component} for component in ['Button', 'Checkbox', 'RadioItems', 'Slider', 'DatePickerRange', 'Graph']
                ],
                value='Button',
                clearable=False
            ),
            # Component display container
            html.Div(id='component-container')
        ],
        style={'columnCount': 2},
    )

# Callback to update the component display based on selection
@app.callback(
    Output('component-container', 'children'),
    Input('component-selector', 'value')
)
def display_component(selected_component):
    if selected_component is None:
        raise PreventUpdate()
    
    # Define the components
    components = {
        'Button': html.Button('Click Me', id='sample-button'),
        'Checkbox': dcc.Checklist(
            id='sample-checkbox',
            options=[{'label': 'Option 1', 'value': 'option1'},
                     {'label': 'Option 2', 'value': 'option2'}],
            value=['option1']
        ),
        'RadioItems': dcc.RadioItems(
            id='sample-radio',
            options=[{'label': 'Option 1', 'value': 'option1'},
                     {'label': 'Option 2', 'value': 'option2'}],
            value='option1'
        ),
        'Slider': dcc.Slider(
            id='sample-slider',
            min=0,
            max=9,
            step=1,
            marks={i: f'Label {i}' for i in range(10)},
            value=5
        ),
        'DatePickerRange': dcc.DatePickerRange(
            id='sample-date-picker-range',
            start_date={'year': 2021, 'month': 1, 'day': 1},
            end_date={'year': 2021, 'month': 1, 'day': 10}
        ),
        'Graph': html.Div(
           dcc.Graph(id='sample-graph'),
            style={'width': '600px', 'height': '600px'}
        )
    }
    
    return components.get(selected_component, "No component found")

# Initialize the app and layout
app = dash.Dash(__name__)
app.layout = serve_layout()

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)