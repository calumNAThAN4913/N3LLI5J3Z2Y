# 代码生成时间: 2025-10-10 19:05:49
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# 定义投票系统应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(children=[
    html.H1("投票系统"),
    dcc.Dropdown(
        id='candidates-dropdown',
        options=[
            {'label': '候选人A', 'value': 'A'},
            {'label': '候选人B', 'value': 'B'},
            {'label': '候选人C', 'value': 'C'},
        ],
        value=['A'],  # 预设选中候选人A
        multi=True,  # 允许多选
    ),
    html.Button('投票', id='submit-button', n_clicks=0),
    html.Div(id='output-container'),
])

# 定义投票回调函数
@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('candidates-dropdown', 'value')],
)
def vote(n_clicks, selected_candidates):
    # 错误处理：防止未选择任何候选人时投票
    if not selected_candidates:
        return '请至少选择一个候选人'
    
    # 模拟投票过程
    votes = {
        'A': 0,
        'B': 0,
        'C': 0,
    }
    for candidate in selected_candidates:
        votes[candidate] += 1
    
    # 生成投票结果图表
    df = pd.DataFrame(list(votes.items()), columns=['Candidate', 'Votes'])
    fig = px.bar(df, x='Candidate', y='Votes', title='投票结果')
    
    # 返回投票结果图表和票数统计
    return html.Div([
        dcc.Graph(figure=fig),
        html.P(f'总票数：{sum(votes.values())}'),
    ])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)