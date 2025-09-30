# 代码生成时间: 2025-09-30 20:08:52
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate

# 定义Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div(children=[
    html.H1("车联网平台"),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # 每1秒刷新一次
        n_intervals=0  # 无限次刷新
    ),
    html.Div(id='live-update-text')
])

# 模拟的车辆数据生成器
def generate_vehicle_data():
    # 这里可以替换为实际的车辆数据源
    return {
        "vehicle_id": "vehicle_1",
        "timestamp": "2024-04-01 12:00:00",
        "speed": 60,
        "location": {"lat": 39.9042, "lon": 116.4074},
        "status": "正常"
    }

# 回调函数，用于实时更新图表和文本
@app.callback(
    Output('live-update-graph', 'figure'),
    Output('live-update-text', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n):
    # 检查是否需要更新
    if not n:
        raise PreventUpdate()
    
    # 生成模拟数据
    vehicle_data = generate_vehicle_data()
    
    # 将数据转换为DataFrame
    df = pd.DataFrame([vehicle_data])
    
    # 绘制图表
    fig = px.scatter_mapbox(
        df,
        lat='lat',
        lon='lon',
        size='speed',
        color='status',
        zoom=10,
        center={"lat": 39.9042, "lon": 116.4074},
        height=600
    )
    
    # 更新图表
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    
    # 更新文本
    live_text = f"车辆ID：{vehicle_data['vehicle_id']}
时间：{vehicle_data['timestamp']}
速度：{vehicle_data['speed']} km/h
位置：{vehicle_data['location']['lat']}, {vehicle_data['location']['lon']}
状态：{vehicle_data['status']}"
    
    return fig, live_text

if __name__ == '__main__':
    # 运行Dash应用
    app.run_server(debug=True)