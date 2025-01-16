from dash import Dash, html, dash_table as dt, Output, Input, State, dcc
import dash
import dash_bootstrap_components as dbc
import plotly.subplots as ps
import plotly.graph_objects as go
from itertools import product
import pandas as pd
from io import StringIO

traces = {'Line': 'line', 'Bar': 'bar', 'Empty': 'empty'}
data = []
def make_subplots_panel(app, fig, data=data):
    # Extract current subplot configuration
    grid_ref = getattr(fig, '_grid_ref', None)
    current_rows = len(grid_ref) if grid_ref else 1
    current_cols = len(grid_ref[0]) if grid_ref and grid_ref else 1

    subplots_form = dbc.Container(id='subplots-div',children=[
        dbc.Col([
            html.Div([
                dbc.Label(html.H5('Subplots')),
                dbc.InputGroup([
                    dbc.Input(id='row-total', type='number', min=1, step=1,
                            value=current_rows, placeholder='Rows'),
                    dbc.Input(id='col-total', type='number', min=1, step=1,
                            value=current_cols, placeholder='Columns')
                ]),
                dbc.InputGroup([
                    dbc.Input(id='ver-spac', placeholder='Vertical Spacing',
                            min=0.1, max=1, step=0.05, type='number', value=0.1),
                    dbc.Input(id='horizon-spac', placeholder='Horizontal Spacing',
                            min=0.1, max=1, step=0.05, type='number', value=0.1)
                ])
            ]),
            html.Div(id='Traces', children=[
                dbc.Label(html.H5('Traces')),
                dbc.InputGroup([
                    dbc.Select(options=[{'label': k, 'value': v} for k, v in traces.items()],
                            id='trace-type', value='line'),
                    dbc.Input(id='row-num', placeholder='Row',
                            type='number', min=1, step=1),
                    dbc.Input(id='col-num', placeholder='Col',
                            type='number', min=1, step=1),
                    dbc.Input(id='trace-name', placeholder='ID', value='1x1')
                ]),
                dbc.InputGroup([
                dbc.Select(id='x-col-select',placeholder='X data'),
                dbc.Select(id='y-col-select',placeholder='Y Data'),
                dbc.Button('➕', id='add-trace-button',
                        style={'backgroundColor': '#1a73e8',
                                'border-width': '2px'}, n_clicks=0)]
                ),
                html.Div([
                    dt.DataTable(
                        id='trace-table',
                        data=data,
                        columns=[
                            {'name': 'Index', 'id': 'Index'},
                            {'name': 'ID', 'id': 'ID'},
                            {'name': 'Type', 'id': 'Type'},
                            {'name': 'Row', 'id': 'Row'},
                            {'name': 'Col', 'id': 'Col'},
                            {'name': 'XData', 'id': 'XData'},
                            {'name': 'YData', 'id': 'YData'}
                        ],
                        editable=False,
                        row_deletable=True,
                        style_cell={
                        "textAlign": "center",
                        "padding": "5px",
                        "fontFamily": "Arial, sans-serif",
                        "fontSize": "12px",
                        "fontWeight": "normal",
                        "color": "black",
                    },
                        style_header={
                        "backgroundColor": "lightblue",
                        "fontWeight": "normal",
                        "textAlign": "center",
                        "fontSize": "12px",
                        "color": "black",
                    }
                    )
                ], style={
                    "height": "200px",
                    "overflowY": "scroll",
                    "margin": "5px"
                })
            ])
        ])
    ],style={'display':'block','margin':'5px'})
    return subplots_form

def add_figure(go, fig, name, type_, rows, cols, x=[1,2], y=[1,2], index=1):
    if isinstance(rows, str):
        rows = eval(rows)
    if isinstance(cols, str):
        cols = eval(cols)
    
    if not isinstance(rows, (list, tuple)):
        rows = [rows]
    if not isinstance(cols, (list, tuple)):
        cols = [cols]
        
    if type_ == 'line':
        trace = go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name=name
        )
    elif type_ == 'bar':
        trace = go.Bar(
            x=x,
            y=y,
            name=name
        )
    else:
        return fig
    fig.add_trace(trace, row=rows[0], col=cols[0])
    return fig
def add_new_row(data, name, type_, row_num, col_num, x, y):
    # Check if the current row_num and col_num already exist in the data
    if not any(row['Row'] == str(row_num) and row['Col'] == str(col_num) for row in data):
        # If not, increment the index
        highest_index = max(int(row['Index']) for row in data) if data else 0
        new_index = str(highest_index + 1)
    else:
        # Otherwise, use the current highest index (no increment)
        new_index = str(max(int(row['Index']) for row in data) if data else 0)
    
    # Add the new row
    new_row = {
        "Index": new_index,
        "ID": str(name),
        "Type": str(type_),
        "Row": str(row_num),
        "Col": str(col_num),
        "XData": str(x),
        "YData": str(y)
    }
    
    if not any(trace['ID'] == name for trace in data):
        data.append(new_row)
    return new_index


from plotly.subplots import make_subplots
def register_subplots(app, fig, go):
    @app.callback(
        [Output('figure-preview', 'figure'),
        Output('trace-table', 'data'),
        Output('axes-select', 'options')],
        [Input('add-trace-button', 'n_clicks'),
        Input('row-total', 'value'),
        Input('col-total', 'value'),
        Input('ver-spac', 'value'),
        Input('horizon-spac', 'value'),
        Input('trace-table', 'data'),
        Input('x-col-select', 'value'),
        Input('y-col-select', 'value')],
        [State('trace-name', 'value'),
        State('trace-type', 'value'),
        State('row-num', 'value'),
        State('col-num', 'value'),
        State('trace-table', 'data_previous'),
        State('df-df', 'data'),
        State('layout-area','value')],
        prevent_initial_call=True
    )
    def update_subplots(n_clicks, rows, cols, v_space, h_space,
                        current_data,x,y ,name, type_, row_num, col_num, previous_data,
                        df_df,layout):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        rows = rows or 1
        cols = cols or 1
        v_space = v_space or 0.1
        h_space = h_space or 0.1
        current_data = current_data or []
        new_fig = make_subplots(
            rows=rows,
            cols=cols,
            vertical_spacing=v_space,
            horizontal_spacing=h_space,
            start_cell='top-left'
        )
        
        if df_df is not None:
            df = pd.read_json(StringIO(df_df),orient='split') if not df_df is None else pd.DataFrame()
        if (triggered_id == 'add-trace-button' and n_clicks and row_num
        and col_num and name and x and y):
            if row_num <= rows and col_num <= cols:
                new_row = add_new_row(current_data,name,type_,row_num,col_num,x,y)
        elif triggered_id == 'trace-table' and previous_data:
            current_data = [row for row in previous_data if row in current_data]
        for trace in current_data:
            new_fig = add_figure(go, new_fig, trace['ID'], trace['Type'],
                                trace['Row'], trace['Col'],
                                x = df[trace['XData']] if not df.empty else [1],
                                y = df[trace['YData']] if not df.empty else [1],
                                index=trace['Index'])
        return (new_fig, current_data, [ti["Index"] for ti in current_data])