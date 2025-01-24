import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash
from dash import Output, Input, State ,html, no_update
from comp.trace_comp.utils import query_trace as qt
import colorsys

def make_line(app):
    return dbc.Container([
        dbc.Select(id='select-trace-line',placeholder='Select Line ID'),
        dbc.Container([
            html.H4('Line', style={
                'backgroundColor': 'lightblue',
                'margin': '5px',
                'text-align': 'center',
                'border-radius': '10px'
            }),
            html.H4('Basic'),
            dbc.InputGroup([
                dbc.Input(id='line-basic-width', type='number'),
                dbc.Input(id='line-basic-opacity', type='number', min=0, max=1, value=0.5),
                dbc.Input(id='line-basic-color', type='color', value='#636efa', style={'height': '40px'})
            ], style={'border-radius': '10px'}),
            html.H4('Shaping'),
            dbc.InputGroup([
                dbc.Select(id='line-shap-dash',options=[
                    {'label':'Solid━━','value':'solid'},
                    {'label':'Dash--','value':'dash'},
                    {'label':'Dot⋯','value':'dot'},
                    {'label':'Dash+Dot-·-','value':'dashdot'},
                ],placeholder='Line Type'),
                dbc.Select(id='line-shap-shape',options=[
                    {'label':'Straight','value':'linear'},
                    {'label':'Curve','value':'spline'},
                    {'label':'VHV','value':'vhv'},
                    {'label':'HVH','value':'hvh'},
                ],placeholder='Line Shape'),
                dbc.Input(id='line-shap-smth',type='number',
                    min=0,max=1,step=0.005,placeholder='Smoothing')
            ], style={'border-radius': '10px'}),
            html.H4('Fill'),
            dbc.InputGroup([
                dbc.Select(id='line-fill-type',options=[
                    {'label':'None','value':'none'},
                    {'label':'Zero X','value':'tozerox'},
                    {'label':'Zero Y','value':'tozeroy'},
                    {'label':'Next','value':'tonext'},
                    {'label':'Next X','value':'tonextx'},
                    {'label':'Next Y','value':'tonexty'},
                    {'label':'Lead Self','value':'toself'},
                ],placeholder='Fill Style', value='none'),
                dbc.Input(id='line-fill-clr',type='color',
                placeholder='Fill Color', value='#ADD8E6', style={'height':'39px'})
            ])
        ]),
        dbc.Container([
            html.H4('Marker', style={
                'backgroundColor': 'lightblue',
                'margin': '5px',
                'text-align': 'center',
                'border-radius': '10px'
            }),
            html.H4('Basic'),
            dbc.InputGroup([
                dbc.Input(id='marker-size', type='number'),
                dbc.Input(id='marker-color', type='color', value='#636efa', style={'height': '40px'})
            ], style={'border-radius': '10px'})
        ]),
    ], id='line-div', style={'display': 'none', 'margin': '5px'})



def toggle_line(app,fig):
    @app.callback(
        [Output('line-div', 'style', allow_duplicate=True),
        Output('line-button', 'style', allow_duplicate=True)],
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
            if row['Type'] == 'line':
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
        [Output('line-basic-width','value'),
        Output('line-basic-opacity', 'value'),
        Output('line-basic-color', 'value'),
        Output('line-fill-type', 'value'),
        Output('line-fill-clr', 'value')],
        Input('select-trace-line','value'),
        State('figdata-area','value'),
    )
    def defaultly(name,data):
        data = json.loads(data)
        for n in data:
            if n['name'] == name:
                l = n.get('line',{})
                lw = l.get('width','')
                lo = l.get('opacity','')
                lc = l.get('color','')
                ft = n.get('fill','')
                fc = n.get('fillcolor','')
                return lw,lo,lc,ft,fc
            break
        return [no_update] * 5

def validate(value):
    return value if value is not None and len(str(value))>0 else None

def update_line(fig, name, **kwargs):
    if not isinstance(fig, go.Figure):
        fig = go.Figure(fig)
    fig.update_traces(**kwargs, selector=dict(name=name))
    return fig

def update_trace(app, fig):
    @app.callback(
        Output('figure-preview', 'figure',allow_duplicate=True),
        [
            Input('line-basic-width', 'value'),
            Input('line-basic-opacity', 'value'),
            Input('line-basic-color', 'value'),
            Input('line-shap-dash', 'value'),
            Input('line-shap-shape', 'value'),
            Input('line-shap-smth', 'value'),
            Input('line-fill-type', 'value'),
            Input('line-fill-clr', 'value'),
            Input('marker-size', 'value'),
            Input('marker-color', 'value')
        ],
        [State('select-trace-line', 'value'),
        State('figure-preview', 'figure')]
    )
    def update(lw, lo, lc, ld, ls, lt, ft, fc, ms, mc, name, fig):
        updated_fig = update_line(
            fig,
            name,
            line=dict(
            width=validate(lw),
            color=validate(lc),
            dash = validate(ld),
            shape = validate(ls),
            smoothing = validate(lt) if validate(ls)=='spline' else None),
            opacity=validate(lo),
            fill = validate(ft),
            fillcolor = validate(fc),
            marker=dict(
                size=ms,
                color=mc
            )
        )
        return updated_fig


def register_line(app,fig):
    toggle_line(app,fig)
    qt(app,'select-trace-line','line')
    set_defaults(app)
    update_trace(app,fig)