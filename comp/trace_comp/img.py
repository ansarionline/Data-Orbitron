import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash
from dash import Output, Input, State

def make_img(app):
    return dbc.Container([
        dbc.Label('Image Settings')
    ],id='img-div',style={'display':'none'})
    
def register_img(app,fig):
    @app.callback(
        [Output('img-div', 'style', allow_duplicate=True),
        Output('image-button', 'style', allow_duplicate=True)],
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
            if row['Type'] == 'image':
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
