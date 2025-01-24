import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash
from dash import Output, Input, State

def make_sca(app):
    return dbc.Container([
        dbc.Label('Sca Settings')
    ],id='sca-div',style={'display':'none'})
    
def register_sca(app,fig):
    @app.callback(
        [Output('sca-div', 'style', allow_duplicate=True),
        Output('scatter-button', 'style', allow_duplicate=True)],
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
            if row['Type'] == 'scatter':
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
