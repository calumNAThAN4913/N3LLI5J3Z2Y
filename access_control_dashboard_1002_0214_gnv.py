# 代码生成时间: 2025-10-02 02:14:26
import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import session
from dash.dependencies import ALL

# 初始化Dash应用
app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])

# 模拟用户数据库，用于验证
USERS = {
    "admin": "admin123",
    "user": "user123"
}

# 登录页面组件
login_div = html.Div([
    html.H1("Login"),
    dcc.Input(id="username", type="text", placeholder="Enter username"),
    dcc.Input(id="password", type="password", placeholder="Enter password"),
    html.Button("Login", id="login")
])

# 主页组件
main_div = html.Div([
    html.H1("Welcome to the Dashboard!"),
    html.Div(id="access-content")  # 根据用户角色显示不同内容
])

# 应用布局
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
])

# 回调函数：处理登录逻辑
@app.callback(
    Output("page-content", "children"),
    [Input("login", "n_clicks"), Input("url", "pathname")],
    [State("username", "value"), State("password", "value")],
)
def login(n_clicks, pathname, username, password):
    if n_clicks is None or username is None or password is None:
        raise PreventUpdate
    if username in USERS and USERS[username] == password:
        session["username"] = username  # 设置用户会话
        return main_div
    return login_div

# 回调函数：根据用户角色显示不同内容
@app.callback(
    Output("access-content", "children"),
    [Input("url", "pathname")],
    [State("page-content", "children")],
)
def display_content(pathname, page_content):
    if page_content is None:
        raise PreventUpdate
    if session.get("username") == "admin":
        # 管理员权限内容
        return html.Div([html.H3("Admin Dashboard"), html.P("Welcome, admin!")])
    elif session.get("username") == "user":
        # 用户权限内容
        return html.Div([html.H3("User Dashboard"), html.P("Welcome, user!")])
    else:
        # 无权限内容
        return html.Div([html.H3("Access Denied"), html.P("You do not have permission to view this page.")])

# 启动应用
if __name__ == '__main__':
    app.run_server(debug=True)