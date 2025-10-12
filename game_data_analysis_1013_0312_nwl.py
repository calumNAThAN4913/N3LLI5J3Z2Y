# 代码生成时间: 2025-10-13 03:12:23
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 游戏数据分析Dash应用程序
class GameDataAnalysisApp:
    def __init__(self, server):
        # 初始化Dash应用程序
        self.app = dash.Dash(__name__, server=server)

        # 定义应用程序的布局
        self.app.layout = html.Div([
            html.H1("游戏数据分析"),
            dcc.Graph(id="game-statistics-graph"),  # 用于显示游戏统计数据的图形元素
            dcc.Upload(
                id='upload-data',
                children=html.Button('上传游戏数据'),
                multiple=False  # 允许上传多个文件
            )
        ])

        # 定义回调函数
        @self.app.callback(
           Output('game-statistics-graph', 'figure'),
           Input('upload-data', 'contents'),
           Input('upload-data', 'filename'),
           prevent_initial_call=True  # 阻止初始调用
        )
        def update_graph(contents, filename):
            if contents is not None:
                # 解析上传的数据
                content_type, content_string = contents.split(',')
                if 'csv' in filename:
                    # 读取CSV文件
                    df = pd.read_csv(pd.compat.StringIO(content_string))
                elif 'xls' in filename:
                    # 读取Excel文件
                    df = pd.read_excel(pd.compat.StringIO(content_string))
                else:
                    # 错误处理：不支持的文件格式
                    raise Exception("不支持的文件格式。请上传CSV或Excel文件。")

                # 数据分析和可视化
                fig = px.bar(df, x="level", y="score", title='游戏得分分析')
                return fig
            else:
                # 如果没有上传数据，则返回空图形
                return go.Figure()

    # 运行应用程序
def run_server():
    # 从Flask服务器创建Dash应用程序并运行
    server = GameDataAnalysisApp("http://127.0.0.1:8050/")
    server.run_server(debug=True)

# 主函数入口
def main():
    run_server()

if __name__ == "__main__":
    main()