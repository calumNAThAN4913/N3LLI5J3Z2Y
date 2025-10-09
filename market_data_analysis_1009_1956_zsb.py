# 代码生成时间: 2025-10-09 19:56:45
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# 定义全局变量，用于存储市场数据
market_data = {"AAPL": [], "GOOGL": []}

# 模拟数据生成函数
def generate_mock_data(ticker, start, end):
    # 创建时间序列
    time_series = pd.date_range(start=start, end=end, freq='B')  # 'B' 代表工作日
    # 生成模拟数据
    return pd.DataFrame({"Date": time_series, ticker: np.random.randn(len(time_series))})

# 应用布局
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='市场数据分析'),
    dcc.Graph(id='market-data-plot'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # 每秒刷新
        n_intervals=0  # 从0开始计数
    )
])

# 回调函数，用于更新图形
@app.callback(
    Output('market-data-plot', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # 更新日期范围，模拟新的数据
    today = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - pd.DateOffset(days=7)).strftime('%Y-%m-%d')
    
    # 更新市场数据
    market_data["AAPL"] = generate_mock_data("AAPL", start=start_date, end=today)
    market_data["GOOGL"] = generate_mock_data("GOOGL", start=start_date, end=today)
    
    # 合并数据
    combined_data = pd.concat(market_data)
    
    # 绘制图表
    fig = px.line(combined_data, x='Date', y=combined_data.columns[1:], title='市场数据分析', labels={"value": "值", "variable": "股票"})
    return fig

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)