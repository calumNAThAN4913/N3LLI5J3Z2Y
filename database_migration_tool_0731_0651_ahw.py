# 代码生成时间: 2025-07-31 06:51:59
import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from sqlalchemy import create_engine

# 数据库连接配置
DATABASE_URI = 'sqlite:///database.db'

# 定义数据库迁移函数
def migrate_database(source_db, target_db, table_name):
    """
    迁移指定表的数据从源数据库到目标数据库。
    
    参数：
    - source_db: 源数据库URI
    - target_db: 目标数据库URI
    - table_name: 需要迁移的表名
    """
    try:
        # 创建数据库引擎
        engine = create_engine(source_db)
        # 读取表数据
        dataframe = pd.read_sql_table(table_name, engine)
        # 创建目标数据库引擎
        target_engine = create_engine(target_db)
        # 将数据写入目标数据库
        dataframe.to_sql(table_name, target_engine, if_exists='replace', index=False)
        return f"Data migration from {table_name} completed successfully."
    except Exception as e:
        return f"Error occurred during data migration: {str(e)}"

# 设置Dash应用
app = dash.Dash(__name__)

# 设置Dash布局
app.layout = html.Div(children=[
    html.H1(children='Database Migration Tool'),
    html.Div(children=[dcc.Input(id='source-db-uri', type='text', placeholder='Enter source database URI'),
                     dcc.Input(id='target-db-uri', type='text', placeholder='Enter target database URI'),
                     dcc.Input(id='table-name', type='text', placeholder='Enter table name')], style={'width': '50%', 'display': 'flex', 'justifyContent': 'space-between'}),
    html.Button('Migrate', id='migration-button', n_clicks=0),
    html.Div(id='migration-output')
])

# 定义Dash回调
@app.callback(
    Output(component_id='migration-output', component_property='children'),
    [Input(component_id='migration-button', component_property='n_clicks')],
    [State(component_id='source-db-uri', component_property='value'),
     State(component_id='target-db-uri', component_property='value'),
     State(component_id='table-name', component_property='value')]
)
def perform_migration(n_clicks, source_db_uri, target_db_uri, table_name):
    # 检查是否点击了按钮
    if n_clicks > 0:
        # 执行数据库迁移
        result = migrate_database(source_db_uri, target_db_uri, table_name)
        return result
    return ''

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)