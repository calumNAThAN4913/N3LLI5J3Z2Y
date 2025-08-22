# 代码生成时间: 2025-08-22 09:02:43
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import subprocess
import psutil
import sys

# Process Manager dashboard layout
def process_manager_layout():
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("Process Manager"),
        dcc.Input(id='process-name-input', type='text', placeholder='Enter process name'),
        html.Button('Kill Process', id='kill-process-button', n_clicks=0),
        dash_table.DataTable(
            id='process-table',
            columns=[{'name': 'PID', 'id': 'PID'}, {'name': 'Process Name', 'id': 'Process Name'}],
            page_size=10,
            style_data_conditional=[{'if': {'column_id': 'PID'}, 'textAlign': 'center'}],
            css=[{'selector': '.row', 'rule': 'margin-top: 5px'}]),
        dcc.Markdown(id='output-container')
    ])

    # Function to update the table with current processes
    def update_process_table():
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                processes.append({'PID': proc.info['pid'], 'Process Name': proc.info['name']})
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return pd.DataFrame(processes).to_dict('records')

    # Callback to update process table
    @app.callback(
        Output('process-table', 'data'),
        [Input('process-name-input', 'value')]
    )
    def update_table(input_value):
        if input_value:
            filtered_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if input_value.lower() in proc.info['name'].lower():
                        filtered_processes.append({'PID': proc.info['pid'], 'Process Name': proc.info['name']})
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return pd.DataFrame(filtered_processes).to_dict('records')
        return update_process_table()

    # Callback to handle process killing
    @app.callback(
        Output('output-container', 'children'),
        [Input('kill-process-button', 'n_clicks')],
        [State('process-table', 'active_cell'), State('process-name-input', 'value')]
    )
    def kill_process(n_clicks, active_cell, process_name):
        if n_clicks > 0 and active_cell is not None and active_cell['row'] is not None:
            pid_to_kill = active_cell['row']
            try:
                process = psutil.Process(pid_to_kill)
                process.terminate()
                process.wait()
                return f'Process with PID {pid_to_kill} terminated successfully.'
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                return f'Failed to terminate process with PID {pid_to_kill}. Error: {e}'
        return ''

    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)

if __name__ == '__main__':
    process_manager_layout()