# 代码生成时间: 2025-08-06 01:42:27
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psutil
import pandas as pd
from dash.exceptions import PreventUpdate


# 系统性能监控Dash应用
class SystemMonitor:
    def __init__(self):
        # 初始化Dash应用
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div([
            html.H1("系统性能监控"),
            dcc.Graph(id='cpu_usage'),
            dcc.Graph(id='memory_usage'),
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # 每1秒刷新一次
                n_intervals=0
            ),
        ])

    def update_metrics(self, interval):
        # 获取CPU和内存使用情况
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        # 更新Dash图表数据
        self.app.callback(
            output=[Output('cpu_usage', 'figure'), Output('memory_usage', 'figure')],
            inputs=[Input('interval-component', 'n_intervals')],
            prevent_initial_call=True
        )(self.get_figure, self.get_figure)

    def get_figure(self, n):
        # 获取CPU或内存使用情况的图表数据
        if n == 0:  # CPU使用情况
            data = pd.DataFrame(
                {
                    'x': list(range(10)),  # x轴数据，模拟10秒内的数据
                    'y': [psutil.cpu_percent(interval=None) for _ in range(10)]  # y轴数据，每1秒采集一次CPU使用率
                }
            )
        else:  # 内存使用情况
            data = pd.DataFrame(
                {
                    'x': list(range(10)),
                    'y': [psutil.virtual_memory().percent for _ in range(10)]
                }
            )

        # 返回图表配置
        return {
            'data': [{'x': data['x'], 'y': data['y']}],
            'layout': {
                'title': 'CPU/内存使用率',
                'xaxis': {'title': '时间 (秒)'},
                'yaxis': {'title': '使用率 (%)'}
            }
        }

    # 运行Dash应用
def run():
    monitor = SystemMonitor()
    monitor.app.run_server(debug=True)

if __name__ == '__main__':
    run()