# 代码生成时间: 2025-08-14 11:24:12
# random_number_generator.py

# 导入Dash库和相关模块
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import random

# 定义Dash应用程序
app = Dash(__name__)

# 设置布局
app.layout = html.Div([
    # 标题
    html.H1("随机数生成器"),
    # 输入框，用于输入最小值和最大值
    html.Div([
        dcc.Input(id='min-value', type='number', placeholder='最小值'),
        html.Div(style={'margin': '10px'}),
        dcc.Input(id='max-value', type='number', placeholder='最大值')
    ]),
    # 按钮，用于生成随机数
    html.Button("生成随机数", id="generate-button"),
    # 输出框，用于显示生成的随机数
    html.Div(id="random-number")
])

# 定义回调函数，处理按钮点击事件
@app.callback(
    Output("random-number", "children"),
    [Input("generate-button", "n_clicks")],
    [State("min-value", "value"), State("max-value", "value")]
)
def generate_random_number(n_clicks, min_value, max_value):
    if n_clicks is None or min_value is None or max_value is None:
        # 如果没有输入或点击按钮，返回提示信息
        return "请填写最小值和最大值，然后点击'生成随机数'"
    else:
        try:
            # 将输入值转换为整数
            min_value = int(min_value)
            max_value = int(max_value)
            # 检查输入值是否有效
            if min_value >= max_value:
                return "最小值必须小于最大值"
            else:
                # 生成随机数
                random_number = random.randint(min_value, max_value)
                return f"生成的随机数是：{random_number}"
        except ValueError:
            # 如果输入值不是整数，返回错误信息
            return "输入值必须是整数"

# 运行Dash应用程序
if __name__ == '__main__':
    app.run_server(debug=True)