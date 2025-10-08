# 代码生成时间: 2025-10-08 20:25:44
import os
import tempfile
from datetime import datetime, timedelta
from dash import Dash, html, Input, Output

# 配置Dash应用
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Temporary File Cleaner"),
    html.Button("Clean Temporary Files", id="clean-button"),
    html.Div(id="output")
])

# 清理临时文件夹中过期文件的函数
def clean_temporary_files():
    # 获取系统临时文件夹路径
    temp_dir = tempfile.gettempdir()
    # 获取当前时间
    now = datetime.now()
    # 定义过期时间阈值（例如：1天）
    threshold = now - timedelta(days=1)
    
    # 遍历临时文件夹中的文件
    for filename in os.listdir(temp_dir):
        # 构建完整的文件路径
        file_path = os.path.join(temp_dir, filename)
        
        # 检查文件是否是普通文件且修改时间早于阈值
        if os.path.isfile(file_path) and os.path.getmtime(file_path) < threshold.timestamp():
            try:
                # 删除文件
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                # 处理删除文件时可能发生的异常
                print(f"Error deleting {file_path}: {e}")

# 回调函数，当点击清理按钮时，清理临时文件并显示结果
@app.callback(
    Output("output", "children"),
    [Input("clean-button", "n_clicks")]
)
def clean_files(n_clicks):
    if n_clicks is None:
        return "Click the button to clean temporary files."
    else:
        try:
            clean_temporary_files()
            return "Temporary files cleaned successfully."
        except Exception as e:
            return f"An error occurred: {e}"

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
