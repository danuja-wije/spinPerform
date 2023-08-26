import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import uuid
external_stylesheets = [
    'assets/style.css'
]

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[external_stylesheets, dbc.themes.BOOTSTRAP],
                meta_tags=[{
                    'name': 'Spin perform',
                    'content': 'width=device-width,initial-scale=1.0'
                }]
                )

app.title = 'SpinPerform'
# app._favicon = app.get_asset_url('favicon.ico')

server = app.server