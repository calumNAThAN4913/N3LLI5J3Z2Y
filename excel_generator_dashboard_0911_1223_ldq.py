# 代码生成时间: 2025-09-11 12:23:03
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
from excel_utils import generate_excel

# 定义 Dash 应用
app = dash.Dash(__name__)
server = app.server

# 应用布局
app.layout = html.Div(
    [   dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ',
                        html.A('Select Files')]),
        style={'width': '50%', 'height': '60px', 'lineHeight': '60px', 
               'borderWidth': '1px', 'borderStyle': 'dashed', 
               'borderRadius': '5px', 'textAlign': 'center', 
               'margin': '10px'},
        # 允许上传多个文件
        multiple=True
    ),
    html.Div(id='output-data-upload', children=[])
]
)

# 回调函数，处理文件上传并生成Excel
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified'),
     State('upload-data', 'size')]
)
def upload_file(contents, filename, last_modified, size):
    # 如果没有上传文件，不执行任何操作
    if not contents:
        raise PreventUpdate
    
    try:
        # 读取上传的文件
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # 将文件内容转换为DataFrame
            df = pd.read_excel(io.BytesIO(decoded))
            # 生成Excel文件
            excel_file = generate_excel(df)
            # 显示下载链接
            return html.A('Download Generated Excel', 
                          href='data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + excel_file, 
                          download='generated_excel.xlsx')
        except Exception as e:
            print(e)
            return 'Error processing file'
    except Exception as e:
        print(e)
        return 'Error reading file'

# 定义一个生成Excel文件的函数
def generate_excel(df):
    # 创建一个BytesIO对象来存储Excel文件
    output = io.BytesIO()
    # 将DataFrame写入Excel文件
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    # 将BytesIO对象内容转换为base64编码的字符串
    output.seek(0)
    return base64.b64encode(output.getvalue()).decode('utf-8')

if __name__ == '__main__':
    app.run_server(debug=True)