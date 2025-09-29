# 代码生成时间: 2025-09-30 02:52:27
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
from dash.exceptions import PreventUpdate

# Define the layout of the Dash app
app = dash.Dash(__name__)

# Define a dropdown menu to select a stock
stock_dropdown = dcc.Dropdown(
    id='stock-dropdown',
    options=[{'label': 'AAPL', 'value': 'AAPL'}, {'label': 'GOOG', 'value': 'GOOG'}],
    value='AAPL',
)

# Define a graph to display the stock price
stock_graph = dcc.Graph(id='stock-graph')

# Define the layout of the app
app.layout = html.Div([
    html.H1('High Frequency Trading System'),
    stock_dropdown,
    stock_graph,
])

# Callback to update the stock graph when a stock is selected
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-dropdown', 'value')],
)
def update_stock_graph(selected_stock):
    # Fetch the stock data from Yahoo Finance
    try:
        stock_data = yf.download(selected_stock, period='1d')
    except Exception as e:
        # Handle any errors that occur during data fetching
        return {'layout': 'No data available for the selected stock.'}

    # Convert the stock data to a Pandas DataFrame
    df = pd.DataFrame(stock_data)

    # Extract the closing prices and create a new DataFrame
    closing_prices = df['Close']

    # Create a plotly express line chart of the closing prices
    fig = px.line(closing_prices, y='Close', title=f'{selected_stock} Stock Price')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
