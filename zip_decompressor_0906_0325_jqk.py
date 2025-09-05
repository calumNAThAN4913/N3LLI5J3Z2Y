# 代码生成时间: 2025-09-06 03:25:04
import dash
import dash_core_components as dcc
import dash_html_components as html
import zipfile
import os
from dash.dependencies import Input, Output, State
import plotly.express as px

# Define the app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
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
    html.Div(id='output-data-upload')
])

# Define the callback to handle the file upload and decompression
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(contents, filename, last_modified):
    # Check if the content is not empty
    if contents is not None:
        # Get the directory where to save the files
        directory = "./"
        for file_info in contents:
            # Get the name of the file
            file_name = file_info['filename']
            # Check if file is a zip
            if file_name.endswith(".zip"):
                # Create a bytes buffer
                file_bytes = file_info['contents']
                # Write the file in the directory
                with open(os.path.join(directory, file_name), "wb") as f:
                    f.write(file_bytes)
                # Unzip the file
                with zipfile.ZipFile(os.path.join(directory, file_name), 'r') as zip_ref:
                    zip_ref.extractall(directory)
                # Return the message indicating success
                return f'Files extracted successfully from {file_name}'
            else:
                # Return the message indicating failure
                return f'File {file_name} is not a zip file'
    else:
        # Return the message indicating no file was uploaded
        return 'No file uploaded'

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)