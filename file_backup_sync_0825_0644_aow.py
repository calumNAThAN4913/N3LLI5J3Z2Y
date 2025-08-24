# 代码生成时间: 2025-08-25 06:44:29
import os
import shutil
import logging
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 文件备份和同步工具
class FileBackupSyncTool:
    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.file_list = []

    def list_files(self):
        """列出源目录下的所有文件"""
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                self.file_list.append(os.path.join(root, file))
        logger.info(f"Found {len(self.file_list)} files in {self.source_dir}")
        return self.file_list

    def backup_files(self):
        """备份文件到目标目录"""
        for file in self.file_list:
            shutil.copy2(file, self.target_dir)
            logger.info(f"Backup {file} to {self.target_dir}")

    def sync_files(self):
        """同步文件到目标目录"""
        for file in self.file_list:
            shutil.copy2(file, self.target_dir)
            logger.info(f"Sync {file} to {self.target_dir}")

    def remove_unused_files(self):
        """删除目标目录中不再存在的文件"""
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in [os.path.join(self.source_dir, f) for f in self.file_list]:
                    os.remove(file_path)
                    logger.info(f"Remove {file_path}")

    def run_backup_sync(self):
        """运行备份和同步操作"""
        try:
            self.list_files()
            self.backup_files()
            self.sync_files()
            self.remove_unused_files()
            logger.info("Backup and sync completed successfully")
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")

# 创建Dash应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Container([
        html.H1("File Backup and Sync Tool"),
        dcc.Upload(
            id="upload-source-dir",
            children=html.Div(["Drag and Drop or ", html.A("Select File")]),
            max_size=5000000,
            multiple=True
        ),
        dcc.Upload(
            id="upload-target-dir",
            children=html.Div(["Drag and Drop or ", html.A("Select File\)]),
            max_size=5000000,
            multiple=True
        ),
        html.Button("Run Backup and Sync", id="run-btn", n_clicks=0),
        html.Div(id="output")
    ])
])

@app.callback(
    Output("output", "children"),
    [Input("upload-source-dir", "contents"), Input("upload-target-dir", "contents")],
    [State("upload-source-dir", "filename"), State("upload-target-dir", "filename")]
)
def run_backup_sync(contents_source, contents_target, filename_source, filename_target):
    if contents_source and contents_target:
        try:
            content_type_source = contents_source[0]['content_type']
            content_type_target = contents_target[0]['content_type']
            if content_type_source != "text/plain" or content_type_target != "text/plain":
                return "Invalid file type, please upload .txt files."
            source_dir = contents_source[0]['name']
            target_dir = contents_target[0]['name']
            with open(source_dir, "wb") as f:
                f.write(contents_source[0]['content'])
            with open(target_dir, "wb") as f:
                f.write(contents_target[0]['content'])
            tool = FileBackupSyncTool(source_dir, target_dir)
            tool.run_backup_sync()
            return "Backup and sync completed successfully."
        except Exception as e:
            return f"Error occurred: {str(e)}."
    return "Please upload both source and target directories."

if __name__ == '__main__':
    app.run_server(debug=True)