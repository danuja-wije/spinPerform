import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd

email_input = html.Div(
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="example-email", placeholder="Enter email"),
        dbc.FormText(
            "Are you on email? You simply have to be these days",
            color="secondary",
        ),
    ],
    className="mb-3",
)

password_input = html.Div(
    [
        dbc.Label("Password", html_for="example-password"),
        dbc.Input(
            type="password",
            id="example-password",
            placeholder="Enter password",
        ),
        dbc.FormText(
            "A password stops mean people taking your stuff", color="secondary"
        ),
    ],
    className="mb-3",
)
dbc.Input(type="hidden", id="logger", value="True")
submit_button = html.Div(
    [
        dbc.Button("Submit", color="primary",className="mr-1"),
    ])

form = dbc.Form([email_input, password_input,submit_button])

@callback(Output('intermediate-value', 'data'), Input('logger', 'value'))
def set_logger(value):
    return value
