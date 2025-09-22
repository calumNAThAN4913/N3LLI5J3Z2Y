# 代码生成时间: 2025-09-22 20:13:13
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import base64
import io
from PIL import Image
import uuid
import os
import logging

# 设置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义全局变量
APP_NAME = '消息通知系统'
APP_VERSION = '1.0'

# 初始化Dash应用
app = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}]
                , external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# 定义页面布局
app.layout = html.Div([
    html.H1('消息通知系统', style={'textAlign': 'center', 'margin': '20px'}),
    html.Div([
        html.Label('消息标题', style={'margin': '5px'}),
        dcc.Input(id='message-title', type='text', value='', style={'margin': '5px'}),
    ]),
    html.Div([
        html.Label('消息内容', style={'margin': '5px'}),
        dcc.Textarea(id='message-content', value='', style={'margin': '5px', 'height': '100px'}),
    ]),
    html.Button('发送消息', id='send-message-btn', n_clicks=0, style={'margin': '20px'}),
    html.Div(id='message-output', style={'margin': '20px'}),
])

# 定义回调函数发送消息
@app.callback(
    Output('message-output', 'children'),
    [Input('send-message-btn', 'n_clicks')],
    [State('message-title', 'value'), State('message-content', 'value')]
)
def send_message(n_clicks, title, content):
    if n_clicks == 0:  # 避免初始加载时触发回调
        raise PreventUpdate
    
    # 验证输入内容
    if not title or not content:  # 确保标题和内容不能为空
        return '标题和内容不能为空！'
    
    # 发送消息通知
    try:  # 尝试发送消息
        logger.info(f'发送消息：{title} - {content}')
        return f'消息发送成功：{title}'
    except Exception as e:  # 捕获异常
        logger.error(f'发送消息失败：{str(e)}')
        return f'消息发送失败：{str(e)}'

# 定义回调函数显示消息列表
@app.callback(
    Output('message-list', 'children'),
    Input('show-messages-btn', 'n_clicks')
)
def show_messages(n_clicks):  # 按钮点击次数
    if n_clicks == 0:  # 避免初始加载时触发回调
        raise PreventUpdate
    
    # 从数据库或文件中读取消息列表
    try:  # 尝试读取数据
        messages = pd.read_csv('messages.csv')  # 假设消息存储在CSV文件中
        message_list = html.Ul([html.Li(message) for message in messages['message'].to_list()])  # 将消息转换为列表
        return message_list
    except Exception as e:  # 捕获异常
        logger.error(f'读取消息列表失败：{str(e)}')
        return f'读取消息列表失败：{str(e)}'

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)