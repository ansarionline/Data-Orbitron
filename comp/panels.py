import dash_bootstrap_components as dbc
from dash import Output,Input,html
from comp import axis, figure, settings, subplot
options=[     
{'label': 'Subplots', 'value': 'subplots'},
{'label': 'Axis', 'value': 'axis'},
{'label': 'Figure', 'value': 'figure'},
{'label': 'Settings', 'value': 'settings'}
]
def make_panel(fig):
    return dbc.Row([
        dbc.Col([
            dbc.InputGroup([html.Img(src='assets/favicon.ico',
                style={"width": "50px", "height": "50px"}),
                dbc.Select(
                id='panel-select',
                options=options,
                value='subplots',  
                name="Editing Mode"
            )]),
        ])
    ])
    
def register_panels_callbacks(app,fig,update_session,go):
    axis.register_axis_callbacks(app,fig)
    subplot.register_subplots(app,fig,go)
    @app.callback(
    Output('panel-content', 'children',allow_duplicate=True),
    Input('panel-select', 'value')
    )
    def update_panel_content(selected_value):
        update_session()
        if selected_value == 'axis':
            return axis.make_axis(fig)
        elif selected_value == 'figure':
            return figure.make_fig(fig)
        elif selected_value == 'settings':
            return settings.make_settings(fig)
        elif selected_value == 'subplots':
            return subplot.make_subplots_panel(fig)
        return html.Div("Select an option from the dropdown")