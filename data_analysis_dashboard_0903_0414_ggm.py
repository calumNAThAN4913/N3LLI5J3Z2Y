# 代码生成时间: 2025-09-03 04:14:33
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# 应用入口函数
def create_dashboard():
    # 引入Dash应用
    app = dash.Dash(__name__)

    # 用于解析数据的URL
    app.layout = html.Div(children=[
        html.H1("数据分析器"),

        html.Div(children=[
            "选择一个数据文件进行分析：",
            dcc.Upload(
                id='upload-data',
                children=html.Button('上传文件'),
                multiple=True,  # 允许上传多个文件
            ),
        ]),

        html.Div(id='output-data-upload'),

        dcc.Graph(id='data-graph'),
    ])

    # 回调函数用于处理文件上传并加载数据
    @app.callback(
        Output('output-data-upload', 'children'),
        [Input('upload-data', 'contents')]
    )
def update_output(contents):
    if contents is not None:
        children = []
        # 读取数据文件并显示文件名
        for i, content in enumerate(contents):
            children.append(html.Div([
                '文件{}: {}'.format(i+1, content['filename'])
            ]))
        return children
    else:
        return '未上传文件'

    # 回调函数用于根据上传的文件生成图表
    @app.callback(
        Output('data-graph', 'figure'),
        [Input('upload-data', 'contents')],
    )
def update_graph(contents):
        if contents is not None:
            # 读取第一个文件内容
            uploaded_file = contents[0]['content']
            # 将文件内容转换为pandas DataFrame
            df = pd.read_csv(pd.compat.StringIO(uploaded_file.decode('utf-8')))
            # 使用Plotly Express生成图表
            fig = px.histogram(df, x=df.columns[0])
            return fig
        else:
            return {
                'layout': {"margin": {"l": 50, "r": 50, "b": 100, "t": 100}},
                'data': [{'x': [], 'y': [], 'type': 'bar'}]
            }

    # 运行应用
    if __name__ == '__main__':
        app.run_server(debug=True)

# 调用应用入口函数
create_dashboard()