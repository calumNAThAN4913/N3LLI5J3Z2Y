# 代码生成时间: 2025-09-05 16:36:40
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from pathlib import Path
import os

# 配置Dash应用的基础信息
APP_NAME = 'Test Report Generator'
SERVER_PORT = 8050

# 初始化Dash应用
app = dash.Dash(__name__)
app.title = APP_NAME

# 应用布局
app.layout = html.Div([
    html.H1('Test Report Generator'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'},
        # 允许多文件上传
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='test-report-graph'),
])

# 回调函数：处理文件上传
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    children = ''
    for i in range(len(list_of_contents)):
        children += f'文件名：{list_of_names[i]}，最后修改时间：{list_of_dates[i]} '
    return html.Div([html.H5('文件已上传：'), html.P(children)])

# 回调函数：生成测试报告图表
@app.callback(
    Output('test-report-graph', 'figure'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def generate_test_report(contents, filenames, dates):
    try:
        # 假设上传的是CSV文件，可以在此添加更多文件格式的处理
        if filenames is not None:
            # 提取第一个文件内容用于生成报告
            content_type, content_string = contents[0].split(',')
            decoded = content_string.decode('utf-8')
            df = pd.read_csv(pd.compat.StringIO(decoded))

            # 根据实际情况对DataFrame进行操作，生成报告
            # 例如：按组统计通过率
            test_pass_rate = df.groupby('test_group')['result'].value_counts(normalize=True).unstack().fillna(0)

            # 使用Plotly Express生成图表
            fig = px.imshow(test_pass_rate, aspect='auto', color_continuous_scale='Blues',
                         labels={'z': '通过率'}, colorbar_title='通过率')
            fig.update_layout(
                title='测试报告通过率分布图',
                xaxis_nticks=36
            )
            return fig
        else:
            return {}
    except Exception as e:
        # 错误处理
        return {'layout': {'annotations': [
            {'text': f'Error: {str(e)}', 'x': 0.5, 'y': 0.5, 'xanchor': 'center', 'yanchor': 'center', 'font': {'size': 20, 'color': 'red'}}
        ]}}

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True, port=SERVER_PORT)
