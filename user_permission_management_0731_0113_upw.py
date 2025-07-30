# 代码生成时间: 2025-07-31 01:13:31
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
from dash.dependencies import Input, Output, State\
import plotly.express as px\
from dash.exceptions import PreventUpdate\
from flask import session\
from flask_simplelogin import login_required, login_user, logout_user\
from werkzeug.security import generate_password_hash, check_password_hash\
import sqlite3\
\
# 数据库初始化\
DATABASE = 'user_permission.db'\
\
class UserPermissionManagement:
    def __init__(self):
        # 初始化Dash应用\
        self.app = dash.Dash(__name__)\
        self.app.layout = html.Div([
            html.H1('用户权限管理系统'),
            html.Div(id='login-div', children=[
                html.Div(
                    [
                        html.Label('用户名'),
                        dcc.Input(id='username-input', type='text', required=True),
                    ],
                    style={'marginBottom': 20}),
                html.Div(
                    [
                        html.Label('密码'),
                        dcc.Input(id='password-input', type='password', required=True),
                    ],
                    style={'marginBottom': 20}),
                html.Button('登录', id='login-button', n_clicks=0),
                html.Div(id='login-output'),
            ]),
            html.Div(id='dashboard-div', children=[], style={'display': 'none'}),
        ])

        # 回调函数：登录按钮点击事件\
        @self.app.callback(
            Output('login-output', 'children'),
            [Input('login-button', 'n_clicks')],
            [State('username-input', 'value'), State('password-input', 'value')]
        )
def login_output(n_clicks, username, password):
            if n_clicks == 0:
                raise PreventUpdate
            if not username or not password:
                return '请输入用户名和密码'
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username=?', (username,))
            user = cursor.fetchone()
            conn.close()
            if not user:
                return '用户名不存在'
            if not check_password_hash(user[1], password):
                return '密码错误'
            login_user(username)
            return '登录成功'

        # 回调函数：显示用户权限\
        @self.app.callback(
            Output('dashboard-div', 'children'),
            [Input('login-output', 'children')],
        )
def show_dashboard(login_output):
            if login_output:
                user = session.get('username')
                conn = sqlite3.connect(DATABASE)
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM permissions WHERE username=?', (user,))
                permissions = cursor.fetchall()
                conn.close()
                return [
                    html.H2('用户权限'),
                    html.Div([
                        html.P(f'{perm[0]}: {perm[1]}') for perm in permissions
                    ]),
                ]
            else:
                raise PreventUpdate

        # 初始化用户数据库\
        self._init_db()

    def _init_db(self):
        # 创建用户表和权限表\
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS permissions
                     (username TEXT, permission TEXT,
                     FOREIGN KEY(username) REFERENCES users(username))''')
        conn.commit()
        conn.close()

    def run_app(self):
        self.app.run_server(debug=True)

if __name__ == '__main__':
    user_permission_management = UserPermissionManagement()
    user_permission_management.run_app()