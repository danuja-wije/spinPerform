import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from app import app
import pymongo

client = pymongo.MongoClient("mongodb+srv://common:admin@cluster0.epwxvmc.mongodb.net/")
db = client["user_database"]
payment_collection = db["payment"]
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
    [Input('submit-button', 'n_clicks')],
    [State('card-number', 'value'),
     State('cvv', 'value'),
     State('expire-date', 'value')]
)
def update_payment_status(n_clicks, card_number, cvv, expire_date):
    if n_clicks == 0:
        raise PreventUpdate

    # Card Number Validation
    if not len(str(card_number)) == 16:
        return "Invalid Card Number"

    # CVV Validation
    if not len(str(cvv)) == 3:
        return "Invalid CVV"

    # Expiration Date Validation
    # try:
    #     exp_date = datetime.strptime(expire_date, "%m/%Y")
    #     if exp_date <= datetime.now():
    #         return "Card has expired"
    # except ValueError:
    #     return "Invalid Expiration Date format. Please use MM/YYYY."

    # Construct the data to be saved
    payment_data = {
        "card_number": card_number,
        "cvv": cvv,
        "expire_date": expire_date
    }

    # Connect to MongoDB and insert data
    try:
        payment_collection.insert_one(payment_data)
        return "Payment successful!"
    except pymongo.errors.PyMongoError as e:
        return f"Error: {str(e)}"  # Handle the error appropriately