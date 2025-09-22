# 代码生成时间: 2025-09-22 15:05:37
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import sqlite3
from contextlib import closing

def prevent_sql_injection(query, params):
    # 防止SQL注入
    return query.replace('?', '%s')

def get_db_connection():
    # 获取数据库连接
    conn = sqlite3.connect('database.db')
    return conn

app = dash.Dash(__name__)

# 应用的布局
app.layout = html.Div([
    dcc.Input(id='input-field', type='text', placeholder='输入查询参数'),
    html.Button('查询', id='submit-button', n_clicks=0),
    html.Div(id='output-container')
])

# 回调函数 - 执行查询
@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-field', 'value')]
)
def execute_query(n_clicks, value):
    if n_clicks is None:  # 防止初始加载时触发
        raise PreventUpdate
    
    try:
        conn = get_db_connection()
        with closing(conn.cursor()) as cursor:  # 使用with语句确保资源正确释放
            # 构建查询语句并防止SQL注入
            query = prevent_sql_injection('SELECT * FROM users WHERE name = ?', (value,))
            cursor.execute(query)
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=['id', 'name', 'email'])
            
            # 返回查询结果
            return df.to_html(classes='table table-striped')
    except sqlite3.Error as e:
        # 错误处理
        return f'An error occurred: {e}'
    finally:  # 确保数据库连接关闭
        if conn:  # 如果连接打开，则关闭
            conn.close()

if __name__ == '__main__':
    app.run_server(debug=True)