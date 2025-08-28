# 代码生成时间: 2025-08-28 19:05:12
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义Dash应用
app = dash.Dash(__name__)

# 设置Dash App的布局
app.layout = html.Div([
    html.H1("网页内容抓取工具"),
    html.Div([
        dcc.Input(id='url-input', type='text', placeholder='输入网页URL'),
        html.Button("抓取内容", id='grab-button', n_clicks=0)
    ]),
    html.Div(id='output-container')
])

# 回调函数，用于抓取网页内容并展示结果
@app.callback(
    Output('output-container', 'children'), 
    [Input('grab-button', 'n_clicks')],
    [State('url-input', 'value')]
)
def grab_content(n_clicks, url):
    if n_clicks == 0 or url is None:
        return ''
    try:
        # 发送请求获取网页内容
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code != 200:
            return f'请求失败，状态码：{response.status_code}'
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 获取网页的标题和段落内容
        title = soup.title.string if soup.title else '无标题'
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        # 将段落内容转换为DataFrame
        df = pd.DataFrame(paragraphs, columns=['内容'])
        # 将DataFrame转换为HTML表格用于展示
        return html.Table([html.Thead(html.Tr([html.Th('内容')])), html.Tbody([html.Tr([html.Td(p)]) for p in df['内容']])])
    except Exception as e:
        # 错误处理
        return f'抓取过程中发生错误：{str(e)}'

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)