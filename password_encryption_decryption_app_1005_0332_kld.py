# 代码生成时间: 2025-10-05 03:32:25
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from cryptography.fernet import Fernet

# 定义密码加密解密工具的函数
def encrypt_password(password: str) -> str:
    # 生成密钥
    key = Fernet.generate_key()
    f = Fernet(key)
    # 加密密码
    encrypted_password = f.encrypt(password.encode()).decode()
    return encrypted_password, key


def decrypt_password(encrypted_password: str, key: str) -> str:
    # 使用密钥解密密码
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password.encode()).decode()
    return decrypted_password

# 初始化Dash应用
app = dash.Dash(__name__)

# 设置应用的布局
app.layout = html.Div([
    html.H1("Password Encryption Decryption Tool"),
    html.Hr(),
    html.Div([
        html.Div([
            html.Label("Password"),
            dcc.Input(id="password-input", type="text")
        ], className="six columns"),
        html.Div([
            html.Label("Key"),
            dcc.Input(id="key-input", type="text", value="")
        ], className="six columns"),
    ], className="row"),
    html.Button("Encrypt", id="encrypt-button", n_clicks=0),
    html.Br(),
    html.Div(id="encrypt-output"),
    html.Button("Decrypt", id="decrypt-button", n_clicks=0),
    html.Br(),
    html.Div(id="decrypt-output"),
], className="container")

# 定义回调函数处理加密操作
@app.callback(
    Output("encrypt-output", "children"),
    [Input("encrypt-button", "n_clicks"), Input("password-input", "value")],
    [State("password-input", "value"), State("key-input", "value")],
)
def encrypt(n_clicks, password, key):
    if n_clicks is None or password is None or key is None:
        raise PreventUpdate
    encrypted_password, new_key = encrypt_password(password)
    return f"Encrypted Password: {encrypted_password}
Key: {new_key}
"

# 定义回调函数处理解密操作
@app.callback(
    Output("decrypt-output", "children"),
    [Input("decrypt-button", "n_clicks"), Input("password-input", "value")],
    [State("password-input", "value"), State("key-input", "value")],
)
def decrypt(n_clicks, encrypted_password, key):
    if n_clicks is None or encrypted_password is None or key is None:
        raise PreventUpdate
    try:
        decrypted_password = decrypt_password(encrypted_password, key)
        return f"Decrypted Password: {decrypted_password}
"
    except Exception as e:
        return str(e)

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)