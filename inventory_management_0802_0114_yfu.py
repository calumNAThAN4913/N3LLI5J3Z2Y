# 代码生成时间: 2025-08-02 01:14:10
import dash\_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate

# Inventory management system using Dash framework
class InventoryManagementSystem:
    def __init__(self, app):
        self.app = app
        self.init_layout()
        self.init_callbacks()

    def init_layout(self):
        # Layout of the dashboard
        self.app.layout = html.Div(
            children=[
                html.H1('Inventory Management System', style={'textAlign': 'center'}),

                # Input section
                html.Div(
                    children=[
                        dbc.Input(id='product-name-input', placeholder='Enter product name', type='text'),
                        dbc.Button('Add Product', id='add-product-button', n_clicks=0),
                        dbc.Button('Remove Product', id='remove-product-button', n_clicks=0),
                        dbc.Input(id='search-product-input', placeholder='Search product', type='text')
                    ],
                    style={'textAlign': 'center', 'padding': '20px'}
                ),

                # Table to display inventory
                dbc.Table(
                    children=[
                        dbc.Thead(
                            children=[
                                dbc.Tr(
                                    children=[
                                        dbc.Th('Product Name'),
                                        dbc.Th('Quantity'),
                                        dbc.Th('Price'),
                                        dbc.Th('Actions')
                                    ]
                                )
                            ]
                        ),
                        dbc.Tbody(id='inventory-table-body')
                    ],
                    bordered=True,
                    responsive=True,
                    style={'margin': 'auto', 'width': '50%'}
                ),

                # Message section
                html.Div(id='message', children=[], style={'textAlign': 'center'})
            ]
        )

    def init_callbacks(self):
        # Callback to add product to inventory
        @self.app.callback(
            Output('inventory-table-body', 'children'),
            [Input('add-product-button', 'n_clicks')],
            prevent_initial_call=True
        )
        def add_product(n_clicks):
            if n_clicks <= 0:
                raise PreventUpdate
            product_name = self.app.callback_context.inputs['product-name-input']['property']['value']
            inventory_df = pd.DataFrame(columns=['Product Name', 'Quantity', 'Price'])
            if product_name:
                inventory_df.loc[0] = [product_name, 0, 0.0]
                return dbc.Tr(
                    children=[
                        dbc.Td(product_name),
                        dbc.Td(0),
                        dbc.Td(0.0),
                        dbc.Td(dbc.Button('Delete', color='danger', className='mr-2'))
                    ]
                )
            else:
                raise PreventUpdate

        # Callback to remove product from inventory
        @self.app.callback(
            Output('inventory-table-body', 'children'),
            [Input('remove-product-button', 'n_clicks')],
            prevent_initial_call=True
        )
        def remove_product(n_clicks):
            if n_clicks <= 0:
                raise PreventUpdate
            inventory_df = pd.DataFrame(columns=['Product Name', 'Quantity', 'Price'])
            return []

        # Callback to search product in inventory
        @self.app.callback(
            Output('inventory-table-body', 'children'),
            [Input('search-product-input', 'value')],
            prevent_initial_call=True
        )
        def search_product(product_name):
            if not product_name:
                raise PreventUpdate
            inventory_df = pd.DataFrame(columns=['Product Name', 'Quantity', 'Price'])
            return dbc.Tr(
                children=[
                    dbc.Td(product_name),
                    dbc.Td(0),
                    dbc.Td(0.0),
                    dbc.Td(dbc.Button('Delete', color='danger', className='mr-2'))
                ]
            )

if __name__ == '__main__':
    app = Dash(__name__)
    InventoryManagementSystem(app)
    app.run_server(debug=True)