# 代码生成时间: 2025-08-23 20:24:49
# 防止SQL注入的Dash应用示例

# 导入必要的库
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import sqlite3
from urllib.parse import quote_plus

# 初始化Dash应用
app = dash.Dash(__name__)

# 定义布局
app.layout = html.Div(
    children=[
        html.H1('防止SQL注入的Dash应用'),
        html.Div(
            children=[
                dcc.Input(id='input-query', type='text', placeholder='输入查询条件'),
                html.Button('查询', id='submit-button', n_clicks=0),
                html.Div(id='output-container')
            ]
        )
    ]
)

# 定义回调函数，处理查询请求
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='submit-button', component_property='n_clicks')],
    [State(component_id='input-query', component_property='value')]
)
def query_database(n_clicks, query_value):
    # 错误处理
    if n_clicks == 0:
        return '请先点击查询按钮。'

    # 检查输入是否为空
    if not query_value:
        return '查询参数不能为空。'
    
    # 使用quote_plus对输入进行URL编码，防止SQL注入
    sanitized_query = quote_plus(query_value)
    
    # 连接数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    try:
        # 编写参数化的SQL查询，防止SQL注入
        cursor.execute('SELECT * FROM users WHERE name LIKE ?', (f'%{sanitized_query}%',))
        rows = cursor.fetchall()
        
        # 将查询结果转换为字符串输出
        output = '<br>'.join([f'Name: {row[0]}, Age: {row[1]}' for row in rows])
        
    except sqlite3.DatabaseError as e:
        # 错误处理
        output = f'数据库错误: {e}'
    finally:
        # 关闭数据库连接
        conn.close()
    
    return output

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)