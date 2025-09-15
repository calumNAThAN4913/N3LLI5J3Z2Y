# 代码生成时间: 2025-09-16 02:52:42
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
import json

# 定义Dash应用
app = dash.Dash(__name__)

# 设置Dash应用的布局
app.layout = html.Div(
    [
        dcc.Input(id='url-input', type='text', placeholder='Enter URL here', value=''),
        html.Button('Make Request', id='submit-button', n_clicks=0),
        html.Div(id='output-container'),
    ]
)

# 回调函数：处理HTTP请求
@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('url-input', 'value')]
)
def make_request(n_clicks, url):
    if n_clicks is None or url is None or url == '':
        # 如果没有点击按钮或URL为空，则不执行操作
        return html.Div()
    try:
        # 发送HTTP请求
        response = requests.get(url)
        response.raise_for_status()  # 检查HTTP响应状态
        # 解析响应内容
        data = response.text
        return html.Pre(data)  # 显示响应内容
    except requests.exceptions.HTTPError as http_err:
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        return f'An error occurred: {err}'

# 运行Dash应用
def run_app():
    app.run_server(debug=True)

# 程序入口点
def main():
    run_app()

if __name__ == '__main__':
    main()