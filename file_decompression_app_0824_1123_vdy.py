# 代码生成时间: 2025-08-24 11:23:27
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import zipfile
import os
from werkzeug.utils import secure_filename
import base64

# 定义应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(children=[
    html.H1('文件压缩解压工具'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['点击上传文件', html.Span(id='upload-text', style={'color': 'red'})]),
        style={'width': '50%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
        # 允许上传的文件类型
        accept='.zip, .rar, .tar.gz, .gz, .7z',
    ),
    html.Button('解压文件', id='extract-button', n_clicks=0),
    dcc.Download(id='download-button'),
    dcc.Graph(id='output-data-upload')
])

# 定义回调函数，处理文件上传
@app.callback(
    Output('upload-text', 'children'),
    [Input('upload-data', 'filename')],
)
def update_output(uploaded_filename):
    if uploaded_filename is not None:
        return f'文件已上传：{uploaded_filename}'
    else:
        return '文件尚未上传'

# 定义回调函数，处理文件解压
@app.callback(
    Output('output-data-upload', 'figure'),
    [Input('extract-button', 'n_clicks'),
     State('upload-data', 'contents')],
)
def extract_file(n_clicks, contents):
    if n_clicks > 0 and contents is not None:
        # 解析文件内容
        file_name = contents.filename
        content_type = contents.content_type
        # 判断文件类型
        if 'zip' in file_name:
            return extract_zip_file(contents)
        else:
            return {'layout': {'xaxis': {'type': 'category'}, 'yaxis': {'type': 'linear'}}}
    return {'layout': {'xaxis': {'type': 'category'}, 'yaxis': {'type': 'linear'}}}

# 解压zip文件
def extract_zip_file(contents):
    try:
        # 将文件内容转换为字节流
        zip_file = base64.b64decode(contents.data[23:])
        # 创建临时文件夹
        temp_folder = os.path.join('temp', secure_filename(contents.filename))
        os.makedirs(temp_folder, exist_ok=True)
        # 解压文件
        with zipfile.ZipFile(BytesIO(zip_file)) as zfile:
            zfile.extractall(temp_folder)
        # 获取解压后的文件
        files = [os.path.join(temp_folder, f) for f in os.listdir(temp_folder)]
        # 返回文件列表
        return {'data': [{'x': [f.split('/')[-1] for f in files], 'y': [os.path.getsize(f) for f in files]}], 'layout': {'title': '解压文件列表'}}
    except Exception as e:
        print(f'解压文件失败：{e}')
        return {'data': [], 'layout': {'title': '解压文件失败'}}

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
