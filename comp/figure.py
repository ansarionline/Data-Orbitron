import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State, Dash
import plotly.graph_objects as go
import json

def make_fig(fig):
    figure_form = dbc.Form([
        dbc.Row([
            dbc.Col([
                html.H5("Figure Settings"),
                dbc.InputGroup([
                    dbc.Input(
                        id='figure-title',
                        placeholder='Figure Title',
                        style={'margin': '5px'}
                    )
                ]),
                dbc.InputGroup([
                    dbc.Input(
                        id='figure-width',
                        type='number',
                        placeholder='Width',
                        min=100,
                        value=800,
                        style={'margin': '5px'}
                    ),
                    dbc.Input(
                        id='figure-height',
                        type='number',
                        placeholder='Height',
                        min=100,
                        value=600,
                        style={'margin': '5px'}
                    )
                ]),
                html.H5("Templates"),
                dbc.Select(
                    id='builtin-templates',
                    options=[
                        {'label': 'Default', 'value': 'none'},
                        {'label': 'Simple', 'value': 'plotly_white'},
                        {'label': 'Dark', 'value': 'plotly_dark'},
                        {'label': 'Seaborn', 'value': 'seaborn'},
                        {'label': 'GGPlot', 'value': 'ggplot2'}
                    ],
                    value='default',
                    style={'margin': '5px'}
                )
            ])
        ])
    ], id='figure-div', style={'display': 'block'})
    return figure_form

def register_figure(app, fig):
    @app.callback(
        Output('figure-preview', 'figure', allow_duplicate=True),
        [
            Input('figure-title', 'value'),
            Input('figure-width', 'value'),
            Input('figure-height', 'value'),
            Input('builtin-templates', 'value'),
        ],
        State('figure-preview', 'figure')
    )
    def update_figure(title, width, height, template_name, fig):
        fig = go.Figure(fig)

        fig.update_layout(title=title, width=width, height=height)

        fig.update_layout(template=template_name)

        # if upload_content:
        #     try:
        #         import base64
        #         content_type, content_string = upload_content.split(',')
        #         template_json = json.loads(base64.b64decode(content_string).decode('utf-8'))
        #         fig.update_layout(**template_json)
        #     except Exception as e:
        #         print(f"Error applying uploaded template: {e}")

        return fig
