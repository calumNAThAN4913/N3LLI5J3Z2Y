# 代码生成时间: 2025-09-20 08:30:58
import psutil
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# 定义一个函数，用于获取CPU使用率
def get_cpu_usage():
    """
    获取CPU使用率
    
    返回值：
        float: CPU使用率百分比
    """
    return psutil.cpu_percent(interval=1)

# 定义一个函数，用于获取内存使用情况
def get_memory_usage():
    """
    获取内存使用情况
    
    返回值：
        tuple: (内存使用量, 总内存量)
    """
    memory = psutil.virtual_memory()
    return memory.used, memory.total

# 定义Dash应用程序
app = dash.Dash(__name__)

# 定义应用程序布局
app.layout = html.Div([
    html.H1("系统性能监控工具"),
    dcc.Graph(id='cpu-usage-graph'),
    html.Div(id='memory-usage-container'),
])

# 定义回调函数，用于更新CPU使用率图表
@app.callback(
    Output('cpu-usage-graph', 'figure'),
    [Input('cpu-usage-graph', 'interval')]
)
def update_cpu_usage_graph(_=None):
    cpu_usage = get_cpu_usage()
    # 创建CPU使用率图表
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=cpu_usage,
        title={'text': "CPU 使用率"},
        gauge={'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"}}
    ))
    return fig

# 定义回调函数，用于更新内存使用情况
@app.callback(
    Output('memory-usage-container', 'children'),
    [Input('memory-usage-container', 'n_intervals')]
)
def update_memory_usage(n):
    used_memory, total_memory = get_memory_usage()
    memory_usage = used_memory / total_memory * 100
    return html.Div([
        html.H2("内存使用情况\),
        html.P(f"已使用内存：{used_memory / (1024 ** 3):.2f} GB\),
        html.P(f"总内存：{total_memory / (1024 ** 3):.2f} GB\),
        html.P(f"内存使用率：{memory_usage:.2f}%\)
    ])

# 运行Dash应用程序
if __name__ == '__main__':
    app.run_server(debug=True)