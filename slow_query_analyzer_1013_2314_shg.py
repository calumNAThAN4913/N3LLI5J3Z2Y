# 代码生成时间: 2025-10-13 23:14:57
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# 定义慢查询分析器类
class SlowQueryAnalyzer:
    def __init__(self, file_path):
        """
        初始化慢查询分析器
        :param file_path: 慢查询日志文件路径
        """
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

    def analyze(self, threshold):
        """
        分析慢查询
        :param threshold: 慢查询时间阈值（单位：秒）
        :return: 慢查询数据框
        """
        try:
            slow_queries = self.data[self.data['duration'] > threshold]
            return slow_queries
        except KeyError:
            print("Error: 'duration' column not found in the log file.")
            return None

    def to_dataframe(self):
        """
        将慢查询数据转换为数据框
        :return: 慢查询数据框
        """
        return self.data

# 创建Dash应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义布局
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("慢查询分析器"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("慢查询日志文件路径: "), width=3),
        dbc.Col(html.Input(id='file-path', type='text'), width=6),
        dbc.Col(html.Button("上传文件", id='upload-button', n_clicks=0), width=3)
    ]),
    dbc.Row([
        dbc.Col(html.P("慢查询时间阈值（秒）: "), width=3),
        dbc.Col(dcc.Input(id='threshold', type='number', value=10), width=6),
        dbc.Col(html.Button("分析慢查询", id='analyze-button', n_clicks=0), width=3)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='slow-query-graph'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Table(id='slow-query-table', filter_action="native"), width=12)
    ])
])

# 回调函数：上传文件
@app.callback(
    Output('file-path', 'value'),
    [Input('upload-button', 'n_clicks')],
    prevent_initial_call=True
)
def upload_file(n_clicks):
    if n_clicks > 0:
        return "/path/to/slow_query_log.csv"  # 替换为实际文件路径
    return None

# 回调函数：分析慢查询
@app.callback(
    Output('slow-query-table', 'data'),
    [Input('analyze-button', 'n_clicks')],
    [State('file-path', 'value'), State('threshold', 'value')],
    prevent_initial_call=True
)
def analyze_slow_queries(n_clicks, file_path, threshold):
    if n_clicks > 0:
        try:
            analyzer = SlowQueryAnalyzer(file_path)
            slow_queries = analyzer.analyze(threshold)
            if slow_queries is not None:
                return slow_queries.to_dict('records')
            else:
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    return []

# 回调函数：绘制慢查询图
@app.callback(
    Output('slow-query-graph', 'figure'),
    [Input('analyze-button', 'n_clicks')],
    [State('file-path', 'value'), State('threshold', 'value')],
    prevent_initial_call=True
)
def plot_slow_queries(n_clicks, file_path, threshold):
    if n_clicks > 0:
        try:
            analyzer = SlowQueryAnalyzer(file_path)
            slow_queries = analyzer.analyze(threshold)
            if slow_queries is not None:
                fig = px.bar(slow_queries, x='query', y='duration', title='慢查询分析')
                return fig
            else:
                return {}
        except Exception as e:
            print(f"Error: {e}")
            return {}
    return {}

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)