# 代码生成时间: 2025-08-03 09:53:25
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import yaml
from pathlib import Path
import json

# Define the layout of the Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Config File Manager"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dcc.Dropdown(
        id='config-file-select',
        options=[],
        placeholder='Select a config file'
    ),
    html.Button('Load Config', id='load-config-button', n_clicks=0),
    dcc.Textarea(
        id='config-content',
        placeholder='Config content will be displayed here'
    ),
    html.Div(id='output-data-content')
])

# Function to read the config file and return its content
def read_config_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError:
        return "Error reading the file."

# Function to update the dropdown with config files
def update_dropdown(files):
    options = []
    for file in files:
        # Assuming .yml and .json are the config file extensions
        if file.suffix in ['.yml', '.json']:
            options.append({'label': file.name, 'value': str(file)})
    return options

# Callback to display the uploaded file names
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    state=[State('upload-data', 'filename'),
           State('upload-data', 'last_modified')]
)
def update_output(contents, filename, last_modified):
    if contents is not None:
        children = [
            html.H5(filename),
            html.H6(f'Last modified: {last_modified}'),
            dcc.Dropdown(
                id='file-select',
                options=update_dropdown([Path(filename)]),
                placeholder='Select a file'
            )
        ]
        return children
    return 'No file uploaded'

# Callback to load the selected config file content
@app.callback(
    Output('config-content', 'value'),
    [Input('config-file-select', 'value')]
)
def load_config(config_file):
    if config_file is not None:
        config_file_path = Path(config_file)
        return read_config_file(config_file_path)
    return ''

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)