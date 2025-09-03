# 代码生成时间: 2025-09-03 15:37:05
import os
import shutil
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# 设置 Dash 应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 设置布局
app.layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(html.H1('Data Backup and Recovery'), width=12),
            ],
        ),
        dbc.Row(
            children=[
                dbc.Col(dcc.Upload(id='upload-data', children=html.Div('Drag and Drop or Select Files'),
                                style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}), width=12),
            ],
        ),
        dbc.Row(
            children=[
                dbc.Col(html.Button('Backup', id='backup-button', n_clicks=0), width=6),
                dbc.Col(html.Button('Restore', id='restore-button', n_clicks=0), width=6),
            ],
        ),
    ],
)

# 定义回调函数
@app.callback(
    Output('backup-button', 'children'),
    Input('backup-button', 'n_clicks'),
    prevent_initial_call=True,
)
def backup_data(n_clicks):
    # 检查是否有文件上传
    if n_clicks == 0:
        return 'Backup'

    # 获取上传的文件
    upload_id = 'upload-data'
    uploaded_file = dash.callback_context.inputs[upload_id][0]
    if uploaded_file is None:
        raise PreventUpdate

    # 获取文件名
    filename = uploaded_file.filename
    if not filename:
        raise PreventUpdate

    # 保存文件
    file_path = os.path.join('backup', filename)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.value)

    return 'Backup Successful'


@app.callback(
    Output('restore-button', 'children'),
    Input('restore-button', 'n_clicks'),
    prevent_initial_call=True,
)
def restore_data(n_clicks):
    # 检查是否有文件上传
    if n_clicks == 0:
        return 'Restore'

    # 获取上传的文件
    upload_id = 'upload-data'
    uploaded_file = dash.callback_context.inputs[upload_id][0]
    if uploaded_file is None:
        raise PreventUpdate

    # 获取文件名
    filename = uploaded_file.filename
    if not filename:
        raise PreventUpdate

    # 恢复文件
    file_path = os.path.join('backup', filename)
    if not os.path.isfile(file_path):
        raise PreventUpdate

    with open(file_path, 'rb') as f:
        file_content = f.read()

    # 保存文件到当前目录
    restore_file_path = os.path.join(os.getcwd(), filename)
    with open(restore_file_path, 'wb') as f:
        f.write(file_content)

    return 'Restore Successful'

if __name__ == '__main__':
    app.run_server(debug=True)
