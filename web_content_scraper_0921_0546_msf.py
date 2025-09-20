# 代码生成时间: 2025-09-21 05:46:27
import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)

# 定义一个函数来抓取网页内容
def scrape_web_content(url):
    try:
        # 发送请求，获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 返回网页的标题和内容
        return {
            'title': soup.title.string if soup.title else 'No title found',
            'content': soup.get_text(separator='\
')
        }
    except requests.RequestException as e:
        # 处理请求异常
        logging.error(f'Request failed: {e}')
        return None
    except Exception as e:
        # 处理其他异常
        logging.error(f'An error occurred: {e}')
        return None

# 定义Dash应用
app = dash.Dash(__name__)

# 定义Dash应用的布局
app.layout = html.Div(children=[
    html.H1(children='Web Content Scraper'),
    dcc.Input(
        id='url-input',
        type='text',
        placeholder='Enter a URL here',
        debounce=True
    ),
    html.Button('Scrape Content', id='scrape-button', n_clicks=0),
    dcc.Markdown(id='content-output')
])

# 定义回调函数，当按钮被点击时触发
@app.callback(
    Output(component_id='content-output', component_property='children'),
    [Input(component_id='url-input', component_property='value'),
     Input(component_id='scrape-button', component_property='n_clicks')]
)
def scrape_content(url, n_clicks):
    if n_clicks > 0 and url is not None:  # 确保按钮被点击且URL有效
        content = scrape_web_content(url)
        if content:
            return f'Title: {content[