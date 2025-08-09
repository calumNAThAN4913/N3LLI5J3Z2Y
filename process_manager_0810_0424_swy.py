# 代码生成时间: 2025-08-10 04:24:39
import dash
import dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import psutil
from dash.exceptions import PreventUpdate

# 定义Dash应用程序
app = dash.Dash(__name__)
app.title = 'Process Manager'

# 设置Dash应用程序外部样式和内部样式
app = dash.Dash(external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])

# 设置Dash应用程序的布局
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Button("Refresh", id="refresh-button", color="success"), width=4),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        id="process-table",
                        columns=[
                            {"name": i, "id": i} for i in ["PID", "Process Name", "CPU Usage", "Memory Usage"]
                        ],
                        data=[],
                        sort_action="native",
                        filter_action="native",
                    ),
                ),
            ],
        ),
    ],
    fluid=True,
)

# 定义回调函数，用于更新进程信息
@app.callback(
    Output("process-table", "data"),
    [Input("refresh-button", "n_clicks")],
    [State("process-table", "data")],
)
def update_process_info(n_clicks, table_data):
    if n_clicks is None:
        raise PreventUpdate
    
    # 获取当前系统的所有进程信息
    processes = [proc for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])]
    
    # 将进程信息转换为DataFrame
    process_df = pd.DataFrame(processes, columns=['PID', 'Process Name', 'CPU Usage', 'Memory Usage'])
    
    # 格式化CPU和内存使用率
    process_df['CPU Usage'] = process_df['CPU Usage'].map('{:.2f}%'.format)
    process_df['Memory Usage'] = process_df['Memory Usage'].map('{:.2f}%'.format)
    
    # 更新表格数据
    return process_df.to_dict('records')

# 运行Dash应用程序
def run():
    app.run_server(debug=True)

# 如果直接运行该脚本，则启动Dash应用程序
def main():
    if __name__ == '__main__':
        run()

# 调用main函数
if __name__ == '__main__':
    main()
