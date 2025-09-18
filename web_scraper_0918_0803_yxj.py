# 代码生成时间: 2025-09-18 08:03:34
import requests
from bs4 import BeautifulSoup
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# 定义一个函数来抓取网页内容
def scrape_web_content(url):
    try:
        # 发送HTTP GET请求
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.prettify()
        else:
            return f"Failed to retrieve content. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# 创建Dash应用
app = dash.Dash(__name__)

# 添加Dash页面布局
app.layout = html.Div(children=[
    html.H1(children='Web Content Scraper'),
    dcc.Input(id='url-input', type='text', placeholder='Enter a URL here'),
    html.Button('Scrape Content', id='scrape-button', n_clicks=0),
    html.Div(id='output-container'),
])

# 定义回调函数来处理用户输入和显示结果
@app.callback(
    Output('output-container', 'children'),
    [Input('scrape-button', 'n_clicks')],
    [State('url-input', 'value')]
)
def update_output(n_clicks, url):
    if n_clicks > 0:
        # 调用抓取函数并获取结果
        content = scrape_web_content(url)
        return html.Pre(style={'whiteSpace': 'pre-wrap'}, children=content)
    return ''

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)