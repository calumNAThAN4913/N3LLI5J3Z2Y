# 代码生成时间: 2025-08-02 09:37:01
import dash
from dash import html
from dash.dependencies import Input, Output
import json

"""
API响应格式化工具
一个简单的Dash应用程序，用于格式化API响应。
"""

# 初始化Dash应用程序
app = dash.Dash(__name__)

# 定义布局
app.layout = html.Div(children=[
    html.H1('API响应格式化工具'),
    html.Div(
        id='input',
        children=[
            html.Label('输入API响应：'),
            html.TextArea(id='api-response-input', style={'width': '100%', 'height': '150px'}),
        ]
    ),
    html.Button('格式化响应', id='format-button', n_clicks=0),
    html.Div(id='formatted-response'),
    html.Div(id='error-response'),
])

# 回调函数，用于处理格式化请求
@app.callback(
    Output('formatted-response', 'children'),
    Output('error-response', 'children'),
    Input('format-button', 'n_clicks'),
    [dash.State('api-response-input', 'value')],
)
def format_response(n_clicks, api_response):
    """
    格式化API响应函数。
    参数：
    n_clicks (int): 按钮点击次数。
    api_response (str): 用户输入的API响应。
    返回：
    格式化后的API响应或错误信息。
    """
    # 如果按钮未点击，则不执行任何操作
    if n_clicks is None or n_clicks == 0:
        return '', ''

    try:
        # 尝试解析输入的API响应
        response = json.loads(api_response)
        # 格式化响应并返回
        formatted_response = json.dumps(response, indent=4)
        return html.Pre(formatted_response), ''
    except json.JSONDecodeError as e:
        # 如果解析失败，返回错误信息
        return '', f'错误：无法解析输入的API响应。 {e}'

# 运行应用程序
if __name__ == '__main__':
    app.run_server(debug=True)