# 代码生成时间: 2025-08-24 21:03:54
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
from flask import session
from functools import wraps

# 模拟数据库中的订单数据
orders_data = [
    {'order_id': 1, 'customer_name': 'John Doe', 'order_date': '2023-04-01', 'total_amount': 150.00, 'status': 'Shipped'},
    {'order_id': 2, 'customer_name': 'Jane Smith', 'order_date': '2023-04-02', 'total_amount': 200.00, 'status': 'Delivered'},
    {'order_id': 3, 'customer_name': 'Alice Johnson', 'order_date': '2023-04-03', 'total_amount': 120.00, 'status': 'Processing'},
    {'order_id': 4, 'customer_name': 'Bob Brown', 'order_date': '2023-04-04', 'total_amount': 180.00, 'status': 'Cancelled'},
]

# 将模拟数据转换为DataFrame
orders_df = pd.DataFrame(orders_data)

# 定义一个装饰器来检查用户是否登录
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            raise PreventUpdate("Please log in first.")
        return f(*args, **kwargs)
    return wrapper

# 创建Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("Order Processing Dashboard"),
    dcc.Graph(id='orders-status-graph'),
    dcc.Table(
        id='orders-table',
        columns=[{'name': i, 'id': i} for i in orders_df.columns],
        data=orders_df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        page_action='native',
        style_table={'overflowX': 'auto'}
    )
])

# 回调函数：更新订单状态图表
@app.callback(
    Output('orders-status-graph', 'figure'),
    [Input('orders-table', 'active_cell')])
@login_required
def update_status_graph(active_cell):
    if active_cell is None:
        raise PreventUpdate
    row, col = active_cell['row'], active_cell['column_id']
    status = orders_df.iloc[row]['status']
    
    # 根据状态创建图表
    fig = px.pie(orders_df, values='total_amount', names='status', title=f'Order Status: {status}')
    return fig

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)
