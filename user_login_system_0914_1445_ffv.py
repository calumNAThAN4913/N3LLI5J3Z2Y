# 代码生成时间: 2025-09-14 14:45:52
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import session
import pandas as pd
from dash.exceptions import PreventUpdate

# 定义用户登录数据集
users = pd.DataFrame({
    "username": ["user1", "user2"],
    "password": ["password1", "password2"]
})

# 定义Dash应用
app = dash.Dash(__name__)

# 设置应用布局
app.layout = html.Div([
    html.H1("User Login System"),
    dcc.Input(id="username", type="text", placeholder="Enter username"),
    dcc.Input(id="password", type="password", placeholder="Enter password"),
    html.Button("Login", id="login-button", n_clicks=0),
    html.Div(id="output")
])

# 回调函数处理用户登录
@app.callback(
    Output("output", "children"),
    [Input("login-button", "n_clicks")],
    [State("username", "value"), State("password", "value")]
)
def login(n_clicks, username, password):
    if n_clicks == 0 or not username or not password:
        raise PreventUpdate  # 防止在未点击按钮或输入数据为空时更新
    
    # 在用户数据集中查找用户名和密码
    user = users[(users['username'] == username) & (users['password'] == password)]
    
    if not user.empty:
        # 登录成功，设置session并返回成功消息
        session['logged_in'] = True
        session['username'] = username
        return f"Login successful for user: {username}"
    else:
        # 登录失败，返回错误消息
        return "Invalid username or password"

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)