# 代码生成时间: 2025-08-15 04:35:03
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
from urllib.parse import urlparse
import re

def validate_url(url):
    # 正则表达式匹配URL
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'[^\s/$.?#].[^\s]*'  # domain...
    )
    return re.match(pattern, url) is not None

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except: return False

def check_url(url):
    if not url:
        return "请输入URL"
    if not validate_url(url):
        return "无效的URL格式"
    try:
        response = requests.head(url, timeout=5)  # 头部请求检测URL是否可达
        if response.status_code == 200:  # 状态码200表示成功
            return "URL有效"
        else:  # 其他状态码
            return f"URL无效，状态码：{response.status_code}"
    except requests.RequestException as e:
        return f"URL不可达：{e}"

def serve_layout():
    app.layout = html.Div(children=[
        html.H1("URL链接有效性验证"),
        dcc.Input(id='url-input', type='text', placeholder="输入URL"),
        html.Button("验证", id="submit-button", n_clicks=0),
        html.Div(id="output-container")
    ])

def serve_callbacks(app):
    @app.callback(
        Output("output-container", "children"),
        [Input("submit-button", "n_clicks")],
        [State("url-input", "value"), State("submit-button", "n_clicks")]
    )
    def validate_url_input(n_clicks, url):
        ctx = dash.callback_context  # 获取上下文
        new_url = url
        if ctx.triggered and ctx.inputs_list and ctx.inputs_list[0]["property"] == "n_clicks":
            if n_clicks > 0:
                return check_url(new_url)
            raise PreventUpdate
        raise PreventUpdate

def main():
    app = dash.Dash(__name__)
    app.layout = serve_layout()
    serve_callbacks(app)
    app.run_server(debug=True)
if __name__ == '__main__':
    main()