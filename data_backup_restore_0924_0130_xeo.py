# 代码生成时间: 2025-09-24 01:30:32
import os
import json
import shutil
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_extensions.snippet import send_file

# 配置文件路径
CONFIG = {
    "backup_path": "./backups",
    "data_path": "./data",
}

# 检查备份路径是否存在，如果不存在则创建
if not os.path.exists(CONFIG["backup_path"]):
    os.makedirs(CONFIG["backup_path"])

# 应用布局
app = Dash(__name__)
app.layout = html.Div([
    html.H1("数据备份与恢复系统"),
    html.Button("备份数据", id="backup-button"),
    html.Button("恢复数据", id="restore-button"),
    dcc.Download(id="download-link"),
])

# 回调函数：备份数据
@app.callback(
    Output("download-link", "data"),
    [Input("backup-button", "n_clicks")],
    [State("download-link", "filename"), State("download-link", "data")],
)
def backup_data(n_clicks, filename, data):
    if n_clicks is None or n_clicks < 0:
        raise PreventUpdate
    try:
        # 将数据备份到备份文件夹
        backup_file_path = os.path.join(CONFIG["backup_path"], "backup_" + str(n_clicks) + ".json")
        with open(CONFIG["data_path"] + "/data.json", "r") as file:
            data = json.load(file)
        with open(backup_file_path, "w") as file:
            json.dump(data, file)
        # 返回备份文件供下载
        return send_file(backup_file_path)
    except Exception as e:
        raise PreventUpdate

# 回调函数：恢复数据
@app.callback(
    Output("download-link", "data"),
    [Input("restore-button", "n_clicks")],
    [State("download-link", "filename"), State("download-link", "data")],
)
def restore_data(n_clicks, filename, data):
    if n_clicks is None or n_clicks < 0:
        raise PreventUpdate
    try:
        # 获取备份文件列表
        backup_files = [f for f in os.listdir(CONFIG["backup_path"]) if f.endswith(".json")]
        if not backup_files:
            raise Exception("没有找到备份文件")
        # 恢复最后一个备份文件
        backup_file_path = os.path.join(CONFIG["backup_path"], backup_files[-1])
        with open(backup_file_path, "r") as file:
            data = json.load(file)
        with open(CONFIG["data_path"] + "/data.json", "w") as file:
            json.dump(data, file)
        # 返回恢复成功消息
        return send_file("恢复成功.txt", "text/plain", "恢复成功")
    except Exception as e:
        raise PreventUpdate

if __name__ == "__main__":
    app.run_server(debug=True)