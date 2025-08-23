# 代码生成时间: 2025-08-23 09:30:18
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "your_database",
    "user": "your_username",
    "password": "your_password",
    "port": 5432
}

# Create a database connection pool
def create_db_pool():
    """
    Create a database connection pool.
    :return: A psycopg2 connection pool object.
    """
    try:
        return pool.SimpleConnectionPool(1, 20, **DB_CONFIG)
    except psycopg2.Error as e:
        print(f"Error creating database pool: {e}")
        return None

# Get a connection from the pool
def get_connection(pool):
    """
    Get a connection from the pool.
    :param pool: A psycopg2 connection pool object.
    :return: A psycopg2 connection object or None if no connection is available.
    """
    try:
        return pool.getconn()
    except psycopg2.Error as e:
        print(f"Error getting connection from pool: {e}")
        return None

# Release a connection back to the pool
def release_connection(pool, conn):
    """
    Release a connection back to the pool.
    :param pool: A psycopg2 connection pool object.
    :param conn: A psycopg2 connection object.
    """
    try:
        pool.putconn(conn)
    except psycopg2.Error as e:
        print(f"Error releasing connection to pool: {e}")

# Close the database connection pool
def close_db_pool(pool):
    """
    Close the database connection pool.
    :param pool: A psycopg2 connection pool object.
    """
    try:
        pool.closeall()
    except psycopg2.Error as e:
        print(f"Error closing database pool: {e}")

# Main Dash application
app = Dash(__name__)

# Layout of the Dash application
app.layout = html.Div([
    html.H1("Database Connection Pool Manager"),
    dcc.Input(id='query-input', type='text', placeholder='Enter a SQL query'),
    html.Button("Execute Query", id="execute-button", n_clicks=0),
    html.Div(id="output")
])

# Callback to execute a SQL query and display the result
@app.callback(
    Output("output", "children"),
    [Input("execute-button", "n_clicks")],
    [State("query-input", "value")]
)
def execute_query(n_clicks, query):
    if n_clicks == 0:
        return html.Div(["Click the button to execute a query."])

    pool = create_db_pool()
    if pool is None:
        return html.Div(["Failed to create database pool."])

    conn = get_connection(pool)
    if conn is None:
        return html.Div(["Failed to get connection from pool."])

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return html.Div([
            html.P("Query executed successfully."),
            html.Table([
                html.Tr([html.Th(col) for col in result.keys()]),
                *[html.Tr([html.Td(cell) for cell in result.values()])
                    for result in results]
            ])
        ])
    except psycopg2.Error as e:
        return html.Div(["Error executing query: ", html.Code(str(e))])
    finally:
        release_connection(pool, conn)
        close_db_pool(pool)

if __name__ == '__main__':
    app.run_server(debug=True)
