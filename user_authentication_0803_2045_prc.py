# 代码生成时间: 2025-08-03 20:45:50
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from werkzeug.security import generate_password_hash, check_password_hash


# 用户身份认证类
class Authentication:
    def __init__(self):
        # 存储用户信息的字典
        self.users = {}

    def add_user(self, username, password):
        """添加新用户"""
        if username in self.users:
            raise ValueError(f"User {username} already exists")
        hashed_password = generate_password_hash(password)
        self.users[username] = hashed_password

    def authenticate(self, username, password):
        """验证用户身份"""
        if username not in self.users:
            return False
        return check_password_hash(self.users[username], password)


# Dash应用
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# 身份认证对象
auth = Authentication()
auth.add_user("user1", "password1")  # 添加测试用户

# 布局
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# 回调函数
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('page-content', 'children')]  # 确保页面刷新时能保持当前状态
)
def display_page(pathname, previous_content):
    # 基本页面
    if pathname == "/login":
        return html.Div([
            html.H3("Login"),
            html.Div([
                html.Label("Username"),
                dcc.Input(id="username", type="text")
            ]),
            html.Div([
                html.Label("Password"),
                dcc.Input(id="password", type="password")
            ]),
            html.Button("Login", id="login-button"),
            dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  # 用于自动刷新页面
        ])
    elif pathname == "/":
        return html.H1("Home Page")
    else:
        return html.H1("404 Not Found")

# 登录回调
@app.callback(
    Output('page-content', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def login(n_clicks, username, password):
    if n_clicks is None:
        return None
    if auth.authenticate(username, password):
        return html.H1("Welcome to the Dashboard!")
    else:
        return html.Div(["Invalid username or password. Please try again."])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
