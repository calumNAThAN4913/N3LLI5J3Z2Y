# 代码生成时间: 2025-08-04 20:05:06
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
from jupyter_dash import JupyterDash

# 初始化Dash应用程序
app = JupyterDash(__name__)
server = app.server

# 定义一个响应式布局
app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(html.H1("响应式布局 Dashboard"), width={"size": 6, "offset": 3}),
        dbc.Col(dcc.Graph(id="example-graph"), width={"size": 6, "offset": 3})
    ),
    fluid=True
)

# 添加回调函数以更新图表
@app.callback(
    Output("example-graph", "figure"),
    Input("example-graph", "id")
)
def update_graph(input_id):
    # 模拟一些数据
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 1, 2]})
    fig = px.line(df, x="x", y="y")
    # 检查输入是否有效，如果无效则触发PreventUpdate
    if not input_id:
        raise PreventUpdate
    return fig

# 运行应用程序
if __name__ == '__main__':
    app.run_server(debug=True)