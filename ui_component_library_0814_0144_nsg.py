# 代码生成时间: 2025-08-14 01:44:15
import dash
from dash import html, dcc, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from dash.dependencies import MATCH, ALL
from dash_table import FormatTemplate

"""
用户界面组件库，提供了Dash框架中的常用组件。
这个库包含了不同种类的输入、输出和布局组件。
"""

# 初始化Dash应用
app = dash.Dash(__name__)

# 定义用户界面布局
app.layout = html.Div([
    # 标题
    html.H1("用户界面组件库"),
    
    # 文本输入框
    dcc.Input(id='input-text', type='text', placeholder='Enter text here'),
    
    # 数字输入框
    dcc.Input(id='input-number', type='number', placeholder='Enter number here'),
    
    # 下拉选择框
    dcc.Dropdown(id='dropdown', options=[{'label': i, 'value': i} for i in ['Option 1', 'Option 2', 'Option 3']], value='Option 1'),
    
    # 复选框
    dcc.Checklist(id='checklist', options=[{'label': i, 'value': i} for i in ['Option 1', 'Option 2', 'Option 3']], value=['Option 1']),
    
    # 单选按钮
    dcc.RadioItems(id='radio-items', options=[{'label': i, 'value': i} for i in ['Option 1', 'Option 2', 'Option 3']], value='Option 1'),
    
    # 滑动条
    dcc.Slider(id='slider', min=0, max=10, step=1, value=5),
    
    # 日期选择器
    dcc.DatePickerRange(id='date-picker-range', start_date='2022-01-01', end_date='2022-01-31'),
    
    # 表格
    dash_table.DataTable(id='table', columns=[{'name': i, 'id': i} for i in ['Column 1', 'Column 2', 'Column 3']], data=[{i: f"{i}{j}" for j, i in enumerate(['Column 1', 'Column 2', 'Column 3'])} for k in range(10)]),
    
    # 图表
    dcc.Graph(id='graph'),
    
    # 按钮
    html.Button('Click Me', id='button'),
])

"""
回调函数：点击按钮时更新表格数据
"""
@app.callback(
    Output('table', 'data'),
    Input('button', 'n_clicks'),
    State('table', 'data')
)
def update_table(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    return [dict(row, **{'Column 4': f'New Column {row[