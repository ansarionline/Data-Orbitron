from dash import dcc, html, Input, Output, State, dash_table, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
import plotly.graph_objects as go

def make_data(app, fig):
    return dbc.Container(id='data-div',children=[
        dbc.Row([
            dcc.Store('df-df',data=[]),
            dbc.Col([
                dcc.Upload(
                    id='upload-data',
                    children=dbc.Alert(
                        [
                            html.A("Select Files", className="text-primary")
                        ],
                        color="info",
                        style={"textAlign": "center", "cursor": "pointer"}
                    ),
                    style={"width": "100%", "marginBottom": "10px"},
                    multiple=False
                )
            ], width=12),
        ], style={'display':'block'}, id='dt-r'),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='df-table',
                    style_table={'height': '180px', 'overflowY': 'auto'},
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
                    },
                    editable=True,
                    row_deletable=False
                    )
            ], width=12)
        ])
    ], style={"margin": "5px",'display':'block'})
def register_data(app, fig=None):
    @app.callback(
        Output('df-table', 'data'),
        Output('df-table', 'columns'),
        Output('x-col-select', 'options'),
        Output('y-col-select', 'options'),
        Output('figure-preview', 'figure', allow_duplicate=True),
        Output('df-df', 'data', allow_duplicate=True),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('figure-preview', 'figure'),
    )
    def update_data(contents, filename, figure):
        data, columns, col_options, fig = [], [], [], figure or {"data": []}
        df_json = None

        if contents is not None:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)

            try:
                if 'csv' in filename:
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                elif 'xls' in filename:
                    df = pd.read_excel(io.BytesIO(decoded))
                else:
                    raise ValueError("Unsupported file type")
                data = df.to_dict('records')
                columns = [{"name": col, "id": col} for col in df.columns]
                col_options = [{"label": col, "value": col} for col in df.columns]
                df_json = df.to_json(orient='split')
            except Exception as e:
                print(f"Error processing uploaded file: {e}")

        return data, columns, col_options, col_options, fig, df_json