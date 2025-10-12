# 代码生成时间: 2025-10-12 23:58:48
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import Flask
import plotly.express as px
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import base64
import io
from PIL import Image
from io import BytesIO
import numpy as np

# 初始化Dash应用
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# 模型加载函数
def load_model(model_path):
    model = pickle.load(open(model_path, 'rb'))
    return model

# 假设模型路径
model_path = 'model.pkl'
model = load_model(model_path)

# 应用布局
app.layout = html.Div(children=[
    html.H1(children='Model Deployment Tool'),
    html.Div(children='''
        Upload a CSV file and select the target column to visualize the predictions.
    '''),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select a CSV File')]),
        style={'width': '50%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
        # 允许上传多个文件
        multiple=True
    ),
    dcc.Dropdown(
        id='column-selector',
        options=[{'label': i, 'value': i} for i in ['Column1', 'Column2', 'Column3']],  # 示例列名
        value='Column1'  # 默认选择
    ),
    dcc.Graph(id='predictions-plot')
])

# 回调函数处理上传的文件并更新图表
@app.callback(Output('predictions-plot', 'figure'),
              [Input('upload-data', 'contents')],
              [State('column-selector', 'value'), State('upload-data', 'filename')])
def update_output(contents, column, filename):  # 定义回调函数
    if contents is None:  # 检查是否上传了文件
        raise PreventUpdate
    
    # 解析上传的文件
    if filename:
        print(f'File {filename} has been uploaded.')
        contents = contents.split(',')
        # 获取文件名
        file = contents[0].split(';')[1]
        # 将文件内容转换为二进制流
        data = base64.b64decode(file)
        # 使用BytesIO读取二进制流中的文件
        df = pd.read_csv(io.StringIO(data.decode('utf-8')))

        # 进行模型预测
        predictions = model.predict(df[column].values.reshape(-1, 1))

        # 将预测结果添加到DataFrame中
        predictions_df = df.copy()
        predictions_df['Predicted'] = predictions

        # 绘制预测结果图表
        fig = px.scatter(predictions_df, x=column, y='Predicted')
        fig.update_layout(title='Predictions Plot', xaxis_title=column, yaxis_title='Predicted')

        return fig
    else:
        return px.scatter(pd.DataFrame(), x='Column1', y='Predicted')


# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
