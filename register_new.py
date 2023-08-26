import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import pymongo
import dash_bootstrap_components as dbc
from app import app
# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://common:admin@cluster0.epwxvmc.mongodb.net/")
db = client["user_database"]
users_collection = db["users"]

# Define the layout of the registration page
# reg = html.Div([
#     html.H1("Registration Page"),
#     html.Div([
#         html.Label("Username"),
#         dcc.Input(id="username-input", type="text"),
#         html.Label("Password"),
#         dcc.Input(id="password-input", type="password"),
#         html.Button("Register", id="register-button"),
#         html.Div(id="registration-status")
#     ])
# ])

reg = html.Div([
    html.Div([
        html.H1("Registration"),
        html.Div([
        dcc.Input(id='logger_store',value="reg", type='hidden'),
            html.Div([
                html.Label("Email address"),
                dcc.Input(id="username-input",type="email",className="form-control",placeholder="Enter email"),
            ],className="login-inner-box-input"),
            html.Div([html.Label("Password"),
            dcc.Input(id="password-input", type="password",className="form-control",placeholder="Password")],className="login-inner-box-input"),
            
            html.Center([dbc.Button("Register",className="btn btn-light", id="register-button")]) ,
            html.Div(id="register-status")
        ])
    ],className="card login-inner-box"),
    html.Img(src=app.get_asset_url('register.gif'),id="login-vector")
    
],className="login-outer-box")

log = html.Div([
    html.Div([
        dcc.Input(id='logger_store',value="login", type='hidden'),
        html.H1("Login"),
        html.Div([
            html.Div([
                html.Label("Email address"),
                dcc.Input(id="username-input",type="email",className="form-control",placeholder="Enter email"),
            ],className="login-inner-box-input"),
            html.Div([html.Label("Password"),
            dcc.Input(id="password-input", type="password",className="form-control",placeholder="Password")],className="login-inner-box-input"),
            
            html.Center([dbc.Button("Login",className="btn btn-light", id="register-button")]) ,
            html.Div(id="register-status")
        ])
    ],className="card login-inner-box"),
    html.Img(src=app.get_asset_url('login.gif'),id="login-vector")
    
],className="login-outer-box")

