import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash
from dash import Output, Input, State, html, no_update
from comp.trace_comp.utils import query_trace as qt

def make_bar(fig):
    return dbc.Container([
        dbc.Select(id='select-trace-bar',placeholder='Select Bar ID'),
        html.H4("Bar", className="mt-4"),
        dbc.InputGroup([
            dbc.Input(id="bar-width", placeholder="Width", type="number", step=0.1),
            dbc.Input(id="bar-color", placeholder="Color", type="color", style={'height':'39px'}),
            dbc.Input(id="bar-opacity", placeholder="Opacity", type="number",
                    min=0, max = 1, step= 0.05,
                    style={'height':'39px'}),
        ], className="mb-3"),
        
        html.H4("Border", className="mt-4"),
        dbc.InputGroup([
            dbc.Input(id="bar-border-width", placeholder="Width", type="number", step=1, min=0),
            dbc.Input(id="bar-border-color", placeholder="Color", type="color", style={'height':'39px'}),
            dbc.Input(
                id="bar-border-rad",
                placeholder='Corner Radius',
                type='number', min=0,step=1
            ),
        ], className="mb-3")
    ],id='bar-div',style={'display':'box'})

def toggle_bar(app,fig):
    @app.callback(
        [Output('bar-div', 'style', allow_duplicate=True),
        Output('bar-button', 'style', allow_duplicate=True)],
        Input('trace-table', 'data')
    )
    def toggle(table):
        style = {'display': 'none'}
        btn_style = {
    'margin':'10px',
    'backgroundColor':'#1a73e8',
    'border-wdith':'2px',
    'border-radius':'10px 10px 0px 0px',
    'width':'95%',
    'font-family':'Arial',
    'font-weight':'bold',
    'font-size':'15px',
    'text-align':'center',
    'color':'white',
    'display':'none'
}
        for row in table:
            if row['Type'] == 'bar':
                style = {'display': 'block'}
                btn_style = {
    'margin':'10px',
    'backgroundColor':'#1a73e8',
    'border-wdith':'2px',
    'border-radius':'10px 10px 0px 0px',
    'width':'95%',
    'font-family':'Arial',
    'font-weight':'bold',
    'font-size':'15px',
    'text-align':'center',
    'color':'white',
    'display':'block'
}
                break
        return style,btn_style

import json
def set_defaults(app):
    @app.callback(
        [Output('bar-width','value'),
        Output('bar-color', 'value'),
        Output('bar-border-width', 'value'),
        Output('bar-border-color', 'value'),
        Output('bar-border-rad', 'value')],
        Input('select-trace-bar','value'),
        State('figdata-area','value'),
    )
    def defaultly(name, data):
        data = json.loads(data)
        
        for n in data:
            if n.get('name') == name:
                b = n.get('marker', {})
                bw = b.get('width', '') 
                bc = b.get('color', '') 
                bd = b.get('line', {})  
                bdw = bd.get('width', '') 
                bdc = bd.get('color', '') 
                bds = bd.get('shape', '')  
                return bw, bc, bdw, bdc, bds
            break
        return [no_update] * 5

def validate(value):
    return value if value is not None and len(str(value))>0 else None

def update_bar(fig, name, **kwargs):
    if not isinstance(fig, go.Figure):
        fig = go.Figure(fig)
    fig.update_traces(**kwargs, selector=dict(name=name))
    return fig

def update_trace(app, fig):
    @app.callback(
        Output('figure-preview', 'figure',allow_duplicate=True),
        [
            Input('bar-width','value'),
            Input('bar-color', 'value'),
            Input('bar-opacity', 'value'),
            Input('bar-border-width', 'value'),
            Input('bar-border-color', 'value'),
            Input('bar-border-rad', 'value')
        ],
        [State('select-trace-bar', 'value'),
        State('figure-preview', 'figure')]
    )
    def update(bw, bc, bo, bdw, bdc, bdr, name, fig):
        fig =  update_bar(
            fig,
            name,
            width=validate(bw),
            marker=dict(
                color = validate(bc),
                opacity = validate(bo),
                line = dict(
                    width = validate(bdw),
                    color = validate(bdc),
                ),
            cornerradius = validate(bdr),
            )
        )
        return fig

def register_bar(app,fig):
    toggle_bar(app,fig)
    qt(app,'select-trace-bar','bar')
    set_defaults(app)
    update_trace(app,fig)
