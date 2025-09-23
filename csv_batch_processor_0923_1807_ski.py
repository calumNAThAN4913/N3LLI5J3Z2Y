# 代码生成时间: 2025-09-23 18:07:29
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import os
from dash.exceptions import PreventUpdate

# Define the CSV batch processor application
class CSVBatchProcessor:
    def __init__(self, title='CSV Batch Processor'):
        self.title = title
        self.app = dash.Dash(__name__)
        self.app.title = title
        self.app.layout = html.Div([
            html.H1(self.title),
            dcc.Upload(
                id='upload-data',
                children=html.Button('Upload CSV files'),
                multiple=True,
            ),
            html.Div(id='output-container'),
        ])

        @self.app.callback(
            Output('output-container', 'children'),
            [Input('upload-data', 'contents')],
        )
        def process_uploaded_files(contents):
            if not contents:
                raise PreventUpdate

            # Process each uploaded file
            output = []
            for content in contents:
                try:
                    # Ensure the file is a CSV
                    if '.csv' not in content.filename:
                        output.append(f'{content.filename} is not a CSV file.')
                        continue

                    # Read the content of the file
                    df = pd.read_csv(content)
                    df.to_csv(f'processed_{content.filename}', index=False)

                    # Append the success message
                    output.append(f'{content.filename} processed successfully.')
                except Exception as e:
                    # Handle any errors that occur during processing
                    output.append(f'Error processing {content.filename}: {str(e)}')

            return '
'.join(output)

    def run(self):
        self.app.run_server(debug=True)

# Create an instance of the CSVBatchProcessor and run it
if __name__ == '__main__':
    processor = CSVBatchProcessor()
    processor.run()