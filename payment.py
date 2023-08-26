import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
payment = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H1("Payment Options", className="text-center"),
                className="mb-4"
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Label("Card Number"),
                className="mb-3"
            ),
            dbc.Col(
                dcc.Input(id='card-number', type='text', className="form-control"),
                className="mb-3"
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Label("CVV"),
                className="mb-3"
            ),
            dbc.Col(
                dcc.Input(id='cvv', type='password', className="form-control"),
                className="mb-3"
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Label("Expiration Date"),
                className="mb-3"
            ),
            dbc.Col(
                dcc.Input(id='expire-date', type='text', placeholder="MM/YYYY", className="form-control"),
                className="mb-3"
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Alert(id='payment-status', color="success", className="mt-3"),
                width=6
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Button("Submit Payment", id='submit-button', n_clicks=0, className="btn btn-primary btn-lg mt-3")
            )
        ])
    ],style={'width':'50%','margin':'auto'}),
    html.Img(src=app.get_asset_url('pay.gif'),id="login-vector")
],className="pay-outer-box",style={'display':'flex','align-items':'center','justify-content':'center'})

@app.callback(
    Output('payment-status', 'children'),
    Input('submit-button', 'n_clicks')
)
def update_payment_status(n_clicks):
    if n_clicks > 0:
        return "Payment successful!"
    return ""

