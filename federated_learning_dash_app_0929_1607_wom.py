# 代码生成时间: 2025-09-29 16:07:05
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
import pandas as pd
import numpy as np
from dash import no_update
from dash_extensions import Download
import os
import base64
from io import BytesIO

def generate_classification_data():
    # Generate a simple classification dataset
    X, y = make_classification(n_samples=100, n_features=3, n_informative=2, n_redundant=0, random_state=42)
    df = pd.DataFrame(X, columns=['Feature1', 'Feature2', 'Feature3'])
    df['Target'] = y
    return df

def train_model(df):
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df.drop('Target', axis=1), df['Target'], test_size=0.2, random_state=42)
    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    # Evaluate the model's performance
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

def get_model_metrics(df):
    # Train the model and get its metrics
    accuracy = train_model(df)
    return accuracy

def download_csv(df):
    # Convert the DataFrame to CSV and return it as a downloadable link
    csv = df.to_csv(index=False)
    data = 'data:text/csv;charset=utf-8,' + urllib.parse.quote(csv)
    return data
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Federated Learning Dashboard'),
    html.Div(children=[
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')],
            style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}
        ),
        html.Div(id='output-data-upload'),
    ]),
    html.Div(children=[
        dcc.Graph(id='data-visualization'),
        html.Div(id='model-metrics'),
    ]),
    html.Div(children=[
        Download(id='download-link', content_type='text/csv'),
    ])
])
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_output(entered, filename, last_modified):
    if entered is None:
        raise PreventUpdate
    file = BytesIO(entered)
    df = pd.read_csv(file)
    return f'File {filename} uploaded successfully.'
@app.callback(
    Output('data-visualization', 'figure'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_graph(entered, filename, last_modified):
    if entered is None:
        raise PreventUpdate
    file = BytesIO(entered)
    df = pd.read_csv(file)
    fig = px.scatter(df, x='Feature1', y='Feature2', color='Target')
    return fig
@app.callback(
    Output('model-metrics', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_metrics(entered, filename, last_modified):
    if entered is None:
        raise PreventUpdate
    file = BytesIO(entered)
    df = pd.read_csv(file)
    accuracy = get_model_metrics(df)
    return f'Model accuracy: {accuracy:.2f}%'
@app.callback(
    Output('download-link', 'content'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_download(entered, filename, last_modified):
    if entered is None:
        raise PreventUpdate
    file = BytesIO(entered)
    df = pd.read_csv(file)
    csv = download_csv(df)
    return csv
if __name__ == '__main__':
    app.run_server(debug=True)