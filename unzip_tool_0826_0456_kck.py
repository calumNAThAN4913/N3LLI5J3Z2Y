# 代码生成时间: 2025-08-26 04:56:53
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import zipfile
import os
from werkzeug.utils import secure_filename

# 定义一个函数来解压文件
def unzip_file(file_path, extract_to):
    """解压ZIP文件到指定目录"""
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return f'Files extracted to {extract_to}
'
    except zipfile.BadZipFile:
        return 'File is not a zip file or it is corrupted.'
    except Exception as e:
        return f'An error occurred: {str(e)}
'

# 初始化Dash应用
def init_dash_app():
    # 创建Dash应用实例
    app = dash.Dash(__name__)

    # 设置布局
    app.layout = html.Div(
        children=[
            html.H1(children='File Unzip Tool'),
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                multiple=True,
                # 允许上传的文件类型
                accept multiple=['.zip']
            ),
            html.Div(id='output-data-upload'),
        ]
    )

    # 定义回调函数，处理文件上传和解压
    @app.callback(
        Output('output-data-upload', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename'),
         State('upload-data', 'last_modified')]
    )
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            # 文件上传后，保存到临时目录
            temp_folder = 'temp_folder'
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            # 解压文件并返回解压信息
            message = ''
            for i, content in enumerate(list_of_contents):
                filename = list_of_names[i]
                file_path = os.path.join(temp_folder, secure_filename(filename))
                with open(file_path, 'wb') as file:
                    file.write(content)
                message += f'Unzipping {filename}: {unzip_file(file_path, temp_folder)}'
            return html.Div([dcc.Markdown(message)])
        else:
            return html.Div(['No file uploaded'])

    return app

# 运行Dash应用
def run_app():
    app = init_dash_app()
    app.run_server(debug=True)

# 入口点
def main():
    run_app()

if __name__ == '__main__':
    main()