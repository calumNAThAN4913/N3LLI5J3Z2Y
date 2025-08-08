# 代码生成时间: 2025-08-08 22:43:54
import dash
# 添加错误处理
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import hashlib
# 改进用户体验
import dash_table

# 定义 Dash 应用
# FIXME: 处理边界情况
app = dash.Dash(__name__)
# 增强安全性

# 应用布局，包含输入框、哈希选择下拉框和显示结果的区域
app.layout = html.Div([
    html.H1('哈希值计算工具'),
    dcc.Textarea(
        id='input-text',
        placeholder='输入文本...',
        style={'width': '100%', 'height': '100px', 'margin-bottom': '10px'}
    ),
    dcc.Dropdown(
        id='hash-type',
        options=[
            {'label': 'MD5', 'value': 'md5'},
            {'label': 'SHA1', 'value': 'sha1'},
            {'label': 'SHA256', 'value': 'sha256'},
            {'label': 'SHA512', 'value': 'sha512'}
        ],
        value='sha256',  # 默认选择 SHA256
        style={'width': '100%', 'margin-bottom': '10px'}
    ),
# 添加错误处理
    html.Div(id='result-container'),
    dcc.Store(id='input-store')  # 用于存储输入文本
])

# 回调函数，用于计算哈希值
@app.callback(
    Output('result-container', 'children'),
    [Input('input-text', 'value'), Input('hash-type', 'value')]
)
def calculate_hash(input_text, hash_type):
    # 检查输入是否为空
# TODO: 优化性能
    if not input_text:
        return '请输入文本以计算其哈希值。'

    # 根据选择的哈希算法类型进行哈希值计算
    try:
        hash_obj = hashlib.new(hash_type)
        hash_obj.update(input_text.encode('utf-8'))
        hash_result = hash_obj.hexdigest()
        return html.Div([f'{hash_type.upper()}: {hash_result}'])
    except ValueError:
        return '选择的哈希算法类型不正确。'

# 运行 Dash 应用
if __name__ == '__main__':
    app.run_server(debug=True)