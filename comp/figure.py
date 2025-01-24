import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State, Dash
import plotly.graph_objects as go
import json

fonts = [
    "Arial",
    "Balto",
    "Courier New",
    "Droid Sans",
    "Droid Serif",
    "Droid Sans Mono",
    "Gravitas One",
    "Old Standard TT",
    "Open Sans",
    "Overpass",
    "PT Sans Narrow",
    "Raleway",
    "Roboto",
    "Times New Roman",
    "Verdana"
]
def make_fig(fig):
    figure_form = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5("Figure Settings"),
                dbc.InputGroup([
                    dbc.Input(
                        id='fig-title-text',
                        placeholder='Figure Title',
                        style={'margin': '5px'}
                    )
                ]),
                dbc.InputGroup([
                    dbc.Select(id='fig-title-font',placeholder='Font',value='White',
                                options = [{'label': l, 'value': l} for l in fonts]),
                    dbc.Input('fig-title-size',placeholder='Size',
                            type='number',min=5,step=1),
                    dbc.Input('fig-title-color',type='color')
                ],style={'margin': '5px'}),
                dbc.InputGroup([
                    dbc.Input('fig-title-x',placeholder='X',value=0.02,
                            type='number',min=0,step=0.05,max=1),
                    dbc.Input('fig-title-y',placeholder='Y',value=0.85,
                            type='number',min=0,step=0.05,max=1),
                ],style={'margin': '5px'})
                ,
                html.H5("Templates"),
                dbc.Select(
                    id='builtin-templates',
                    options=[
    {'label': 'None', 'value': 'none'},
    {'label': 'Simple', 'value': 'simple_white'},
    {'label': 'White', 'value': 'plotly_white'},
    {'label': 'Dark', 'value': 'plotly_dark'},
    {'label': 'Seaborn', 'value': 'seaborn'},
    {'label': 'GGPlot', 'value': 'ggplot2'},
    {'label': 'Presentation', 'value': 'presentation'}
                    ],
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
            Input('fig-title-text', 'value'),
            Input('fig-title-font', 'value'),
            Input('fig-title-size', 'value'),
            Input('fig-title-color', 'value'),
            Input('fig-title-x', 'value'),
            Input('fig-title-y', 'value'),
            Input('builtin-templates', 'value'),
        ],
        State('figure-preview', 'figure')
    )
    def update_figure(title, font, size, color, x, y,
                    template_name, fig):
        def validate_input(value):
            return value is not None and len(str(value)) > 0
        def return_input(value):
            return value if validate_input(value) else None
        fig = go.Figure(fig)
        layout_update = {}
        layout_update['template'] = return_input(template_name) or fig.layout.template
        layout_update['title'] = {
            'text': return_input(title) or fig.layout.title.text,
            'font': {
                'family': return_input(font) or (fig.layout.title.font.family if fig.layout.title else 'Arial'),
                'size': return_input(size) or (fig.layout.title.font.size if fig.layout.title else 24),
                'color': return_input(color) or (fig.layout.title.font.color if fig.layout.title else 'black')
            },
            'x': return_input(x) or fig.layout.title.x,
            'y': return_input(y) or fig.layout.title.y
        }
        layout_update = {key: value for key, value in layout_update.items() if value is not None}
        fig.update_layout(layout_update)
        return fig

