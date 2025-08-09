# 代码生成时间: 2025-08-09 16:02:50
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from dash_table import DataTable
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# 定义Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义全局变量
ORDERS_CSV = 'orders.csv'  # 假设有一个包含订单数据的CSV文件

# 加载订单数据
df = pd.read_csv(ORDERS_CSV)

# 定义Dash应用布局
app.layout = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Label('订单ID'), width=4), dbc.Col(dbc.Input(id='order-id-input', placeholder='输入订单ID', type='text'), width=8)]),
        dbc.Row([dbc.Col(dcc.Graph(id='order-graph'), width=12)]),
        dbc.Row([dbc.Col(dcc.Table(id='order-table', data=[], columns=[], style_cell={'textAlign': 'left'}), width=12)]),
    ], fluid=True
)

# 定义回调函数，用于处理订单查询和显示结果
@app.callback(
    Output('order-graph', 'figure'),
    Output('order-table', 'data'),
    Output('order-table', 'columns'),
    Input('order-id-input', 'value'),
    State('order-table', 'data'),
    State('order-table', 'columns'))
def query_order(order_id, table_data, table_columns):
    if not order_id:
        raise PreventUpdate
    try:
        # 根据订单ID过滤订单数据
        order_df = df[df['order_id'] == order_id]
        if order_df.empty:
            raise ValueError('订单ID不存在')

        # 创建图表
        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Bar(x=order_df['product'], y=order_df['quantity']), row=1, col=1)
        fig.add_trace(px.line(order_df, x='date', y='amount'), row=2, col=1)
        fig.update_layout(height=600)

        # 更新表格数据
        table_data = order_df.to_dict('records')
        table_columns = [{'name': i, 'id': i} for i in order_df.columns]
        return fig, table_data, table_columns
    except Exception as e:
        print(f'查询订单时发生错误：{e}')
        return go.Figure(), [], []

if __name__ == '__main__':
    app.run_server(debug=True)