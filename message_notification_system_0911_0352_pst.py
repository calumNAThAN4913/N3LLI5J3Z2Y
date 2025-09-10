# 代码生成时间: 2025-09-11 03:52:22
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
from threading import Thread
import time
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义全局变量存储消息队列
message_queue = []

# 定义Dash应用
app = dash.Dash(__name__)
app.title = "Message Notification System"

# 定义布局
app.layout = html.Div([
    html.H1("Message Notification System"),
    dcc.Input(id="message-input", type="text", placeholder="Enter message..."),
    html.Button("Send Message", id="send-button", n_clicks=0),
    dcc.Interval(
        id="interval-component",
        interval=1*1000,  # 1000 milliseconds
        n_intervals=0
    ),
    html.Div(id="message-container")
])

# 定义回调，处理发送消息事件
@app.callback(
    Output("message-container", "children"),
    [Input("send-button", "n_clicks"), Input("interval-component", "n_intervals")],
    [State("message-input", "value")],
    prevent_initial_call=True
)
def update_output(n_clicks, n_intervals, message):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ""  # 不是按钮点击触发的回调，返回空
    if n_clicks is None or n_clicks == 0:
        return ""  # 按钮没有被点击，返回空
    
    # 添加到消息队列
    message_queue.append(message)
    
    # 清空输入框
    return ""

# 定义回调，显示消息
@app.callback(
    Output("message-container", "children"),
    [Input("interval-component", "n_intervals")],
)
def display_messages(n_intervals):
    if not message_queue:
        return ""  # 没有消息时返回空
    try:
        # 从队列中获取消息并展示
        messages = message_queue.copy()
        message_queue.clear()  # 清空队列
        return html.Div([html.P(m) for m in messages])
    except Exception as e:
        logger.error(f"Error displaying messages: {e}")
        return "Error displaying messages"

# 定义回调，处理外部消息通知
@app.callback(
    Output('message-container', 'children'),
    [Input('external-message', 'n_clicks')],
    prevent_initial_call=True,
    output_triggerable=True
)
def handle_external_message(n_clicks):
    if n_clicks is None or n_clicks == 0:
        return None
    
    # 模拟从外部系统接收消息
    external_message = "External message received"
    message_queue.append(external_message)
    return html.Div([html.P(external_message)])

# 定义线程函数，模拟从外部系统接收消息
def receive_external_messages():
    while True:
        time.sleep(10)  # 每10秒接收一次消息
        try:
            # 这里使用requests模拟从外部系统接收消息
            response = requests.get("https://api.example.com/external-messages")
            if response.status_code == 200:
                external_message = response.json().get("message", "")
                if external_message:
                    # 触发回调处理外部消息
                    logger.info(f"Received external message: {external_message}")
                    app.callback("output('message-container', 'children')").trigger("external-message