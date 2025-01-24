import dash_bootstrap_components as dbc
from dash import Output, Input, State

def query_trace(app, output, type_):
    @app.callback(
        Output(output, "options"),
        [Input('figure-preview', "figure")]
    )
    def toggle_panel(figure):
        if not figure or 'data' not in figure: 
            return [] 
        
        trace = []
        for t in figure['data']:
            if type_ == 'line':         
                if (t.get('type', '') == 'scatter' and t.get('mode') == 'lines+markers'):
                    trace.append({
                        "label": t.get('name', ''),
                        "value": t.get('name', '')
                    })
            elif type_ == 'scatter' or type_ == 'bubbles':
                if t.get('type', '') == 'scatter' and t.get('mode') == 'markers':
                    trace.append({
                        "label": t.get('name', ''),
                        "value": t.get('name', '')
                    })
            elif type_ == 'bar':
                if t.get('type', '') == 'bar':
                    trace.append({
                        "label": t.get('name', ''),
                        "value": t.get('name', '')
                    })
        return trace
