# 代码生成时间: 2025-08-06 12:34:51
import dash
import dash_core_components as dcc
import dash_html_components as html
import json
from dash.dependencies import Input, Output

# 定义JSON数据格式转换器应用
class JsonConverterApp:
    def __init__(self, app):
        # 设置页面布局
        self.app = app
        app.layout = html.Div(children=[
            html.H1(children='JSON Data Format Converter'),
            html.Div(children=[
                dcc.Textarea(
                    id='json-input',
                    placeholder='Enter JSON data here...',
                    style={'width': '80%', 'height': '200px'}
                ),
                html.Button('Convert', id='convert-button', n_clicks=0)
            ]),
            html.Div(id='output-container')
        ])

        # 定义回调函数，将输入的JSON数据转换为其他格式
        @app.callback(
            Output('output-container', 'children'),
            [Input('convert-button', 'n_clicks')],
            [State('json-input', 'value')]
        )
        def update_output(n_clicks, json_input):
            if n_clicks == 0:
                # 如果按钮没有被点击，不进行任何操作
                return ''
            try:
                # 尝试将输入的字符串解析为JSON对象
                json_data = json.loads(json_input)
                # 将JSON对象转换为字符串
                formatted_json = json.dumps(json_data, indent=4)
                return html.Pre(formatted_json)
            except json.JSONDecodeError:
                # 如果解析JSON失败，返回错误信息
                return 'Invalid JSON data entered.'

# 创建Dash应用
def create_app():
    app = dash.Dash(__name__)
    JsonConverterApp(app)
    return app

# 运行Dash应用
if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True)