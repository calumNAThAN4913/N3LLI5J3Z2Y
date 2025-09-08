# 代码生成时间: 2025-09-08 09:24:24
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import random

# 定义Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    # 标题
    html.H1("Random Number Generator"),
    # 输入框
    dcc.Input(
        id='min-max-input',
        type='text',
        placeholder='Enter min and max values separated by a comma',
        value='0,10'
    ),
    # 按钮
    html.Button("Generate", id="generate-button"),
    # 输出框
    html.Div(id="output-container")
])

# 回调函数：当用户点击按钮时，生成随机数
@app.callback(
    Output("output-container", "children"),
    [Input("generate-button", "n_clicks")],
    [State("min-max-input", "value")]
)
def generate_random_number(n_clicks, min_max_input):
    # 错误处理：检查输入格式是否正确
    if n_clicks is None or min_max_input is None or ',' not in min_max_input:
        return "Please enter valid min and max values separated by a comma."
    
    try:
        # 解析输入的最小值和最大值
        min_val, max_val = map(int, min_max_input.split(','))
        # 检查值的范围是否合理
        if min_val >= max_val:
            return "Minimum value must be less than maximum value."
        # 生成随机数
        random_number = random.randint(min_val, max_val)
        return f"Random Number: {random_number}"
    except ValueError:
        return "Please enter valid integers for min and max values."

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)