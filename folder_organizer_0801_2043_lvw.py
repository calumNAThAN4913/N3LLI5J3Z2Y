# 代码生成时间: 2025-08-01 20:43:35
import os
import shutil
from dash import Dash, html, dcc, Input, Output

"""
Folder Organizer is a Python script that uses the Dash framework to create a web application
for organizing and sorting files in a specified directory.

This application allows users to select a directory and set rules to move files into
subfolders based on specific criteria, such as file extension or creation date.
"""

class FolderOrganizer:
    def __init__(self):
        self.app = Dash(__name__)
        self.app.layout = html.Div(children=[
            html.H1(children='Folder Organizer'),
            dcc.Upload(
                id='upload-directory',
                children=html.Button('Upload Directory'),
                description='Drag and Drop or click to upload your directory',
                multiple=True
            ),
            html.Div(id='directory-content'),
            html.Button('Organize', id='organize-button', n_clicks=0),
            html.Div(id='output')
        ])

        @self.app.callback(
            Output('directory-content', 'children'),
            [Input('upload-directory', 'contents')],
        )
        def update_output(list_of_contents):
            if list_of_contents is not None:
                children = []
                for i in range(len(list_of_contents)):
                    children.append(
                        html.Div(
                            [
                                html.P(f'Name: {list_of_contents[i][