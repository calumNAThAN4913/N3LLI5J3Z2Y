# 代码生成时间: 2025-09-16 13:34:50
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
from bs4 import BeautifulSoup

"""
Web Content Extractor using DASH framework
This application allows users to enter a URL and extract web content from the given webpage.

@author: Your Name
@version: 1.0
"""

# Define the layout of the Dash application
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Web Content Extractor"),
    dcc.Input(id='url-input', type='text', placeholder='Enter URL here'),
    html.Button('Extract Content', id='extract-button', n_clicks=0),
    dcc.Markdown(id='extracted-content')
])

# Define the callback function to handle the button click event
@app.callback(
    Output(component_id='extracted-content', component_property='children'),
    [Input(component_id='extract-button', component_property='n_clicks')],
    [State(component_id='url-input', component_property='value')]
)
def extract_content(n_clicks, url):
    """
    Extracts the content from the webpage specified in the url input field.
    
    Args:
        n_clicks (int): Number of times the button has been clicked.
        url (str): The URL of the webpage to extract content from.
    
    Returns:
        str: The extracted content from the webpage.
    
    Raises:
        Exception: If there is an error while extracting content.
    """
    if n_clicks == 0:
        # Return an empty string if the button has not been clicked
        return ''
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve webpage. Status code: {response.status_code}")
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove all script and style elements from the HTML
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get the text content from the parsed HTML
        text = soup.get_text()
        
        # Break the text into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("
"))
        
        # Drop blank lines
        text = '
'.join(chunk for chunk in chunks if chunk)
        
        return f"Extracted Content: 

{text}"
    except Exception as e:
        # Return an error message if there is an error while extracting content
        return f"Error: {str(e)}"

# Run the Dash server
if __name__ == '__main__':
    app.run_server(debug=True)