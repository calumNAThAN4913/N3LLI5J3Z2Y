# 代码生成时间: 2025-10-09 01:59:20
# infinite_loading_component.py
"""
A Dash application that demonstrates how to implement an infinite loading component.
"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Initialize the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = html.Div([
    dbc.Button("Load More", id="load-more-button", className="mb-3"),
    dbc.Spinner(id="loading-spinner"),
    html.Div(id="infinite-container"),
])

# Callback to handle the loading of more items
@app.callback(
    Output("infinite-container", "children"),
    [Input("load-more-button", "n_clicks")],
    [State("infinite-container", "children")],
    prevent_initial_call=True
)
def load_more(n_clicks, container_children):
    # If the button has not been clicked, do nothing
    if n_clicks is None:
        raise PreventUpdate()
    
    # Simulate an infinite loading process
    new_children = []
    for i in range(5):  # Load 5 more items
        new_children.append(
            html.Div(
                f"Item {len(container_children) + i + 1}",
                id=f"item-{len(container_children) + i + 1}"
            )
        )
    
    # Return the new children to be appended to the container
    return container_children + new_children

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
