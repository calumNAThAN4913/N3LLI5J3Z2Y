# 代码生成时间: 2025-09-23 12:56:00
import dash
import dash_auth
from dash import html, dcc
from dash.dependencies import Input, Output

# Define a simple user database
USERS = {
    'username1': 'password1',
    'username2': 'password2',
}

# Create the Dash application
app = dash.Dash(__name__)

# Setup the Dash authentication
auth = dash_auth.BasicAuth(
    app,
    # Use the custom authentication function
    auth_func=lambda username, password: username in USERS and USERS[username] == password,
)

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Define the callback to display the correct page
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/login':
        # Show the login page if the user is not authenticated
        return html.Div([
            html.H1('Login'),
            html.Div(
                dash_auth.BasicAuth(
                    app,
                    route='/',
                    # The page to redirect to after successful login
                    unauthorized_access_message='Please log in to view this page',
                ),
            ),
        ])
    elif pathname == '/':
        # Show the dashboard if the user is authenticated
        return html.Div([
            html.H1('Welcome to the Dashboard'),
            html.P('You are now logged in as ' + auth.get_user()),
            dcc.Link('Logout', href='/logout', className='btn btn-primary')
        ])
    else:
        # Return a 404 page if the path is not recognized
        return html.Div([
            html.H1('404 Page Not Found'),
            html.P('You have encountered a page that does not exist.'),
        ])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)