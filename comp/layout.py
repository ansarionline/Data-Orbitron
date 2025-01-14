import dash_bootstrap_components as dbc
from dash import Output, Input, State, no_update, html, dcc, ctx
import json
import dash_ace

def make_layout(fig):
    return html.Div(id='layout-div', children=[
        dbc.Button('Update Layout', id='update-btn',style={'width':'100%',
                                                        'margin':'5px',
                                                        'bordre-radius':'20px'},
        color='primary', className='mt-2'),
        dash_ace.DashAceEditor(
            id='layout-area',
            theme='light',
            mode='json', 
            fontSize=14,
            showGutter=False,
            showPrintMargin=True,
            highlightActiveLine=True,
            wrapEnabled=False,
            readOnly=False,  # Allow editing
            width='100%',
            height='500px'
        ),
    ], style={'margin': '5px', 'display': 'block'})

def register_layout(app, fig):
    @app.callback(
        [Output('figure-preview', 'figure', allow_duplicate=True),
         Output('layout-area', 'value', allow_duplicate=True)],
        [Input('update-btn', 'n_clicks'),
         Input('figure-preview', 'figure')],
        [State('layout-area', 'value')],
        prevent_initial_call=True  # Prevent initial callback on app start
    )
    def update_figure_and_json(n_clicks, figure, layout_json):
        triggered_id = ctx.triggered_id
        
        # Case when figure changes (e.g., from other callbacks or user interactions)
        if figure and triggered_id == 'figure-preview':
            layout = figure.get('layout', {})
            return figure, json.dumps(layout, indent=4)
        
        # Case when the button is clicked
        if n_clicks is not None and triggered_id == 'update-btn':
            try:
                # Apply changes from the JSON editor to the figure
                new_layout = json.loads(layout_json)

                # Ensure the new layout is a valid dictionary
                if isinstance(new_layout, dict):
                    # Update the figure with the new layout
                    updated_fig = {
                        "data": figure['data'],  # Keep the existing data, only change layout
                        "layout": new_layout
                    }

                    # Return the updated figure and the updated JSON layout for the editor
                    return updated_fig, json.dumps(new_layout, indent=4)
                else:
                    return no_update, no_update
            except json.JSONDecodeError:
                return no_update, no_update
        return no_update, no_update
