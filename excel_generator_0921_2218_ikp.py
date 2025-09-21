# 代码生成时间: 2025-09-21 22:18:31
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from io import BytesIO
import base64

# 定义 Dash 应用程序的初始化函数
app = dash.Dash(__name__)

# 定义 Dash 布局
app.layout = html.Div([
    html.H1("Excel 表格自动生成器"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
        style={'width': '50%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
    ),
    html.Div(id='output-data-upload'),
    html.Button('生成Excel', id='generate-excel', n_clicks=0),
    html.Div(id='excel-output'),
])

# 定义回调函数，处理文件上传
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(entered, filename):
    if entered is not None:
        return html.Div([html.H5(filename), html.H6(entered.keys())])
    return 'Drop or select files to upload'

# 定义回调函数，生成Excel文件
@app.callback(
    Output('excel-output', 'children'),
    [Input('generate-excel', 'n_clicks')],
    [State('output-data-upload', 'children'), State('upload-data', 'contents')])
def generate_excel(n_clicks, children, contents):
    if contents is not None and n_clicks > 0:
        df = pd.DataFrame(contents)
        # 将DataFrame转换为Excel文件
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        # 编码Excel文件，使其可以在客户端下载
        excel_str = base64.b64encode(output.getvalue()).decode()
        return html.A(
            "下载Excel文件",
            href=f'data:application/vnd.ms-excel;base64,{excel_str}',
            download='output.xlsx'
        )
    return None

# 运行Dash应用程序
if __name__ == '__main__':
    app.run_server(debug=True)