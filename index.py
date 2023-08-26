import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pymongo
import shutil
from app import app
from app import server

import evaluate,register_new,login,profile,payment
import user

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://common:admin@cluster0.epwxvmc.mongodb.net/")
db = client["user_database"]
users_collection = db["users"]
user1 = user.User("","")
history_collection = db["history"]

@app.callback(Output('signout-value', 'data'),
              Input('signout', 'n_clicks'))
def signout(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return "False"

header = html.Div([
    dbc.Row([
        # html.Img(src=app.get_asset_url('logo.jpg'), id='logo', style ,height='100px'),
        dbc.Nav(
    [
        dbc.NavItem(html.Img(src=app.get_asset_url('logo.png'), id='logo', height='100px', style={'padding':'10px'})),
        dbc.NavItem(dbc.NavLink(html.H1("SpinPerform"),id='logo-text', active=True, href="/")),
        # dbc.NavItem(dbc.NavLink("A link", href="#")),
        # dbc.NavItem(dbc.NavLink("Another link", href="#")),
        # dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#")),
        html.Div(id='nav_home', children=[],style={'margin-left':'auto','padding':'10px','display':'flex','align-items':'center','justify-content':'center'}),

    ],style={'textAlign':'center'}
)
    ],style={'display':'flex','align-items':'center','justify-content':'center','padding':'10px'}),
    
], className='header_box')

container = html.Div([
    html.Div([
        html.Div([
            html.H1('Boost your skills with new technologies..', className='title'),
            html.Div([
                dbc.Button('Evaluate', className='btn-started', href='/Evaluate'),
                # dbc.Button('Learn More', color='primary', className='btn-started', href='/about'),
            ], className='line'),
        ], className='main-container-word-box'),
        html.Img(src=app.get_asset_url('p3.png'), id='main-vector')  
    ], className='main-container-box'),
], className='container-fluid')
app.layout = html.Div(
    [
        # dcc.Input(id='logger_store',value="False", type='hidden'),
        dcc.Store(id='intermediate-value'),
        dcc.Store(id='signout-value'),
        dcc.Location(id='url', refresh=False),
        header,
        dcc.Loading(type='default', id='loading-1', children=[
            html.Div(id='page_content', children=[]),
        ]),
    ], className='container-fluid'
)
# @app.callback(Output('nav_home', 'children'),[Input("intermediate-value", "data"),Input("signout-value", "data")])
# def logger_checker(logger,sign):
#     print("logger_checker",logger)
#     print("sign",sign)
#     if not logger == 'False' and  logger is not None:
#         if not sign == "False":
#             return [
#                 # dbc.Button("Sign Out" ,id="signout" , className="mr-1", href='/signout'),
#                 html.Div(id='img-circle', children=[],style={'padding':'10px','background':'url(https://www.w3schools.com/howto/img_avatar.png) center / cover','width':'50px','height':'50px','border-radius':'50%','margin-right':'10px'}),
#                 # html.Img(src=app.get_asset_url('user.webp'),id='user', height='80px', style={'padding':'10px'},className="img-circle"),
#                 dbc.DropdownMenu(
#                     children=[
#                         dbc.DropdownMenuItem(logger, header=True),
#                         dbc.DropdownMenuItem("Profile", href="/profile",id="profile"),
#                         dbc.DropdownMenuItem("Signout", href="/signout",id="signout"),
#                     ],
#                     nav=True,
#                     in_navbar=True,
#                     # label=html.Img(src=app.get_asset_url('user.jpg'),id='user', height='30px', style={'padding':'10px'},className="img-circle"),
#                 ),
#                 # dbc.Button("Sign In" ,id="signin" , className="mr-1", href='/signin'),
#                 # dbc.Button("Sign Up", color="primary", id="signup",className="mr-1", href='/signup'),
#             ]
#     else:
#         return [
#             dbc.Button("Sign In" ,id="signin" , className="mr-1", href='/signin'),
#             dbc.Button("Sign Up", color="primary", id="signup",className="mr-1", href='/signup'),
#         ]
# Define callback to handle registration
@app.callback(
    [Output("url", "pathname"),Output('intermediate-value', 'data'),Output('register-status', 'children')],
    [Input("register-button", "n_clicks"),Input('logger_store', 'value')],
    State("username-input", "value"),
    State("password-input", "value"),
)
def register_user(n_clicks,logger, username, password):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if logger == "reg":
            if not username or not password:
                return "/signup","False","Username and password are required."
            # Check if the username already exists
            existing_user = users_collection.find_one({"username": username})
            if existing_user:
                return  "/signup","False","Username already exists."

            # Insert new user into the database
            new_user = {
                "username": username,
                "password": password
            }
            users_collection.insert_one(new_user)
            # print("User in fo ----------------",new_user)
            # user1 = user.User(username,password)
            # user1.log_in()
            # print("User in fo ----------------",user1.get_user_info())
            return  "/",username,"Registration successful."
        else:
            if not username or not password:
                    return "/signin","False","Username and password are required."

            # Check if the user exists and the password matches
            user = users_collection.find_one({"username": username})
            if user and user["password"] == password:
                return "/",username,"Login successful."
            else:
                return "/signin","False","Invalid username or password."

# Define callback to handle login
# @app.callback(
#     [Output("url", "pathname"),Output('intermediate-value', 'data'),Output('login-status', 'children')],
#     Input("login-button", "n_clicks"),
#     State("login-username-input", "value"),
#     State("login-password-input", "value")
# )
# def login_user(n_clicks, username, password):
#     if n_clicks is None:
#         raise PreventUpdate

#     if not username or not password:
#         return "/signin","False","Username and password are required."

#     # Check if the user exists and the password matches
#     user = users_collection.find_one({"username": username})
#     if user and user["password"] == password:
#         return "/","True","Login successful."
#     else:
#         return "/signin","False","Invalid username or password."




@app.callback([Output(component_id='page_content', component_property='children'),Output('nav_home', 'children')],
              [Input(component_id='url', component_property='pathname'),Input("intermediate-value", "data"),Input("signout-value", "data")])
def load_content(pathname,logger,sign):
    print("logger",logger)
    print("sign",sign)
    val = []
    if not logger == 'False' and  logger is not None:
        if not sign == "False":
            val =  [
                # dbc.Button("Sign Out" ,id="signout" , className="mr-1", href='/signout'),
                html.Div(id='img-circle', children=[],style={'padding':'10px','background':'url(https://www.w3schools.com/howto/img_avatar.png) center / cover','width':'50px','height':'50px','border-radius':'50%','margin-right':'10px'}),
                # html.Img(src=app.get_asset_url('user.webp'),id='user', height='80px', style={'padding':'10px'},className="img-circle"),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(logger, header=True),
                        dbc.DropdownMenuItem("Profile", href="/profile",id="profile"),
                        dbc.DropdownMenuItem("Signout", href="/signout",id="signout"),
                    ],
                    nav=True,
                    in_navbar=True,
                    # label=html.Img(src=app.get_asset_url('user.jpg'),id='user', height='30px', style={'padding':'10px'},className="img-circle"),
                ),
                # dbc.Button("Sign In" ,id="signin" , className="mr-1", href='/signin'),
                # dbc.Button("Sign Up", color="primary", id="signup",className="mr-1", href='/signup'),
            ]
        else:
            val = [
                dbc.Button("Sign In" ,id="signin" , className="mr-1", href='/signin'),
                dbc.Button("Sign Up", color="primary", id="signup",className="mr-1", href='/signup'),
            ]
    else:
        val = [
            dbc.Button("Sign In" ,id="signin" , className="mr-1", href='/signin'),
            dbc.Button("Sign Up", color="primary", id="signup",className="mr-1", href='/signup'),
        ]
    if not logger == 'False' and not logger == None:
        if not sign == "False":
            if pathname == '/':
                return container,val
            elif pathname == '/Evaluate':
                return evaluate.outer_box,val
            elif pathname == '/signup':
                return register_new.reg,val
            elif pathname == '/signin':
                return register_new.log,val
            elif pathname == '/signout':
                return register_new.log,val
            elif pathname == '/app/danger_area':
                return None,val
            elif pathname == '/app/no_ball':
                return None,val
            elif pathname == '/app/arm_angle':
                return None,val
            elif pathname == '/app/leg_angle':
                return None,val
            elif pathname == '/profile':
                return profile.prof,val
            elif pathname == '/payment':
                return payment.payment,val
            else:
                return ["404 Error"],val
        else:
            if pathname == '/signup':
                return register_new.reg,val
            elif pathname == '/signin':
                return register_new.log,val
            else:
                return register_new.log,val
    else:
        if pathname == '/signup':
            return register_new.reg,val
        elif pathname == '/signin':
            return register_new.log,val
        else:
            return register_new.log,val

if __name__ == "__main__":
    app.run_server(debug=True)