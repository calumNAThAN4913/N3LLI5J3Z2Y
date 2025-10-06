# 代码生成时间: 2025-10-06 17:43:51
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate

# 定义学习资源库应用
class LearningResourceLibrary:
    def __init__(self):
        # 初始化Dash应用
        self.app = dash.Dash(__name__)
        self.app.title = "Learning Resource Library"

        # 定义应用布局
        self.layout()

    def layout(self):
        # 定义应用的布局，包括导航栏、表格和搜索框
        self.app.layout = html.Div([
            html.H1("Learning Resource Library"),
            html.Div([
                dcc.Input(id='search-input', type='text', placeholder='Search...'),
                html.Button('Search', id='search-button', n_clicks=0)
            ]),
            dcc.Dropdown(id='categories-dropdown', options=[], value=['All'], multi=True),
            dcc.Table(id='resources-table',
                      columns=[{"name": i, "id": i} for i in ["Title", "Author", "Category", "Year"]],
                      style_cell={'textAlign': 'left', 'fontFamily': 'sans-serif'}),
            html.Div(id='output-container')
        ])

    def callbacks(self):
        # 定义回调函数，处理用户输入并更新表格和布局
        @self.app.callback(
            Output('categories-dropdown', 'options'),
            [Input('search-button', 'n_clicks')]
        )
        def update_categories(n_clicks):
            if n_clicks is None:
                raise PreventUpdate
            # 从CSV文件加载数据
            df = pd.read_csv('resources.csv')
            # 获取唯一的类别
            categories = df['Category'].unique().tolist()
            # 添加'All'选项
            categories.insert(0, 'All')
            return [{'label': i, 'value': i} for i in categories]

        @self.app.callback(
            Output('resources-table', 'data'),
            [Input('search-button', 'n_clicks'), Input('categories-dropdown', 'value')],
            [State('search-input', 'value')]
        )
        def update_table(n_clicks, categories, search_query):
            if n_clicks is None:
                raise PreventUpdate
            # 从CSV文件加载数据
            df = pd.read_csv('resources.csv')
            # 过滤搜索结果
            if search_query:
                df = df[df['Title'].str.contains(search_query, case=False, na=False)]
            # 根据类别过滤
            if categories and 'All' not in categories:
                df = df[df['Category'].isin(categories)]
            # 返回过滤后的表格数据
            return df.to_dict('records')

    def run(self):
        # 运行Dash应用
        self.app.run_server(debug=True)

# 创建学习资源库应用实例并运行
if __name__ == '__main__':
    app = LearningResourceLibrary()
    app.callbacks()
    app.run()