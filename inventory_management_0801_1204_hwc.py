# 代码生成时间: 2025-08-01 12:04:09
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate

# App 的布局
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='库存管理系统'),
    dcc.Input(id='item-name', type='text', placeholder='输入商品名称...'),
    html.Button('添加商品', id='add-item-button', n_clicks=0),
    dcc.Dropdown(id='item-dropdown', options=[], value='', multi=True),
    html.Div(id='live-update'),
    html.Table(id='inventory-table', children=[
        html.Thead(
            html.Tr([html.Th(col) for col in ['商品名称', '数量', '操作']])),
        html.Tbody(id='table-body')
    ])
])

# 初始库存数据
inventory_data = pd.DataFrame(columns=['商品名称', '数量'])

# 回调函数：添加商品到库存
@app.callback(
    Output('live-update', 'children'),
    [Input('add-item-button', 'n_clicks')],
    [State('item-name', 'value'), State('item-dropdown', 'value')]
)
def add_item(n_clicks, item_name, dropdown_value):
    if n_clicks is None or item_name is None or item_name.strip() == '':
        raise PreventUpdate
    if dropdown_value is None:
        dropdown_value = []
    item_name = item_name.strip()
    if item_name in inventory_data['商品名称'].values:  # 检查商品是否已存在
        return f'商品 {item_name} 已存在。'
    # 添加新商品
    inventory_data = inventory_data.append({'商品名称': item_name, '数量': 0}, ignore_index=True)
    return f'商品 {item_name} 已添加。'

# 回调函数：更新库存数据
@app.callback(
    Output('inventory-table', 'children'),
    [Input('inventory-table', 'children')],
    [State('inventory-table', 'children'), State('inventory-table', 'children')]
)
def update_table(rows, children, table_children):
    if not inventory_data.empty:
        return [
            html.Thead(
                html.Tr([html.Th(col) for col in ['商品名称', '数量', '操作']])),
            html.Tbody(
                children=[
                    html.Tr(
                        children=[
                            html.Td(inventory_data.iloc[i]['商品名称']),
                            html.Td(
                                dcc.Input(
                                    id={'type': 'item-quantity', 'index': i},
                                    value=inventory_data.iloc[i]['数量'],
                                    type='number',
                                    min='0'
                                )
                            ),
                            html.Td(
                                html.Button('删除', id={'type': 'delete-item', 'index': i})
                            )
                        ]
                    ) for i in range(len(inventory_data))
                ]
            )
        ]
    raise PreventUpdate

# 回调函数：删除商品
@app.callback(
    Output({'type': 'item-quantity', 'index': 'index'}, 'value'),
    [Input({'type': 'delete-item', 'index': 'index'}, 'n_clicks')],
    [State({'type': 'item-quantity', 'index': 'index'}, 'value')]
)
def delete_item(n_clicks, index):
    if n_clicks is None:
        raise PreventUpdate
    # 删除库存数据中的商品
    inventory_data = inventory_data.drop(index)
    return ''

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)