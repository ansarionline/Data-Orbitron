import dash
from dash import Output, Input, State, html, dcc
import dash_bootstrap_components as dbc
from dash_breakpoints import WindowBreakpoints
import plotly.subplots as ps
import plotly.graph_objects as go
from dash_resizable_panels import PanelGroup, Panel, PanelResizeHandle
from flask import session
import os
from comp import layout, panels, subplot, data, axis, figure, export, fig_data
from comp.trace_comp import line,bar,img,sca

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
                        [
                            PanelGroup([
                                Panel([
                                    dbc.Col([
                                        dbc.Container([
                                            layout.make_layout(fig)
                                        ])
                                    ])
                                ]),
                                PanelResizeHandle(
                        id='handler0a',
                        children=[html.Div(
                    style={'height': '100%', 'width': '5px','backgroundColor':'lightblue'})]
                    ),
                                Panel([
                                    dbc.Col([
                                        dbc.Container([
                                            fig_data.make_figdata(fig)
                                        ])
                                    ])
                                ])
                            ])
                        ],id='fig-json'
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
#panel functions registry
subplot.register_subplots(app, fig, go)
data.register_data(app,fig)
axis.register_axis(app,fig)
layout.register_layout(app,fig)
fig_data.register_figdata(app,fig)
figure.register_figure(app,fig)
export.register_export(app,fig)
#Trace sepecific
line.register_line(app,fig)
bar.register_bar(app,fig)
sca.register_sca(app,fig)
img.register_img(app,fig)
#panel toggle registry
panels.register_panel(app,'data-button','data-div')
panels.register_panel(app,'subplots-button','subplots-div')
panels.register_panel(app,'axis-button','axis-div')
panels.register_panel(app,'figure-button','figure-div')
panels.register_panel(app,'export-button','export-div')
#Trace specific
panels.register_panel(app,'line-button','line-div')
panels.register_panel(app,'bar-button','bar-div')
panels.register_panel(app,'image-button','img-div')
panels.register_panel(app,'scatter-button','sca-div')
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