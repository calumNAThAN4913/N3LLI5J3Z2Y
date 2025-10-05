# 代码生成时间: 2025-10-05 21:09:56
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import base64
import io
import os
from flask import send_file, safe_join
from werkzeug.utils import secure_filename

# 定义一个二进制文件读写工具应用
class BinaryFileTool:
    def __init__(self, app):
        # 初始化应用程序
        self.app = app
        self.layout = html.Div([
            html.H1("二进制文件读写工具"),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=True
            ),
            html.Div(id='output-data-upload')
        ])
        # 设置布局
        app.layout = self.layout

    def callback(self):
        # 定义回调函数
        @app.callback(
            Output('output-data-upload', 'children'),
            [Input('upload-data', 'contents')],
            [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
        )
        def update_output(
            list_of_contents, list_of_names, list_of_dates):
            # 读取文件内容并返回
            if list_of_contents is not None:
                children = []
                for content, name, date in zip(list_of_contents, list_of_names, list_of_dates):
                    # 检查文件类型
                    if name.endswith('.bin') or name.endswith('.dat'):
                        try:
                            # 读取二进制文件内容
                            contents = base64.b64decode(content.split(',')[1])
                            with open('temp.bin', 'wb') as f:
                                f.write(contents)
                            # 读取文件内容并返回
                            with open('temp.bin', 'rb') as f:
                                data = f.read()
                                children.append(
                                    html.Div([
                                        html.H5(name),
                                        html.P(f'Last Modified: {date}'),
                                        html.P('File Size: {} bytes'.format(len(data))),
                                        dcc.Graph(
                                            id='graph-{}'.format(name),
                                            figure=px.bar(x=range(len(data)), y=[byte for byte in data])
                                        )
                                    ])
                                )
                        except Exception as e:
                            children.append(html.P(f'Error reading file {name}: {str(e)}'))
                    else:
                        children.append(html.P(f'File {name} is not a binary file'))
                return children
            else:
                return html.P('No file uploaded')

    def run_server(self):
        # 运行服务器
        if __name__ == '__main__':
            self.app.run_server(debug=True)

# 创建Dash应用程序
app = dash.Dash(__name__)

# 初始化二进制文件读写工具应用
binary_file_tool = BinaryFileTool(app)

# 定义回调函数
binary_file_tool.callback()

# 运行服务器
binary_file_tool.run_server()