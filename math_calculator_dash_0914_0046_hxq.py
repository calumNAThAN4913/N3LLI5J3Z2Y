# 代码生成时间: 2025-09-14 00:46:50
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# 定义Dash应用
app = dash.Dash(__name__)

# 定义App的布局
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            dbc.Col(
                html.H1('Math Calculator Dashboard'),
                md=12,
            ),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='math-function-dropdown',
                    options=[
                        {'label': 'Addition', 'value': 'add'},
                        {'label': 'Subtraction', 'value': 'subtract'},
                        {'label': 'Multiplication', 'value': 'multiply'},
                        {'label': 'Division', 'value': 'divide'},
                    ],
                    value='add',
                ),
                md=6,
            ),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Input(id='input-number-1', type='number'),
                md=6,
            ),
            dbc.Col(
                dcc.Input(id='input-number-2', type='number'),
                md=6,
            ),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='math-result-graph'),
                md=12,
            ),
        ),
    ],
)

# 回调函数计算结果
@app.callback(
    Output('math-result-graph', 'figure'),
    [Input('math-function-dropdown', 'value'),
     Input('input-number-1', 'value'),
     Input('input-number-2', 'value')],
)
def calculate_result(math_function, num1, num2):
    if math_function is None or num1 is None or num2 is None:
        raise PreventUpdate
    try:
        if math_function == 'add':
            result = num1 + num2
        elif math_function == 'subtract':
            result = num1 - num2
        elif math_function == 'multiply':
            result = num1 * num2
        elif math_function == 'divide':
            if num2 == 0:
                raise ValueError('Cannot divide by zero.')
            result = num1 / num2
        else:
            raise ValueError('Invalid math function.')
    except ValueError as e:
        return px.line(x=[0], y=[0], labels={'y': 'Error'}, error_y={'type': 'data', 'visible': True, 'color': 'red'}, title=f'Error: {e}')
    df = pd.DataFrame([{'Number 1': num1, 'Number 2': num2, 'Result': result},])
    fig = px.bar(df, x=['Number 1', 'Number 2', 'Result'], labels={'value': 'Value', 'variable': 'Type'}, title=f'{math_function.capitalize()} Result')
    return fig

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)