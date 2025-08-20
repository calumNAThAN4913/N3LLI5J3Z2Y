# 代码生成时间: 2025-08-20 10:28:11
import os
import shutil
from datetime import datetime
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

"""
文件备份和同步工具，使用DASH框架实现图形界面
==============================================

功能：
- 选择源文件夹和目标文件夹
- 备份和同步源文件夹中的文件到目标文件夹
- 显示备份和同步的进度和结果
"""

# 初始化DASH应用程序
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义布局
app.layout = dbc.Container(
    style={"padding": "20px"},
    children=[
        dbc.Row(
            dbc.Col(
                dbc.Input(id="source-folder", placeholder="选择源文件夹"),
                md=6,
            ),
            dbc.Col(
                dbc.Input(id="target-folder", placeholder="选择目标文件夹"),
                md=6,
            ),
        ),
        dbc.Button("备份和同步", id="backup-sync-button", color="primary"),
        dcc.Output("output-data-upload", id="backup-sync-output"),
    ],
)

# 定义回调函数
@app.callback(
    Output("backup-sync-output", "children"),
    [Input("backup-sync-button", "n_clicks")],
)
def backup_and_sync(n_clicks):
    if n_clicks is None:
        return None

    # 获取源文件夹和目标文件夹路径
    source_folder = os.path.abspath(dbc.Input(id="source-folder").value)
    target_folder = os.path.abspath(dbc.Input(id="target-folder").value)

    # 检查文件夹路径是否有效
    if not os.path.isdir(source_folder):
        return "源文件夹路径无效"
    if not os.path.isdir(target_folder):
        return "目标文件夹路径无效"

    try:
        # 创建备份文件
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        backup_folder = os.path.join(target_folder, backup_name)
        os.makedirs(backup_folder, exist_ok=True)
        shutil.copytree(source_folder, backup_folder)

        # 同步文件
        for filename in os.listdir(source_folder):
            source_file = os.path.join(source_folder, filename)
            target_file = os.path.join(target_folder, filename)
            if os.path.isfile(source_file):
                if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                    shutil.copy2(source_file, target_file)

        # 返回结果
        return f"备份和同步完成：{backup_folder}"
    except Exception as e:
        # 错误处理
        return f"备份和同步失败：{str(e)}"

# 运行DASH应用程序
if __name__ == '__main__':
    app.run_server(debug=True)
