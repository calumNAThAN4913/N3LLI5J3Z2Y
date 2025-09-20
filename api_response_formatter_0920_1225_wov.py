# 代码生成时间: 2025-09-20 12:25:32
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import json

# 定义一个响应格式化工具的函数
def format_response(data):
    """
    格式化API响应为JSON字符串

    参数:
        data (dict): API响应数据

    返回:
        str: 格式化后的JSON字符串
    """
    try:
        # 尝试将数据转换为JSON格式
        formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
        return formatted_data
    except (TypeError, ValueError) as e:
        # 处理数据转换错误
        return f"Error formatting response: {str(e)}"

# 初始化Dash应用
app = dash.Dash(__name__)

# 设置布局
app.layout = html.Div(
    children=[
        html.H1("API响应格式化工具"),
        dcc.Textarea(
            id="input-data",
            placeholder="输入API响应数据..."
        ),
        html.Button("格式化", id="format-button"),
        html.Pre(id="formatted-data")  # 显示格式化后的JSON字符串
    ]
)

# 定义回调函数，处理按钮点击事件
@app.callback(
    Output("formatted-data", "children"),
    [Input("format-button", "n_clicks")],
    [State("input-data", "value")]
)
def format_api_response(n_clicks, input_data):
    """
    处理按钮点击事件，格式化输入的API响应数据

    参数:
        n_clicks (int): 按钮点击次数
        input_data (str): 输入的API响应数据

    返回:
        str: 格式化后的JSON字符串或错误信息
    "