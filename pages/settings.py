import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout=html.Div([                 
    dbc.Row([
        dbc.Col([
          html.Br(),
          dbc.Row([
              dbc.Col([
                html.H5("Update Data"),
                html.Br(),
                dbc.Row(
                    dbc.Button(
                        "Update Publications",      #with our script, also classify study
                        outline=True,
                        color="dark",
                        id="Update_Papers",
                        className="m-3",
                    ),
                ),
                dbc.Row(
                    dbc.Button(
                        "Update Database",          #from icij, update also medical fields and device type
                        outline=True,
                        color="dark",
                        id="Update_Database",
                        className="m-3",
                    ),
                ),
              ],
                className="shadow p-3 m-2 bg-white rounded",
              ),
              dbc.Col([
                html.H5("Report an issue"),
                html.Br(),
                dbc.InputGroup(
                    [
                        dbc.Input(placeholder="Username"),
                        dbc.InputGroupAddon("@polimi.it", addon_type="append"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Select(
                            options=[
                                {"label": "System error", "value": 1},
                                {"label": "Data error", "value": 2},
                                {"label": "Functionalities", "value": 3},
                            ]
                        ),
                        dbc.InputGroupAddon("Type", addon_type="append"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("Message", addon_type="prepend"),
                        dbc.Textarea(bs_size="lg"),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    dbc.Button(
                        "Send report",         
                        outline=True,
                        color="dark",
                        id="Send",
                        className="m-3",
                    ),
                    justify="center"
                )
              ],
                className="shadow p-3 m-2 bg-white rounded",
              ),
          ]),
          html.Div(
            [
                #dcc.Interval(id="progress-interval", n_intervals=0, interval=1000),  #interval is in ms
                #dbc.Progress(id="progress"),
            ],
            className="shadow p-3 m-2 bg-white rounded",
          )
        ])
    ]) 
])