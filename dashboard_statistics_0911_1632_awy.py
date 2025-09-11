# 代码生成时间: 2025-09-11 16:32:32
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# 假设我们有一个数据文件，名为data.csv
DATA_FILE = 'data.csv'

# 加载数据集
def load_data():
    try:
        # 读取CSV文件
        df = pd.read_csv(DATA_FILE)
        return df
    except Exception as e:
        # 打印错误信息，并返回空DataFrame
        print('Error loading data:', e)
        return pd.DataFrame()

# 创建Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(children=[
    html.H1(children='统计数据分析器'),
    dcc.Dropdown(
        id='column-selector',
        options=[{'label': i, 'value': i} for i in load_data().columns],
        value=load_data().columns[0],
        multi=False,
    ),
    dcc.Graph(id='bar-graph'),
])

# 回调函数，用于更新图形
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('column-selector', 'value')]
)
def update_graph(selected_column):
    df = load_data()
    if df.empty:
        return {}
    # 创建柱状图
    fig = px.bar(df, x=selected_column)
    return fig

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)