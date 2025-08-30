# 代码生成时间: 2025-08-30 19:05:09
import dash
import dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import subprocess
import psutil
import sys

# ProcessManager class to encapsulate the logic
class ProcessManager:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.app.layout = self.create_layout()
        self.setup_callbacks()

    def create_layout(self):
        # Create the layout for the Dash app
        return html.Div([
            html.H1('Process Manager'),
            dcc.Input(id='process-name-input', type='text', placeholder='Enter process name'),
            html.Button('Search', id='search-button', n_clicks=0),
            dash_table.DataTable(
                id='process-table',
                columns=[{'name': i, 'id': i} for i in ['PID', 'Process Name', 'Memory Usage', 'CPU Usage']],
                page_size=10,
                style_table={'overflowX': 'auto'}
            )
        ])

    def setup_callbacks(self):
        @self.app.callback(
            Output('process-table', 'data'),
            [Input('search-button', 'n_clicks')],
            [State('process-name-input', 'value')]
        )
        def update_table(n_clicks, process_name):
            if n_clicks is None or process_name is None:
                raise dash.exceptions.PreventUpdate()

            # Get all running processes
            processes = [p.info for p in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent'])]

            # Filter processes by name
            filtered_processes = [p for p in processes if process_name.lower() in p['name'].lower()]

            return filtered_processes

    def run(self):
        self.app.run_server(debug=True)

# Check if the script is run directly
if __name__ == '__main__':
    try:
        manager = ProcessManager()
        manager.run()
    except Exception as e:
        print(f'An error occurred: {e}', file=sys.stderr)
