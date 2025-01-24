import dash_bootstrap_components as dbc
from dash import Output,Input,html,State
from comp import axis, figure, subplot, data, export
from comp.trace_comp import line, bar, sca, img
options=[     
    {'label': 'Subplots', 'value': 'subplots'},
    {'label': 'Axis', 'value': 'axis'},
    {'label': 'Figure', 'value': 'figure'},
    {'label': 'Settings', 'value': 'settings'}
]
img_=img

def add_headings(text='Heading',style={
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
}):
    return dbc.Button(f'{text.title()}',id=f'{text.lower()}-button',style=style)

def register_panel(app, button_id, target_id):
    @app.callback(
        [Output(target_id, "style"), Output(button_id, "style")],
        [Input(button_id, "n_clicks")],
        [State(target_id, "style")],
    )
    def toggle_panel(n_clicks, current_style):
        # Default styles
        container_hidden = {"display": "none"}
        container_visible = {"display": "block"}
        
        button_hidden_style = {
    'margin':'10px',
    'backgroundColor':'darkblue',
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
        button_visible_style = {
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
        if n_clicks and current_style["display"] == "none":
            return container_visible, button_visible_style 
        return container_hidden, button_hidden_style


def make_panel(app,fig,img):
    return dbc.Col([
        dbc.InputGroup([
            html.Img(src=img,
            style={'width':'50px','height':'50px'}),
            dbc.Label('Data Orbitron',style={'font-family':'Arial',
                                            'font-weight':'bold',
                                            'font-size':'35px',
                                            'margin-left':'10px'}
                    )
        ]),
        add_headings('Data'),
        data.make_data(app,fig),
        add_headings('Subplots'),
        subplot.make_subplots_panel(app, fig),
        add_headings('Axis'),
        axis.make_axis(app, fig),
        add_headings('Figure'),
        figure.make_fig(fig),
        add_headings('Line'),
        line.make_line(app),
        add_headings('Bar'),
        bar.make_bar(app),
        add_headings('Scatter'),
        sca.make_sca(app),
        add_headings('Image'),
        img_.make_img(app),
        add_headings('Export'),
        export.make_export(fig),
        ],style={
                    "height": "98vh",
                    "overflowY": "scroll",
                    'overflowX': 'hidden',
                    'margin':'5px'
                },
        )