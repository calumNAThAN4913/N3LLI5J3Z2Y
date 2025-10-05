# 代码生成时间: 2025-10-06 02:25:26
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

# 定义全局变量
DATA_FILE = 'network_data.csv'  # 网络数据文件


def load_data(file_path):
    """加载网络数据"""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f'Error loading data: {e}')
        return None


def create_app():
    """创建Dash应用"""
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1('网络安全监控'),
        dcc.Dropdown(
            id='timeframe-dropdown',
            options=[
                {'label': 'Last 1 Hour', 'value': '1h'},
                {'label': 'Last 6 Hours', 'value': '6h'},
                {'label': 'Last 12 Hours', 'value': '12h'},
                {'label': 'Last 24 Hours', 'value': '24h'}],
            value='24h',
            multi=False
        ),
        dcc.Graph(id='network-traffic-graph', figure=create_figure()),
    ])

    @app.callback(
        Output('network-traffic-graph', 'figure'),
        [Input('timeframe-dropdown', 'value')],
        [State('network-traffic-graph', 'figure')]
    )
    def update_graph(selected_timeframe, figure):
        """根据选择的时间范围更新图表"""
        df = load_data(DATA_FILE)
        if df is not None:
            # 根据选择的时间范围筛选数据
            current_time = datetime.now()
            if selected_timeframe == '1h':
                df_filtered = df[(df['timestamp'] >= current_time - pd.Timedelta(hours=1)) & (df['timestamp'] <= current_time)]
            elif selected_timeframe == '6h':
                df_filtered = df[(df['timestamp'] >= current_time - pd.Timedelta(hours=6)) & (df['timestamp'] <= current_time)]
            elif selected_timeframe == '12h':
                df_filtered = df[(df['timestamp'] >= current_time - pd.Timedelta(hours=12)) & (df['timestamp'] <= current_time)]
            else:  # 24h
                df_filtered = df[(df['timestamp'] >= current_time - pd.Timedelta(days=1)) & (df['timestamp'] <= current_time)]

            # 创建图表
            figure = create_figure()
            if not figure['data']:
                figure['data'].append(go.Scatter(x=df_filtered['timestamp'], y=df_filtered['traffic'], mode='lines'))
            else:
                figure['data'][0]['x'] = df_filtered['timestamp']
                figure['data'][0]['y'] = df_filtered['traffic']

            return figure
        else:
            return figure

    return app


def create_figure():
    """创建图表"""
    df = load_data(DATA_FILE)
    if df is not None:
        fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['traffic'], mode='lines')])
        fig.update_layout(title='网络流量监控', xaxis_title='时间', yaxis_title='流量')
        return fig
    else:
        return {}

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True)