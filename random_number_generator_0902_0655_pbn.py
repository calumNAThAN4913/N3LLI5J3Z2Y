# 代码生成时间: 2025-09-02 06:55:33
import dash
import dash_core_components as dcc
import dash_html_components as html
import random
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

# 定义随机数生成器的组件
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    # 标题
    html.H1(children='Random Number Generator'),

    # 滑动条组件，用于设置随机数的范围
    dcc.Slider(
        id='random-slider',
        min=1,
        max=100,
        step=1,
        marks={str(i): str(i) for i in range(1, 101)},
        value=10,
    ),

    # 按钮组件，用于生成随机数
    html.Button('Generate', id='generate-button', n_clicks=0),

    # 输出组件，用于显示生成的随机数
    html.Div(id='random-output'),
])

# 回调函数，当按钮被点击时触发
@app.callback(
    Output('random-output', 'children'),
    [Input('generate-button', 'n_clicks')],
    [State('random-slider', 'value')],
)
def generate_random_number(n_clicks, slider_value):
    # 错误处理，确保滑动条的值在预期范围内
    if slider_value < 1 or slider_value > 100:
        return 'Please set slider within the range 1-100.'

    # 生成随机数
    random_number = random.randint(1, slider_value)

    # 返回显示随机数的字符串
    return f'Generated number: {random_number}'

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)