import dash
from dash import Output, Input, html, dcc
import dash_bootstrap_components as dbc
from plotly.graph_objects import Figure
import plotly.graph_objects as go
import plotly.subplots as ps
from flask import session
import os
from comp import panels
fig = ps.make_subplots(1,1)
app = dash.Dash('Data Orbitron',title='Data Orbitron',
            external_stylesheets=[dbc.themes.COSMO],
            suppress_callback_exceptions=True,
            prevent_initial_callbacks=True)

app.server.secret_key = os.urandom(24)
server = app.server
def update_session():
    if 'count' not in session:
        session['count'] = 0  
    session['count'] += 1  

app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                panels.make_panel(None),
                html.Div(id='panel-content', style={'margin-top': '20px'})
            ]),
            style={'height': '100vh', 'padding': '10px'},
            width=3
        ),
        dbc.Col(
            html.Div([
                html.Div("Right Section", id='toolbar'),
                dcc.Graph(
                    id='figure-preview',
                    figure=fig,
                    config={'displaylogo': False, 'editable': True},
                    style={'height': '80vh', 'padding': '10px'}
                )
            ]),
            style={ 'padding': '20px'},
            width=9
        ),
    ], style={'margin': '0', 'width': '100%'})
])
panels.register_panels_callbacks(app,fig,update_session,go)
if __name__ == '__main__':
    app.run(debug=True)