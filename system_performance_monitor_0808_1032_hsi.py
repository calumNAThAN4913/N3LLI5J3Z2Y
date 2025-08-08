# 代码生成时间: 2025-08-08 10:32:24
import os
import psutil
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px


# 定义一个函数来获取系统性能数据
def get_system_performance():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_usage, memory_usage, disk_usage


# 创建Dash应用
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("系统性能监控工具"),
    dcc.Graph(id='cpu-usage-graph'),
    dcc.Graph(id='memory-usage-graph'),
    dcc.Graph(id='disk-usage-graph')
])

# 定义一个回调函数来更新CPU使用率图
@app.callback(
    Output('cpu-usage-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_cpu_usage_graph(n):
    cpu_usage = get_system_performance()[0]
    fig = px.line(
        x=[1, 2], y=[cpu_usage, cpu_usage],
        labels={'x': 'Time', 'y': 'CPU Usage (%)'},
        title='实时CPU使用率'
    )
    return fig

# 定义一个回调函数来更新内存使用率图
@app.callback(
    Output('memory-usage-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_memory_usage_graph(n):
    memory_usage = get_system_performance()[1]
    fig = px.line(
        x=[1, 2], y=[memory_usage, memory_usage],
        labels={'x': 'Time', 'y': 'Memory Usage (%)'},
        title='实时内存使用率'
    )
    return fig

# 定义一个回调函数来更新磁盘使用率图
@app.callback(
    Output('disk-usage-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_disk_usage_graph(n):
    disk_usage = get_system_performance()[2]
    fig = px.line(
        x=[1, 2], y=[disk_usage, disk_usage],
        labels={'x': 'Time', 'y': 'Disk Usage (%)'},
        title='实时磁盘使用率'
    )
    return fig

# 添加一个定时器组件来定期更新图表
app.layout.append(dcc.Interval(
    id='interval-component',
    interval=1*1000,  # 1秒
    n_intervals=0
))


# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)