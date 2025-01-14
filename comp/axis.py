import dash
import dash_bootstrap_components as dbc
from dash import ctx, dcc, html
from dash import Input, Output, State, no_update
import plotly.graph_objects as go

def make_xaxis():
    return dbc.Form([
        dbc.Label('X Axis', style={'textAlign': 'center'}),
        dbc.Card([
            dbc.Input(id='x-label', value='X', placeholder='X Label')
        ])
    ])

def make_yaxis():
    return dbc.Form([
        dbc.Label('Y Axis', style={'textAlign': 'center'}),
        dbc.Input(id='y-label', placeholder='Y Label')
    ])

def make_axis(app,fig):
    return dbc.Container(
        [   
            dbc.Select(id='axes-select',options={'label':'','value':''},value=''),  # Default to 1st axis
            dbc.Row(dbc.Col(make_xaxis()), className="mb-3"),
            dbc.Row(dbc.Col(make_yaxis())),
        ], id='axis-div',
        style={'display': 'block'}
    )


def register_axis(app, fi):
    @app.callback(
        Output('figure-preview', 'figure', allow_duplicate=True),
        [Input('x-label', 'value')],
        [State('figure-preview', 'figure'),
         State('axes-select', 'value')]  # Get selected axis index
    )
    def update_xaxis(label, figure, selected_index):
        fig = go.Figure(figure)
        if label:
            layout = {
                f'xaxis{selected_index}': {'title': {'text': label}}
            }
            fig.update_layout(**layout)
            return fig
        return no_update
