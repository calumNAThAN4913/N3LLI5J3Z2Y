# 代码生成时间: 2025-09-13 09:58:40
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
from dash.dependencies import Input, Output, State\
import plotly.express as px\
import pandas as pd\
\
# 定义Dash应用\
app = dash.Dash(__name__)\
\
# 使用Pandas DataFrame模拟一些数据\
df = pd.DataFrame(\
    {
        'Year': [2015, 2016, 2017, 2018, 2019],\
        'Sales': [100, 120, 150, 180, 200],\
        'Profits': [30, 40, 60, 80, 100],\
    }
)\
\
# 响应式布局设计\
app.layout = html.Div(\
    [
        html.H1('响应式布局示例'),\
        dcc.Graph(id='line-graph', figure=px.line(df, x='Year', y='Sales')),\
        html.P('这是一段文本，演示响应式布局。'),\
        html.Div(\
            [
                html.Div(\
                    [
                        html.P("左侧面板"),\
                        dcc.Graph(id='pie-chart', figure=px.pie(df, names='Year', values='Sales')),\
                    ],\
                    id='left-panel',\
                    className='six columns',\
                ),\
                html.Div(\
                    [
                        html.P("右侧面板"),\
                        html.Div(id='right-panel-content'),\
                    ],\
                    id='right-panel',\
                    className='six columns',\
                ),\
            ],\
            className='row',\
        ),\
    ]
)\
\
# 回调函数：响应窗口大小变化\
@app.callback(\
    Output('right-panel-content', 'children'),\
    [Input('line-graph', 'clickData')],\
    [State('line-graph', 'figure')],\
)\
def update_output_div(clickData, figure):
    if clickData is None:
        raise dash.exceptions.PreventUpdate()
    
    # 根据点击的数据点更新右侧面板的内容
    if clickData['points'][0]['curveNumber'] != 0:
        raise dash.exceptions.PreventUpdate()
    
    # 点击的数据点对应的年份
    year = df['Year'][clickData['points'][0]['pointIndex']]
    
    # 显示点击年份的销售数据
    return html.P(f'您选中的年份是 {year}，销售额为 {clickData[