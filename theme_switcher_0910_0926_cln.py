# 代码生成时间: 2025-09-10 09:26:16
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# 定义Dash应用程序
app = dash.Dash(__name__)

# 设置应用的布局
app.layout = html.Div([
    html.P("Choose a theme: "),
    dcc.Dropdown(
        id='theme-selector',
        options=[
            {'label': 'Light', 'value': 'light'},
            {'label': 'Dark', 'value': 'dark'}
        ],
        value='light'  # 设置默认值为light
    ),
    html.Div(id='theme-output')
])

# 定义回调函数，用于根据选择的主题更改应用主题
@app.callback(
    Output('theme-output', 'children'),
    [Input('theme-selector', 'value')]
)
def update_output(value):
    # 根据选择的主题更新应用的布局
    if value == 'light':
        return 'You have selected the Light theme.'
    elif value == 'dark':
        return 'You have selected the Dark theme.'
    else:
        return 'Please select a valid theme.'

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)