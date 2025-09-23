# 代码生成时间: 2025-09-23 23:08:56
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
from flask import escape
from dash.exceptions import PreventUpdate

# API响应格式化工具
class ApiResponseFormatter:
    def __init__(self, app):
        """初始化API响应格式化工具"""
        self.app = app
        self.app.layout = html.Div([
            html.H1("API响应格式化工具"),
            dcc.Textarea(
                id='api_response_input',
                placeholder='粘贴API响应内容...',
                style={'width': '100%', 'height': '200px'}
            ),
            html.Button('格式化', id='format_button'),
            dcc.Textarea(
                id='formatted_response_output',
                placeholder='格式化后的响应内容将显示在这里...',
                style={'width': '100%', 'height': '200px', 'border': '1px solid black'},
                readOnly=True
            )
        ])
        self.app.callback(
            Output('formatted_response_output', 'value'),
            [Input('format_button', 'n_clicks')],
            [State('api_response_input', 'value')]
        )(self._format_response)

    def _format_response(self, n_clicks, api_response_input):
        """格式化API响应内容"""
        if not n_clicks or not api_response_input.strip():
            raise PreventUpdate
        try:
            # 尝试解析JSON响应内容
            response_data = escape(
                json.dumps(
                    json.loads(api_response_input),
                    indent=4,
                    ensure_ascii=False
                )
            )
            return response_data
        except json.JSONDecodeError as e:
            # 处理JSON解析错误
            return f'JSON解析错误：{str(e)}'

# 运行Dash应用程序
def run_dash_app():
    """运行Dash应用程序"""
    import json
    import dash
    app = dash.Dash(__name__)
    api_formatter = ApiResponseFormatter(app)
    app.run_server(debug=True)

if __name__ == '__main__':
    run_dash_app()