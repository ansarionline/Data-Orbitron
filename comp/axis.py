import dash_bootstrap_components as dbc
from dash import html, Output,Input
fonts = ['Arial', 'Courier New', 'Times New Roman', 'Verdana', 'Georgia', 'Tahoma']

default = {
    'label': '',
    'font': 'Arial',
    'size': 20,
    'color': '#000000',
    'tickmode': 'auto',
    'ticks': 'outside',
    'linecolor': '#000000',
    'tickformat': ''
}

def make_axis(fig):
    return dbc.Form(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("X-Label"),
                            html.Div(id='x-label', children=[
                                dbc.Input(id='x-label-text', placeholder='Label Text',
                                          style={'margin': '5px'}, value=default['label']),
                                dbc.InputGroup([
                                    dbc.Select(id='x-label-font', options=[{'label': f, 'value': f} for f in fonts],
                                               value=default['font']),
                                    dbc.Input(id='x-label-size', type='number', placeholder='size',
                                              min=1, value=default['size']),
                                    dbc.Input(id='x-label-color', placeholder='Color', type='color',
                                              value=default['color'], style={'height': '40px'})
                                ], style={'margin': '5px'}),
                            ]),
                            html.H5("X-Ranges"),
                            html.Div(id='x-range', children=[
                                dbc.InputGroup([dbc.Input(id='x-range-min', type='number', placeholder='Min range',
                                                          value=0),
                                                dbc.Input(id='x-range-max', type='number', placeholder='Max range',
                                                          value=10),
                                                dbc.Input(id='x-range-step', type='number', placeholder='Steps',
                                                          min=1, value=1)], style={'margin': '5px'})
                            ]),
                            html.H5("X-Axis Ticks"),
                            html.Div(id='x-ticks', children=[
                                dbc.InputGroup([
                                    dbc.Select(id='x-tickmode', options=[
                                        {'label': 'Auto', 'value': 'auto'},
                                        {'label': 'Linear', 'value': 'linear'},
                                        {'label': 'Array', 'value': 'array'}
                                    ], value=default['tickmode']),
                                ], style={'margin': '5px'}),
                                dbc.InputGroup([
                                    dbc.Select(id='x-ticks-position', options=[
                                        {'label': 'Outside', 'value': 'outside'},
                                        {'label': 'Inside', 'value': 'inside'},
                                        {'label': 'None', 'value': ''}
                                    ], value=default['ticks']),
                                    dbc.Input(id='x-tickformat', placeholder='Tick label format',
                                    value=default['tickformat'])
                                ], style={'margin': '5px'}),
                            ]),
                            html.H5("X-Axis Line Color"),
                            html.Div(id='x-line', children=[
                                dbc.Input(id='x-line-color', type='color', value=default['linecolor'],
                                          style={'height': '40px'})
                            ]),
                        ]
                    ),
                ],
                className="mb-3"
            ),
        ], className="fullscreen-child", style={'margin': '5px'}
    )
def register_axis_callbacks(app, fig):
    @app.callback(
        Output('figure-preview', 'figure',
        allow_duplicate=True),
        [
            Input('x-label-text', 'value'),
            Input('x-label-font', 'value'),
            Input('x-label-color', 'value'),
            Input('x-label-size', 'value'),
            Input('x-range-min', 'value'),
            Input('x-range-max', 'value'),
            Input('x-range-step', 'value'),
            Input('x-tickmode', 'value'),
            Input('x-ticks-position', 'value'),
            Input('x-line-color', 'value'),
            Input('x-tickformat', 'value')
        ],
    allow_duplicate=True
    )
    def update_axis_label(label, font, color, size, r_min, r_max, r_step, tickmode,  ticks, linecolor, tickformat):
        fig.update_layout(
            xaxis=dict(
                title=label,
                title_font=dict(
                    size=size,
                    color=color,
                    family=font
                ),
                range=[r_min, r_max],
                dtick=r_step,
                tickmode=tickmode,
                ticks=ticks,
                linecolor=linecolor,
                tickformat=tickformat
            )
        )
        return fig