# 代码生成时间: 2025-08-02 15:09:24
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# 定义主布局，包含主题切换按钮和用于展示主题的容器
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.RadioItems(
        id='theme-selector',  # 用于存储用户选择主题的组件ID
        options=[
            {'label': 'Light', 'value': 'light'},
            {'label': 'Dark', 'value': 'dark'}
        ],
        value='light'  # 默认主题
    ),
    html.Div(id='theme-content')  # 使用ID来标识内容区域
])

# 回调函数，用于根据用户选择的主题更新主题样式
@app.callback(
    Output('theme-content', 'children'),
    [Input('theme-selector', 'value')]
)
def update_theme(selected_theme):
    # 根据选择的主题设置不同的样式
    if selected_theme == 'light':
        return html.Div([
            html.Div("Hello, this is the light theme!"),
            # 可以添加更多组件和样式
        ], style={'backgroundColor': 'white'})
    elif selected_theme == 'dark':
        return html.Div([
            html.Div("Hello, this is the dark theme!"),
            # 可以添加更多组件和样式
        ], style={'backgroundColor': 'black', 'color': 'white'})
    else:
        # 如果输入未知，防止更新
        raise PreventUpdate

# 运行Dash应用程序
if __name__ == '__main__':
    app.run_server(debug=True)