from dash import Dash, html, dash_table as dt, Output, Input, State, dcc
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

traces = {'Line': 'line', 'Bar': 'bar'}
data = [
    {"Trace": "Default", "Type": 'Line', 'Row': 1, 'Col': 1},
]
def make_subplots_panel(fig, data=data):
    return dbc.Form([
        dbc.Col([
            html.Div(id='Traces', children=[
                dbc.Label(html.H5('Traces')),
                dbc.InputGroup([
                    dbc.Select(options=[{'label': k, 'value': v} for k, v in traces.items()],
                            id='trace-type', value='line'),
                    dbc.Input(id='row-num',placeholder='Row',type='number',
                            min=1,step=1),
                    dbc.Input(id='col-num',placeholder='Row',type='number',
                            min=1,step=1),
                    dbc.Input(id='trace-name', placeholder='Trace', value='Default'), 
                    dbc.Button('➕', id='add-trace-button', style={'backgroundColor': 'lightgreen',
                                                                'border-width': '2px'}, n_clicks=0)
                ]),
                html.Div([
                    dt.DataTable(id='trace-table',
                                data=data, editable=False, 
                                row_deletable=True,
                                style_cell={
                                    "textAlign": "center",
                                    "padding": "5px",
                                    "fontFamily": "Arial, sans-serif",
                                    "fontSize": "12px",
                                    "fontWeight": "normal",
                                    "color": "black",
                                }, style_header={
                        "backgroundColor": "lightgreen",
                        "fontWeight": "bold",
                        "textAlign": "center",
                        "fontSize": "12px",
                        "color": "darkgreen",
                    })], style={
                    "height": "200px",
                    "overflowY": "scroll",
                    "margin": "5px"
                })
            ])
        ], style={'margin': '5px'})
    ])
def add_figure(go, fig, name, type_, row, col):
    if type_ == 'line':
        fig.add_trace(go.Scatter(x=[0, 1, 2, 3], y=[0, 1, 2, 3], 
            mode='lines', name=name),row=row,col=col)
    elif type_ == 'bar':
        fig.add_trace(go.Bar(x=[0, 1, 2, 3], y=[0, 1, 2, 3],
            name=name),row=row,col=col)
    return fig
def register_subplots(app, fig, go):
    @app.callback(
        [Output('figure-preview', 'figure'),
         Output('trace-table', 'data')],  # Output message box
        [Input('add-trace-button', 'n_clicks'),
         Input('trace-table', 'data'),
         Input('row-num','value'),
         Input('col-num','value')],
        [State('trace-name', 'value'),
         State('trace-type', 'value'),
         State('trace-table', 'data_previous')]
    )
    def update_subplots(n_clicks, current_data, row_, col
                    , name, type_, previous_data):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == 'add-trace-button' and n_clicks > 0:
            for i in current_data:
                if i['Trace'] == name:
                    return fig, current_data
            add_figure(go, fig, name, type_, row_, col)
            new_row = {"Trace": name, "Type": type_, "Row": 1, "Col": 1}
            current_data.append(new_row)
            return fig, current_data 
        elif triggered_id == 'trace-table' and previous_data is not None:
            deleted_rows = [row for row in previous_data if row not in current_data]
            for row in deleted_rows:
                trace_name = row['Trace']
                fig.data = [trace for trace in fig.data if trace.name != trace_name]
            return fig, current_data 
        return fig, current_data
