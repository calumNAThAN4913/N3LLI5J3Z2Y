# 代码生成时间: 2025-10-01 21:19:55
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import uuid
import sqlite3
from dash.exceptions import PreventUpdate

# 定义项目管理工具的配置信息
app = dash.Dash(__name__)
app.title = '项目管理工具'

# 连接数据库
def get_db_connection():
    conn = sqlite3.connect('projects.db')
    conn.row_factory = sqlite3.Row
    return conn

# 读取项目数据
def load_projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return projects

# 添加项目
def add_project(project_name, project_owner):
    conn = get_db_connection()
    conn.execute('INSERT INTO projects (name, owner) VALUES (?, ?)', (project_name, project_owner))
    conn.commit()
    conn.close()

# 删除项目
def delete_project(project_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()

# 更新项目
def update_project(project_id, project_name, project_owner):
    conn = get_db_connection()
    conn.execute('UPDATE projects SET name = ?, owner = ? WHERE id = ?', (project_name, project_owner, project_id))
    conn.commit()
    conn.close()

# 定义Dash应用的布局
app.layout = html.Div(children=[
    html.H1(children='项目管理工具'),
    html.Div(children=[
        html.P(children='项目名称:'),
        dcc.Input(id='project-name', type='text', placeholder='输入项目名称'),
        html.P(children='项目负责人:'),
        dcc.Input(id='project-owner', type='text', placeholder='输入项目负责人'),
        html.Button('添加项目', id='add-project-button', n_clicks=0),
        html.Div(id='projects-container')
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
])

# 回调函数：添加项目
@app.callback(
    Output('projects-container', 'children'),
    [Input('add-project-button', 'n_clicks')],
    [State('project-name', 'value'), State('project-owner', 'value')]
)
def add_project_callback(n_clicks, project_name, project_owner):
    if n_clicks <= 0 or not project_name or not project_owner:
        raise PreventUpdate
    add_project(project_name, project_owner)
    return html.Div(id='projects-container', children=[html.Div(project) for project in load_projects()])

# 回调函数：定时刷新项目列表
@app.callback(
    Output('projects-container', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def refresh_projects(n_intervals):
    return html.Div(id='projects-container', children=[html.Div(project) for project in load_projects()])

# 启动Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
