import base64
from dash import dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.io as pio
import dash
import io
import os
import plotly.graph_objects as go

# Supported export formats
formats = [
    fmt.upper() for fmt in ['png', 'jpg', 'jpeg', 
                            'webp', 'svg', 'pdf', 'eps', 
                            'json', 'pydict', 'py', 
                            'html', 'htm']
]

def make_export(fig):
    return html.Div(
        [
            dbc.Form(
                id='export-div',
                children=[
                    dbc.InputGroup([
                        dbc.Input(id='export-name', placeholder='Name', value='Figure'),
                        dbc.Select(
                            id='export-type',
                            options=[{'label': fmt, 'value': fmt} for fmt in formats],
                            placeholder="Select Export Format"
                        )
                    ]),
                    dbc.InputGroup([
                        dbc.Input(id='export-width', placeholder='Width',
                        value=1280,type='number',min=50),
                        dbc.Input(id='export-height', placeholder='Height',
                        value=720,type='number',min=50),
                        dbc.Input(id='export-scale', placeholder='Resolution',
                        value=1,type='number',min=1,step=1),
                    ]),
                    html.A(id='export-link', target='_blank',
                    download='True',style = {
                                    'margin': '10px',
                                    'backgroundColor': 'lightblue',
                                    'borderWidth': '2px',
                                    'borderRadius': '10px',
                                    'width': '95%',
                                    'fontFamily': 'Arial, sans-serif',
                                    'fontWeight': 'normal',
                                    'fontSize': '15px',
                                    'textAlign': 'center',
                                    'color': 'black',
                                    'display': 'inline-block',
                                    'padding': '10px',
                                    'textDecoration': 'none'
                                }),
                ],
                style={'margin': '5px', 'display': 'block'}
            )
        ]
    )
def register_export(app, fig):
    @app.callback(
        [Output("export-link", "download"),
        Output("export-link", "href"),
        Output("export-link", "children")],
        [Input("export-name", "value"),
        Input("export-type", "value"),
        Input("export-width", "value"),
        Input("export-height", "value"),
        Input("export-scale", "value")],
        State('figure-preview','figure'),
        prevent_initial_call=True
    )
    def export_figure(file_name, export_type, w, h, s, fig):
        if not export_type:
            return None, None, None
        export_type = export_type.lower()
        file_name = file_name or "figure"
        print(fig)
        fig = go.Figure(fig)
        try:
            if export_type in ["html", "htm"]:
                file_name = f"{file_name}.{export_type}"
                file_content = io.StringIO()
                pio.write_html(fig, file_content, include_plotlyjs='cdn', config={'displaylogo': False})
                file_content.seek(0)
                encoded_file = base64.b64encode(file_content.read().encode()).decode()
                href = f"data:text/html;base64,{encoded_file}"
            elif export_type == "json":
                file_name = f"{file_name}.json"
                file_content = fig.to_json()
                encoded_file = base64.b64encode(file_content.encode()).decode()
                href = f"data:application/json;base64,{encoded_file}"
            elif export_type in ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps']:
                img_bytes = fig.to_image(format=export_type,
                                        width=w,height=h,scale=s)
                encoded_file = base64.b64encode(img_bytes).decode()
                file_name = f"{file_name}.{export_type}"
                href = f"data:image/{export_type if export_type != 'jpg' else 'jpeg'};base64,{encoded_file}"
            elif export_type == "pydict":
                file_name = f"{file_name}.pydict"
                file_content = str(fig.to_plotly_json())
                encoded_file = base64.b64encode(file_content.encode()).decode()
                href = f"data:text/plain;base64,{encoded_file}"
            elif export_type == "py":
                file_name = f"{file_name}.py"
                file_content = (
                    f"import plotly.graph_objects as go\n"
                    f"fig = go.Figure({fig.to_plotly_json()})\n"
                    f"fig.show()"
                )
                encoded_file = base64.b64encode(file_content.encode()).decode()
                href = f"data:text/x-python;base64,{encoded_file}"
            return file_name, href, f"{file_name}.{export_type}"
        except Exception as e:
            error_message = f"Error exporting figure: {str(e)}"
            print(error_message)
            return None, None, None