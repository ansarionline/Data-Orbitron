import dash_bootstrap_components as dbc
from dash import Output, Input, State, no_update, html, dcc, ctx
import json
import dash_ace
def make_figdata(fig):
    return dbc.Container(id='figdata-div', children=[
        dbc.Button('Update Data', id='update-fig-data-btn', style={
            'margin': '10px',
            'backgroundColor': 'lightblue',
            'border-width': '2px',
            'border-radius': '10px',
            'width': '95%',
            'font-family': 'Arial',
            'font-weight': 'normal',
            'font-size': '15px',
            'text-align': 'center',
            'color': 'black'
        }, color='primary', className='mt-2'),
        dash_ace.DashAceEditor(
            id='figdata-area',
            theme='light',
            mode='json',
            fontSize=14,
            showGutter=True,
            showPrintMargin=False,
            highlightActiveLine=True,
            wrapEnabled=True,
            readOnly=False,
            style={
                "width": "100%",
                "height": "100%",
                "minHeight": "150px",
                "maxHeight": "100%",
                "overflow": "auto",
                "resize": "both", 
            }
        )
    ], 
    style={
        "resize": "both",
        "overflow": "auto",
        "minHeight": "200px",
        "maxHeight": "800px",
        "border": "1px solid #ddd",
        "padding": "10px"
    })

def register_figdata(app, fig):
    @app.callback(
        [
            Output('figure-preview', 'figure', allow_duplicate=True),
            Output('figdata-area', 'value', allow_duplicate=True),
        ],
        [
            Input('update-fig-data-btn', 'n_clicks'),
            Input('figure-preview', 'figure'),
        ],
        [State('figdata-area', 'value')],
        prevent_initial_call=True,
    )
    def update_figure_and_json(n_clicks, figure, data_json):
        triggered_id = ctx.triggered_id

        # Fetch data from the figure and display as JSON
        if figure and triggered_id == 'figure-preview':
            data = figure.get('data', [])
            try:
                formatted_data = json.dumps(data, indent=4)
                return figure, formatted_data
            except (TypeError, ValueError):
                # Handle unexpected issues during serialization
                return figure, json.dumps({"error": "Invalid figure data"}, indent=4)

        # Update the figure from JSON input
        if n_clicks is not None and triggered_id == 'update-fig-data-btn':
            try:
                new_data = json.loads(data_json)
                if isinstance(new_data, list):  # Ensure 'data' is a list
                    updated_fig = {
                        "data": new_data,
                        "layout": figure.get('layout', {}),  # Preserve the existing layout
                    }
                    return updated_fig, json.dumps(new_data, indent=4)
                else:
                    return no_update, json.dumps({"error": "Data must be a list"}, indent=4)
            except json.JSONDecodeError:
                return no_update, json.dumps({"error": "Invalid JSON format"}, indent=4)

        return no_update, no_update
