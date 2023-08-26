import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import pymongo
import dash_bootstrap_components as dbc
from app import app
# Define the layout of the login page
log = html.Div([
    html.Div([
        html.H1("Login"),
        html.Div([
            html.Div([
                html.Label("Email address"),
                dcc.Input(id="login-username-input",type="email",className="form-control",placeholder="Enter email"),
            ],className="login-inner-box-input"),
            html.Div([html.Label("Password"),
            dcc.Input(id="login-password-input", type="password",className="form-control",placeholder="Password")],className="login-inner-box-input"),
            
            html.Center([dbc.Button("Login",className="btn btn-light", id="login-button")]) ,
            html.Div(id="login-status")
        ])
    ],className="card login-inner-box"),
    html.Img(src=app.get_asset_url('login.gif'),id="login-vector")
    
],className="login-outer-box")

