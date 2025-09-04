# 代码生成时间: 2025-09-05 05:03:02
import os
import shutil
import logging
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# 配置日志
logging.basicConfig(level=logging.INFO)

# 定义全局变量
SOURCE_DIR = '/path/to/source'  # 源文件夹路径
DEST_DIR = '/path/to/destination'  # 目标文件夹路径

# 函数：备份文件
def backup_files(src, dest):
    try:
        # 检查源文件夹和目标文件夹是否存在
        if not os.path.exists(src):
            logging.error(f"Source directory does not exist: {src}")
            return False
        if not os.path.exists(dest):
            os.makedirs(dest)
            logging.info(f"Created destination directory: {dest}")
        
        # 遍历源文件夹中的文件
        for filename in os.listdir(src):
            file_path = os.path.join(src, filename)
            
            # 如果是文件则复制到目标文件夹
            if os.path.isfile(file_path):
                dest_path = os.path.join(dest, filename)
                shutil.copy2(file_path, dest_path)
                logging.info(f"Copied file: {filename}")
        
        # 返回备份成功
        return True
    except Exception as e:
        logging.error(f"Error occurred during backup: {e}")
        return False

# 函数：同步文件
def sync_files(src, dest):
    try:
        # 检查源文件夹和目标文件夹是否存在
        if not os.path.exists(src):
            logging.error(f"Source directory does not exist: {src}")
            return False
        if not os.path.exists(dest):
            logging.error(f"Destination directory does not exist: {dest}")
            return False
        
        # 获取源文件夹和目标文件夹中的文件
        src_files = set(os.listdir(src))
        dest_files = set(os.listdir(dest))
        
        # 同步文件
        for file in src_files:
            if file not in dest_files:
                file_path = os.path.join(src, file)
                dest_path = os.path.join(dest, file)
                shutil.copy2(file_path, dest_path)
                logging.info(f"Synced file: {file}")
            
        for file in dest_files:
            if file not in src_files:
                file_path = os.path.join(dest, file)
                os.remove(file_path)
                logging.info(f"Removed file: {file}")
        
        # 返回同步成功
        return True
    except Exception as e:
        logging.error(f"Error occurred during sync: {e}")
        return False

# DASH界面
app = Dash(__name__)

# 布局
app.layout = html.Div([
    html.H1("File Backup and Sync Tool"),
    html.Button("Backup Files", id="backup-button"),
    html.Button("Sync Files", id="sync-button"),
    dcc.Output("output", "children")
])

# 回调函数：备份文件
@app.callback(
    Output("output", "children"),
    [Input("backup-button", "n_clicks"), Input("sync-button", "n_clicks")]
)
def backup_sync(backup_clicks, sync_clicks):
    # 重置输出
    output = ""
    
    # 检查备份按钮点击
    if backup_clicks:
        backup_success = backup_files(SOURCE_DIR, DEST_DIR)
        if backup_success:
            output += "Backup successful.
"
        else:
            output += "Backup failed.
"
    
    # 检查同步按钮点击
    if sync_clicks:
        sync_success = sync_files(SOURCE_DIR, DEST_DIR)
        if sync_success:
            output += "Sync successful.
"
        else:
            output += "Sync failed.
"
            
    return output

# 运行DASH应用
if __name__ == '__main__':
    app.run_server(debug=True)