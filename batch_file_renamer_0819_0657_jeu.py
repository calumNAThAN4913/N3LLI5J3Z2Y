# 代码生成时间: 2025-08-19 06:57:42
import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import re

# 定义批量重命名工具的类
class BatchFileRenamer:
    def __init__(self, directory):
        """
        初始化BatchFileRenamer对象
        :param directory: 需要重命名的文件所在的目录
        """
        self.directory = directory
        self.files = os.listdir(directory)

    def rename_files(self, prefix, suffix):
        """
        批量重命名文件
        :param prefix: 新文件名的前缀
        :param suffix: 新文件名的后缀（不含扩展名）
        """
        for i, filename in enumerate(self.files):
            basename, extension = os.path.splitext(filename)
            new_name = f"{prefix}_{i+1:03d}{suffix}.{extension}"
            try:
                os.rename(os.path.join(self.directory, filename), 
                          os.path.join(self.directory, new_name))
            except OSError as e:
                print(f"Error renaming {filename}: {e}")

# 创建Dash应用程序
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Upload(
        id='upload-directory',
        children=html.Button('Upload Directory'),
        multiple=False,
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
    ),
    html.Div(id='output-data')
])

# 回调函数处理文件上传和重命名操作
@app.callback(
    Output('output-data', 'children'),
    Input('upload-directory', 'contents'))
def process_contents(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = content_type, base64.b64decode(content_string).decode('utf-8')
        directory = base64.b64decode(content_string).decode('utf-8')
        renamer = BatchFileRenamer(directory)
        prefix = input("Enter new file prefix: ")
        suffix = input("Enter new file suffix (without extension): ")
        renamer.rename_files(prefix, suffix)
        return f'Files renamed in {directory}'
    else:
        return html.Div()

if __name__ == '__main__':
    app.run_server(debug=True)