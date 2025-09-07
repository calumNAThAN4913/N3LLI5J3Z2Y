# 代码生成时间: 2025-09-07 08:20:36
import hashlib
from dash import Dash, html, Input, Output

# 初始化 Dash 应用
app = Dash(__name__)

# 定义布局，包含一个文本输入框和一个按钮
app.layout = html.Div([
    html.H1('Hash Calculator'),
    html.Div('Enter text to hash:'),
    html.Div([
        html.Input(id='input-text', type='text'),
        html.Button('Calculate Hash', id='calculate-button', n_clicks=0),
    ]),
    html.Div(id='output-container'),
])

# 定义回调函数，当按钮被点击时触发
@app.callback(
    Output('output-container', 'children'),
    [Input('calculate-button', 'n_clicks')],
    [State('input-text', 'value')]
)
def calculate_hash(n_clicks, input_value):
    # 处理点击事件
    if n_clicks == 0:
        return ''  # 如果按钮未被点击，则不显示任何内容
    
    try:
        # 计算输入文本的哈希值
        if not input_value:
            raise ValueError('Input is empty.')
        hash_value = hashlib.sha256(input_value.encode()).hexdigest()
        return f'Hash Value: {hash_value}'
    except Exception as e:
        # 处理可能发生的错误
        return str(e)

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)
