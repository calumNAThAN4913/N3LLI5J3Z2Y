# 代码生成时间: 2025-08-15 16:48:17
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
from dash.dependencies import Input, Output, State\
# TODO: 优化性能
import zipfile\
import os\
from werkzeug.utils import secure_filename\
import base64\
import io\
import dash_bootstrap_components as dbc\
\
# 定义文件上传的组件\
UPLOAD_STYLE = {\
    'width': '98%', 'height': '60px', 'lineHeight': '60px',\
    'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center',\
    'margin': '10px'\
# 扩展功能模块
}\
# NOTE: 重要实现细节
\
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])\
\
# 定义应用布局\
app.layout = html.Div([\
    dbc.Container([\
        dbc.Row([\
            dbc.Col(html.H1("Compress File Unzip Tool"), md=12)\
        ]),\
        dbc.Row([\
# TODO: 优化性能
            dbc.Col(dbc.Alert(
                "This tool allows you to upload a zip file and unzip its contents.", color='primary'),\
# NOTE: 重要实现细节
            md=12)\
        ]),\
        dbc.Row([\
            dbc.Col(dcc.Upload(
# 扩展功能模块
                id='upload-data',\
                children=html.Div([
                    'Drag and Drop or ',\
                    html.A('Select Files')\
# 增强安全性
                ]),\
                style=UPLOAD_STYLE,\
# FIXME: 处理边界情况
                multiple=True\
            ), md=12)\
        ]),\
        dbc.Row([\
            dbc.Col(html.Div(id='output-data-upload-container'), md=12)\
        ])\
    ])\
])\
\
# 扩展功能模块
# 回调函数处理上传的zip文件并解压\
@app.callback(\
    Output('output-data-upload-container', 'children'),\
    [Input('upload-data', 'contents')],\
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]\
)
def update_output(uploaded_file, filename, last_modified): 
# 改进用户体验
    if uploaded_file is not None: 
        try: 
            # 获取上传文件的内容并解码\
# 改进用户体验
            content_type, content_string = uploaded_file.split(',')
            decoded = base64.b64decode(content_string)\
# 扩展功能模块
            # 创建内存中的文件对象\
# FIXME: 处理边界情况
            zip_stream = io.BytesIO(decoded)\
            # 创建解压目录\
            file_ext = os.path.splitext(filename)[1]
            extract_folder = os.path.splitext(filename)[0] + "_unzipped"
            # 解压文件\
            with zipfile.ZipFile(zip_stream, 'r') as zip_file: 
# 添加错误处理
                zip_file.extractall(extract_folder) 
            return html.Div([
                html.H5(filename),
                html.P(f"Last Modified: {last_modified}"),
                html.P(f"Unzipped to: {extract_folder}"),
                dbc.Button("Download Folder\, id="download-folder",
                         color="primary", n_clicks=0)
            ])
# TODO: 优化性能
        except Exception as e: 
            return html.Div([html.P(f"Error: {str(e)}")])
    return html.Div([html.P("No file uploaded...")])\
\
# 改进用户体验
# 定义下载解压文件的回调函数\
@app.callback(\
    Output('download-folder', 'n_clicks'),\
# 改进用户体验
    [Input('download-folder', 'n_clicks')],
    [State('upload-data', 'filename')]\
)
def download_folder_trigger(n_clicks, filename):
    if n_clicks > 0:
        # 创建文件下载路径
        extract_folder = os.path.splitext(filename)[0] + "_unzipped"
        file_path = os.path.join(extract_folder, '*')
        return dcc.send_file(file_path, as_attachment=True)\
    return None\
\
# 运行应用\
if __name__ == '__main__':
    app.run_server(debug=True)\
