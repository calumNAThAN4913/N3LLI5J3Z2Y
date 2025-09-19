# 代码生成时间: 2025-09-19 18:16:04
# random_number_generator.py
# This file contains a Dash application that generates random numbers.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import random

# Create the Dash application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div(children=[
    # Title of the application
    html.H1(children='Random Number Generator'),
    # Instructions for the user
    html.P(id='instructions', children='Enter a number and press generate'),
    # Input field for the user to enter a range
# NOTE: 重要实现细节
    dcc.Input(id='input-range', type='number', placeholder='Enter number here'),
    # Button to generate random number
    html.Button(id='generate-button', children='Generate'),
    # Output field to display the random number
# 增强安全性
    html.Div(id='output-container')
])

# Define the callback to generate a random number
@app.callback(
    Output('output-container', 'children'),
    [Input('generate-button', 'n_clicks')],
    [State('input-range', 'value')
])
def generate_random_number(n_clicks, input_value):
    # Error handling for input
    if not input_value or input_value < 1:
        return 'Please enter a positive integer.'
    # Attempt to convert the input to an integer
    try:
        num = int(input_value)
    except ValueError:
        return 'Invalid input. Please enter a number.'
    # Generate a random number and return it
    if n_clicks:
        random_number = random.randint(1, num)
        return f'Random number between 1 and {num}: {random_number}'
    return ''

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)