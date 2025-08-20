# 代码生成时间: 2025-08-21 05:46:14
import hashlib
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Define the main function for the hashing
def calculate_hash(input_text, hash_algorithm):
    """
    Calculate the hash of the input text using the specified algorithm.
# 增强安全性

    Args:
        input_text (str): The text to be hashed.
        hash_algorithm (str): The name of the hashing algorithm to use.

    Returns:
        str: The calculated hash.
    """
    hash_func = getattr(hashlib, hash_algorithm, None)
    if not hash_func:
# 优化算法效率
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
    return hash_func(input_text.encode()).hexdigest()
# 优化算法效率

# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = html.Div(
    [
        dbc.Container(
# 优化算法效率
            [
                dbc.Row(
                    dbc.Col(
                        dbc.Input(id='input-text', placeholder='Enter text to hash', type='text'),
                        width=12
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.DropdownMenu(
                            id='hash-algorithm-dropdown',
                            direction='down',
                            children=[
                                dbc.DropdownMenuItem(
                                    dbc.Button(
                                        'MD5',
                                        outline=True,
                                        color='primary',
                                        className='dropdown-toggle-split'
                                    )
                                ),
                                dbc.DropdownMenuItem(
                                    'SHA1',
                                    className='dropdown-item'
                                ),
# 改进用户体验
                                dbc.DropdownMenuItem(
                                    'SHA256',
                                    className='dropdown-item'
                                ),
                                dbc.DropdownMenuItem(
                                    'SHA512',
                                    className='dropdown-item'
                                ),
                                dbc.DropdownMenuItem(
                                    'SHA224',
                                    className='dropdown-item'
                                )
                            ],
                            label='Select Hash Algorithm',
# 扩展功能模块
                            nav=True,
                            in_navbar=True,
                            className='d-none d-lg-block'
                        ),
                        width=3
                    )
                ),
                dbc.Row(
# 添加错误处理
                    dbc.Col(
                        html.Button('Calculate Hash', id='calculate-hash-button', n_clicks=0, className='me-1'),
                        width=12
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(id='output-hash', style={'whiteSpace': 'pre-line'}),
                        width=12
                    )
# TODO: 优化性能
                )
            ],
            className='mt-4',
# 改进用户体验
            fluid=True
# 增强安全性
        )
    ]
)
# NOTE: 重要实现细节

# Callback to handle the calculation of the hash
@app.callback(
    Output('output-hash', 'children'),
    [Input('calculate-hash-button', 'n_clicks')],
    prevent_initial_call=True
)
def on_calculate_hash(n_clicks):
    if n_clicks > 0:
        input_text = dash.callback_context.inputs['input-text']['value']
        hash_algorithm = dash.callback_context.inputs['hash-algorithm-dropdown']['active']
# FIXME: 处理边界情况
        try:
            result_hash = calculate_hash(input_text, hash_algorithm)
            return result_hash
        except ValueError as e:
            return str(e)
    return ''

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
