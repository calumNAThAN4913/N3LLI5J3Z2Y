# 代码生成时间: 2025-09-03 19:36:30
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import pandas as pd
import numpy as np

# 定义Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(
    children=[
        html.H1(children='性能测试仪表板'),
        dcc.Graph(id='performance-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # 每1秒刷新一次
            n_intervals=0
        ),
    ]
)

# 定义生成测试数据的函数
def generate_test_data():
    """生成模拟性能测试数据"""
    # 创建DataFrame
    df = pd.DataFrame({
        'Time': pd.date_range(start='1/1/2023', periods=100, freq='S'),
        'Value': np.random.randint(100, 200, 100)
    })
    return df

# 回调函数，用于更新图表
@app.callback(
    Output('performance-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    """更新图表以显示最新的性能测试数据"""
    try:
        df = generate_test_data()
        fig = px.line(df, x='Time', y='Value', title='性能测试趋势')
        return fig
    except Exception as e:
        print(f"Error: {e}")
        return px.line(pd.DataFrame(), x='Time', y='Value', title='性能测试趋势')

# 运行服务器（仅在非测试环境中）
if __name__ == '__main__':
    app.run_server(debug=True)
