import dash
from dash import Output, Input, State, html, dcc
import dash_bootstrap_components as dbc
import plotly.subplots as ps
import plotly.graph_objects as go
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
from flask import session
import os
from comp import layout, panels, subplot, data, axis, figure

# Create initial figure
fig = ps.make_subplots(rows=1, cols=1, start_cell='top-left')
app = dash.Dash('Data Orbitron',
                title='Data Orbitron',
                external_stylesheets=[dbc.themes.COSMO],
                suppress_callback_exceptions=True,
                prevent_initial_callbacks=True)

app.server.secret_key = os.urandom(24)
server = app.server

app.layout = html.Div([
    PanelGroup(
        id='panel-resizable',
        children=[
            dcc.Store(id='tab-session',data={'counter': 0},storage_type='session'),
                    Panel(
                        id='panel-left',
                        children=[
                            dbc.Col(
                                html.Div(
                                    [
                                        panels.make_panel(app, fig, 'assets/favicon.ico'),
                                        html.Div(id='panel-content', style={'margin-top': '20px'})
                                    ]
                                ),
                                style={'height': '100%', 'margin': '5px'},
                            )
                        ],
                    defaultSizePercentage = 30
                    ),
                    PanelResizeHandle(
                        id='handler',
                        children=html.Div(style={'height': '100%', 'width': '5px','backgroundColor':'#4682B4'})
                    ),
                    Panel(
                        id='panel-layout',
                        children=[
                            dbc.Col(
                                html.Div(
                                    [
                                        layout.make_layout(fig),
                                    ]
                                ),
                                style={'height': '100%', 'margin': '5px'},
                            )
                        ]
                    ),
                    PanelResizeHandle(
                        id='handler0',
                        children=html.Div(style={'height': '100%', 'width': '5px','backgroundColor':'lightblue'})
                    ),
                    Panel(
                        id='panel-right',
                        children=[
                            dbc.Col(
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='figure-preview',
                                            figure=fig,
                                            config={'displaylogo': False, 'editable': True},
                                            style={'height': '700px', 'padding': '10px'}
                                        )
                                    ]
                                ),
                                style={'padding': '20px'}
                            )
                        ],
                        defaultSizePercentage = 70
                    ),
                ],style={'margin': '0', 'width': '100%'},
        direction='horizontal')]
)
subplot.register_subplots(app, fig, go)
data.register_data(app,fig)
axis.register_axis(app,fig)
layout.register_layout(app,fig)
figure.register_figure(app,fig)
panels.register_panel(app,'data-button','data-div')
panels.register_panel(app,'subplots-button','subplots-div')
panels.register_panel(app,'axis-button','axis-div')
panels.register_panel(app,'figure-button','figure-div')

@app.callback(
    Output('tab-session', 'data'),
    Input('tab-session', 'data'),
    prevent_initial_call=True
)
def manage_session(data):
    data = data or {'counter': 0}
    data['counter'] += 1         
    return data                  

if __name__ == '__main__':
    app.run(debug=True)
