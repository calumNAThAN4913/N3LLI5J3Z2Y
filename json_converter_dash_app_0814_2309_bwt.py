# 代码生成时间: 2025-08-14 23:09:38
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json
from flask import escape

# 定义Dash应用
app = dash.Dash(__name__)
server = app.server

# 应用布局
app.layout = html.Div([
    # 输入框，用于输入JSON数据
    dcc.Textarea(
        id="input-json",
        placeholder="Enter JSON data here...",
        style={'width': '100%', 'height': '200px'},
    ),
    # 转换按钮
    html.Button("Convert", id="convert-button"),
    # 输出框，用于显示转换后的JSON数据
    dcc.Textarea(
        id="output-json",
        placeholder="Converted JSON data will appear here...",
        style={'width': '100%', 'height': '200px'},
    ),
    # 错误信息显示框
    html.Div(id="error-message"),
])

# 定义回调函数，实现JSON数据格式转换
@app.callback(
    Output("output-json", "value"),
    Output("error-message", "children"),
    [Input("convert-button", "n_clicks"), Input("input-json", "value")],
    [State("input-json", "value")],
)
def convert_json(n_clicks, input_json, input_json_state):
    # 初始化错误信息为空字符串
    error_message = ""
    # 检查是否点击了转换按钮
    if n_clicks is None:
        return input_json_state, error_message
    # 尝试解析输入的JSON数据
    try:
        # 将输入的JSON字符串转换为Python字典
        json_data = json.loads(input_json)
        # 将Python字典转换回JSON字符串，并格式化输出
        output_json = json.dumps(json_data, indent=4)
    except json.JSONDecodeError as e:
        # 如果解析失败，记录错误信息
        error_message = "Invalid JSON data: " + str(e)
        output_json = input_json_state  # 保持原输入数据不变
    return output_json, error_message

# 运行Dash应用
if __name__ == "__main__":
    app.run_server(debug=True)