# 代码生成时间: 2025-09-17 07:33:49
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

# 假设有一个用户数据结构，用于存储用户名和密码
# 在实际应用中，这些数据应该存储在数据库中
users_db = {"admin": generate_password_hash("admin123")}

# 身份认证装饰器
def authenticate(func):
    def wrapper(*args, **kwargs):
        # 检查用户是否已经登录，即session中是否有用户信息
        if 'user' not in session:
            # 用户未登录，重定向到登录页面
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

# 登录页面组件
login_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div([
        html.H1("Login"),
        html.Div([
            html.Label("Username"),
            dcc.Input(id='username', type='text'),
        ]),
        html.Div([
            html.Label("Password"),
            dcc.Input(id='password', type='password'),
        ]),
        html.Button("Login", id='login-button', n_clicks=0),
    ]),
])

# 登录表单回调函数
@app.callback(
    Output('page-content', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def login(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate
    # 检查用户名和密码是否正确
    if username in users_db and check_password_hash(users_db[username], password):
        # 用户登录成功，保存用户信息到session
        session['user'] = username
        return html.Div(["Welcome, {}!".format(username)])
    else:
        # 用户登录失败，显示错误信息
        return html.Div(["Invalid username or password. Please try again."])

# 受保护页面组件
protected_layout = html.Div([
    html.H1("Protected Page"),
    html.Div("Only authenticated users can see this content.")
])

# 受保护页面回调函数
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('page-content', 'children')]
)
def display_page(pathname, children):
    if pathname == "/protected":
        return protected_layout
    elif pathname == "/login":
        return login_layout
    else:
        return html.Div(["404 Not Found"])

# 启动Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)