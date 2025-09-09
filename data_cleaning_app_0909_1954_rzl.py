# 代码生成时间: 2025-09-09 19:54:27
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from urllib.parse import quote_plus
import base64
from io import BytesIO

# 定义Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(children=[
    html.H1(children='数据清洗和预处理工具'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ',
                         html.A('Select Files')],
                         id='upload-data-text'),
        # 允许上传文件类型
        description='',
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(children=[
        html.Button('预处理数据', id='preprocess-button', n_clicks=0),
        html.Div(id='preprocess-output')
    ])
])

# 回调函数：处理文件上传
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')]
)
def update_output(*args, **kwargs):
    if args[0] is not None:
        # 解码文件内容
        content_type, content_string = args[0].split(',')
        decoded = base64.b64decode(content_string)
        try:
            # 读取文件内容为DataFrame
            df = pd.read_csv(BytesIO(decoded))
            df.head().to_string()
            return html.Div([
                html.H5('数据预览：'),
                html.Table([html.Tr([html.Th(col) for col in df.columns])] +
                          [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(len(df), 5))]),
                html.Button('上传成功，点击预处理', id='preprocess-button', n_clicks=0),
                html.Div(id='preprocess-output')
            ])
        except Exception as e:
            print(e)
            return html.Div([html.H6('文件读取失败，请检查文件格式')])
    else:
        return html.Div([html.H6('请上传数据文件')])

# 回调函数：执行数据预处理
@app.callback(
    Output('preprocess-output', 'children'),
    [Input('preprocess-button', 'n_clicks')],
    [State('upload-data', 'contents')]
)
def preprocess_data(n_clicks, contents):
    if n_clicks > 0 and contents is not None:
        # 解码文件内容
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # 读取文件内容为DataFrame
            df = pd.read_csv(BytesIO(decoded))
            # 数据预处理
            # 例如：删除缺失值
            df = df.dropna()
            # 显示预处理后的数据
            return html.Div([
                html.H5('预处理后的数据：'),
                dcc.Download(
                    id='download-preprocessed-data',
                    children=html.A('下载预处理后的数据'),
                    href='data:text/csv;charset=utf-8,' + quote_plus(str(df.to_csv(index=False))),
                    download='preprocessed_data.csv'
                )
            ])
        except Exception as e:
            print(e)
            return html.Div([html.H6('数据预处理失败，请检查文件格式')])
    return html.Div([])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)