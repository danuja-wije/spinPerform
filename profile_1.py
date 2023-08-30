import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
import pymongo
import pandas as pd
import plotly.express as px

client = pymongo.MongoClient("mongodb+srv://common:admin@cluster0.epwxvmc.mongodb.net/")
db = client["user_database"]
users_collection = db["users"]
# user1 = user.User("","")
history_collection = db["history"]
all_scorees = []

prof  = html.Div([
    html.Div([
        html.Div(children=[],className="scroll-container",id="profile-history"),
        html.Div([
            dcc.Graph(id='line-chart')
        ],className="profile-graph",id="profile-graph"),
    ],className="profile-inner-box-1"),
    html.Div([
        html.Div([
            html.H1("Profile"),
            html.Div([
                html.Div([
                    html.Label("Name"),
                    dcc.Input(id="profile-name-input",type="text",className="form-control",placeholder="Enter name"),
                ],className="profile-inner-box-input"),
                html.Div([
                    html.Label("Email"),
                    dcc.Input(id="profile-email-input",type="email",className="form-control",placeholder="Enter email",disabled=True),
                ],className="profile-inner-box-input"),
                html.Div([
                    html.Label("Password"),
                    dcc.Input(id="profile-password-input", type="password",className="form-control",placeholder="Password")],className="profile-inner-box-input"),
                html.Div([
                    html.Label("Confirm Password"),
                    dcc.Input(id="profile-confirm-password-input", type="password",className="form-control",placeholder="Password")],className="profile-inner-box-input"),
                html.Center([dbc.Button("Update",className="btn btn-light", id="profile-button")]) ,
                html.Div(id="profile-status",children=[])
            ])
        ],className="card profile-inner-box-input"),
        html.Img(src=app.get_asset_url('user_profile.gif'),id="profile-vector"),

    ],className="profile-inner-box-2"),
],className="profile-outer-box")

# Define the layout of the profile page
@app.callback([Output('profile-history', 'children'),Output('line-chart', 'figure'),Output('profile-name-input', 'value'),Output('profile-email-input', 'value')],[Input('profile', 'n_clicks'),Input("intermediate-value", "data"),Input('line-chart', 'relayoutData')])
def profile_history(n_clicks,current_user,relayout_data):
    
    query = {'username': current_user} 
    try:
        user = users_collection.find_one(query)

        if not current_user == 'False' or current_user is not None:
            query = {'user': current_user}  # Replace 'field_name' with your actual field name
            data = history_collection.find(query)
            card_elements = []
            for entry in data:
                all_scorees.append(entry['score'])
                card = dbc.Card(
                    dbc.CardBody([
                        html.H4(entry['score'], className='card-title'),
                        html.P(entry['leg_ball'], className='card-text'), 
                        html.P(entry['no_ball'], className='card-text'),  
                        html.P(entry['danger_ball'], className='card-text'), 
                        html.P(entry['arm-_ball'], className='card-text')  

                    ],className="single-card-body")
                )
                card_elements.append(card)
            df = pd.DataFrame(all_scorees, columns = ['score'])
            print(df)
            if relayout_data:
                return card_elements,px.line(df, x=df.index, y='score', title='Overall History'),user['name'],user['username']
    except:
        return [card_elements],px.line(df, x=df.index, y='score', title='Overall History'),"",""
    # print(current_user,"current_user profile")
    
            # return [card_elements]

# @app.callback([Output('profile-name-input', 'value'),Output('profile-email-input', 'value')],[Input('profile', 'n_clicks'),Input("intermediate-value", "data")])
# def update_field(n_clicks,current_user):
#     print(current_user,"current_user profile")
#     query = {'username': current_user} 
#     try:
#         user = users_collection.find_one(query)
#         return user['name'],user['username']
#     except:
#         return "",""


@app.callback(
    Output("profile-status", "children"),
    Input("profile-button", "n_clicks"),
    State("profile-name-input", "value"),
    State("profile-email-input", "value"),
    State("profile-password-input", "value"),
    State("profile-confirm-password-input", "value")
)
def update_profile(n_clicks, name, email, password, confirm_password):
    if n_clicks:
        if password != confirm_password:
            return "Passwords do not match."
        else:
            try:
                users_collection.update_one({"username": email}, {"$set": {"name": name, "password": password}})
                return "Profile updated successfully."
            except:
                return "Profile failed  to update."
    return ""