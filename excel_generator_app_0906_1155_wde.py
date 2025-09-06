# 代码生成时间: 2025-09-06 11:55:37
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from dash import no_update
import base64
import io
import os
from datetime import datetime
import xlsxwriter

def generate_excel(df):
    # 存储Excel文件的内存缓冲区
    output = io.BytesIO()
    # 创建一个Excel写入器
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    # 将DataFrame写入Excel文件
    df.to_excel(writer, index=False)
    # 保存Excel文件
    writer.save()
    # 将内存缓冲区转换为Base64编码字符串
    output.seek(0)
    return base64.b64encode(output.getvalue()).decode('utf-8')

def parse_contents(contents, filename):
    # 尝试解析文件内容
    try:
        contents = contents.split(',')[1]
        df = pd.read_excel(io.BytesIO(base64.b64decode(contents)))
    except Exception as e:
        print(e)
        df = pd.DataFrame()
    return df

def serve_layout():
    # Dash应用布局
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ',
                            html.A('Select Files'),
                            html.Span(id='output-data-upload'),
                            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
            },
            # 允许上传Excel文件
            accept=r'.csv, .xls, .xlsx',
        ),
        html.Div(id='output-container'),
    ])

def callback(app):
    @app.callback(
        Output('output-container', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')])
def generate_output(uploaded_contents, filename):
        # 检查是否有文件上传
        if uploaded_contents is None or filename is None:
            raise PreventUpdate
        # 解析文件内容
        df = parse_contents(uploaded_contents, filename)
        # 生成Excel文件
        excel = generate_excel(df)
        # 创建下载链接
        return html.A(
            'Download Excel',
            href='data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{}'.format(excel),
            download= '{}.xlsx'.format(os.path.splitext(os.path.basename(filename))[0]),
        )
def main():
    # 初始化Dash应用
    app = dash.Dash(__name__)
def serve_layout(app):
    app.layout = html.Div([
        serve_layout()
    ])
def callback(app):
    generate_output(uploaded_contents, filename)
    # 运行Dash服务器
    if __name__ == '__main__':
        main()
        app.run_server(debug=True)
