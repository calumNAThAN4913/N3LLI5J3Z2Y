# 代码生成时间: 2025-08-11 22:59:59
import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from markdown import markdown
from bs4 import BeautifulSoup
import re

# 定义一个函数来清理输入，以防止XSS攻击
def sanitize_input(input_text):
    # 使用BeautifulSoup来解析HTML并移除潜在的XSS代码
    soup = BeautifulSoup(input_text, 'html.parser')
    # 移除所有的脚本和iframe标签
    for script in soup(["script", "iframe"]):
        script.decompose()
    # 将清理后的HTML转换回字符串
    return str(soup)

# 创建Dash应用程序
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义应用布局
app.layout = dbc.Container(
    [
        dbc.Alert(
            "输入你的HTML代码测试XSS防护功能。",
            id="alert",
            color="info",
        ),
        dbc.FormGroup(
            [
                dbc.Label("HTML输入"),
                dbc.Textarea(
                    id="html-input",
                    placeholder="在这里输入你的HTML代码..."
                ),
            ],
        ),
        dbc.Button("提交", id="submit-button", color="primary"),
        html.Div(id="output-container"),
    ],
    fluid=True,
)

# 定义回调函数来处理用户的输入并显示清理后的结果
@app.callback(
    Output("output-container", "children"),
    [Input("submit-button", "n_clicks")],
    [State("html-input", "value")],
)
def display_cleaned_html(n_clicks, input_value):
    if n_clicks is None or input_value is None:
        raise PreventUpdate
    # 清理输入以防止XSS攻击
    cleaned_html = sanitize_input(input_value)
    # 使用markdown来渲染清理后的HTML，以防止XSS执行
    rendered_html = markdown(cleaned_html, output_format='html')
    return html.Div(
        [html.H4("清理后的HTML"), html.Pre(rendered_html)]
    )

if __name__ == '__main__':
    app.run_server(debug=True)
