# 代码生成时间: 2025-09-17 11:13:39
import os
from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
pm = imageio.imread
from PIL import Image
import numpy as np
import imageio
import base64
import io

"""
Image Resizer Application using Dash framework.
This application allows users to upload multiple images, select desired width and height, and then
resizes the images accordingly.
"""

# Define a function to resize images
def resize_image(image, width, height):
    img = Image.open(image)
    img = img.resize((width, height), Image.ANTIALIAS)
    return img

# Define a function to encode image to base64
def encode_image(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')

# Initialize the Dash application
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Image Resizer App"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dcc.Dropdown(
        id='resize-type',
        options=[{'label': 'Width', 'value': 'width'},
                 {'label': 'Height', 'value': 'height'}],
        value='width',
        multi=False
    ),
    dcc.Input(id='resize-value', type='number', placeholder='Enter size'),
    html.Button('Resize Images', id='resize-button', n_clicks=0),
    dcc.Loading(id='loading', type='default'),
    html.Div(id='resized-images')
])

# Define the callback to display uploaded images
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(entered, list_of_names, list_of_dates):
    if entered is None:
        raise PreventUpdate
    return html.Div([
        html.P(list_of_names),
        html.P(list_of_dates)
    ])

# Define the callback to resize images
@app.callback(
    Output('resized-images', 'children'),
    [Input('resize-button', 'n_clicks'), Input('resize-value', 'value'), Input('resize-type', 'value')],
    [State('upload-data', 'contents'), State('upload-data', 'filename')]
)
def resize_images(n_clicks, resize_value, resize_type, list_of_contents, list_of_names):
    ctx = dash.callback_context
    if not ctx.triggered or n_clicks < 1:
        raise PreventUpdate
    if list_of_contents is None:
        return dash.no_update

    resized_images = []
    for content, name in zip(list_of_contents, list_of_names):
        try:
            image = pm(io.BytesIO(content))
            if resize_type == 'width':
                resized = resize_image(image, resize_value, None)
            elif resize_type == 'height':
                resized = resize_image(image, None, resize_value)
            encoded_image = encode_image(resized)
            resized_images.append(html.Img(src='data:image/png;base64,{}'.format(encoded_image)))
        except Exception as e:
            print('Error resizing image', name, ':', str(e))

    return resized_images

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)