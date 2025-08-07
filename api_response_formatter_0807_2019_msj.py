# 代码生成时间: 2025-08-07 20:19:25
import dash
from dash import html
from dash.dependencies import Input, Output
import json

# 设置Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    html.H1('API响应格式化工具'),
    html.Textarea(id='api-response-input', rows=10, cols=50, placeholder='输入API响应...'),
    html.Button('格式化', id='format-button'),
    html.Pre(id='formatted-response')
])

# 回调函数用于格式化API响应
@app.callback(
    Output('formatted-response', 'children'),
    [Input('format-button', 'n_clicks')],
    [State('api-response-input', 'value')]
)
def format_response(n_clicks, response_text):
    # 错误处理：确保有输入
    if not response_text or n_clicks is None:
        return '请先输入API响应并点击格式化。'
    
    try:
        # 尝试将输入的字符串解析为JSON
        parsed_response = json.loads(response_text)
        # 格式化JSON字符串
        formatted_response = json.dumps(parsed_response, indent=4, ensure_ascii=False)
        return formatted_response
    except json.JSONDecodeError as e:
        # 错误处理：捕获JSON解析错误
        return f'错误：无法解析JSON - {str(e)}'

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
