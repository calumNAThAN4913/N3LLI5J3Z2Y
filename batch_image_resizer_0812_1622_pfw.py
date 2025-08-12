# 代码生成时间: 2025-08-12 16:22:54
import os
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import PIL
from PIL import Image
import glob
import base64
import io
import numpy as np
import pandas as pd

# Constants
IMAGE_EXTENSIONS = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']
RESIZED_IMAGE_FOLDER = 'resized_images'

# Initialize Dash app
app = Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ',
                        html.A('Select Files')]),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed',
                'borderRadius': '5px', 'textAlign': 'center',
                'margin': '10px'},
        # Allowed file extensions
        accept='.png,.jpg,.jpeg,.bmp,.gif',
    ),
    html.Div(id='output-data-upload')
])

# Callback to resize images
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')]
)
def resize_images(contents):
    # Check if contents are not None
    if contents is None:
        return 'No files uploaded'

    # Create a directory for resized images if it doesn't exist
    if not os.path.exists(RESIZED_IMAGE_FOLDER):
        os.makedirs(RESIZED_IMAGE_FOLDER)

    # List to store image file paths
    resized_image_paths = []

    # Loop through each file in the contents
    for i, content in enumerate(contents):
        try:
            # Get filename and create a new filename for the resized image
            filename = content.filename
            _, file_extension = os.path.splitext(filename)
            new_filename = 'resized_' + filename
            file_path = os.path.join(RESIZED_IMAGE_FOLDER, new_filename)
            resized_image_paths.append(new_filename)

            # Read the image file as bytes and open using PIL
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)
            image = Image.open(io.BytesIO(decoded))

            # Resize the image
            width, height = image.size
            new_height = 300
            new_width = int(width * (new_height / height))
            image = image.resize((new_width, new_height))

            # Save the resized image
            image.save(file_path)
        except Exception as e:
            # Handle any errors that occur during image resizing
            return f'Error resizing image {filename}: {str(e)}'

    # Return a list of resized image paths
    return [html.Li(path) for path in resized_image_paths]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)