import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

#import functions
from functions.Queries import * #maybe not needed anymore
#import global variables
from pages import df
from pages import countries


layout=html.Div([
        
        dbc.Row([
            dbc.Col([
                html.H5("Find device"),
                dbc.Row(
                    [
                    dbc.Col([
                        dcc.Dropdown(
                            id="DD6-med_field",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in df["medical_field"].dropna().unique()],
                            clearable=False,
                            placeholder="Select medical field",
                        ),
                    ]), 
                    dbc.Col([
                        dcc.Dropdown(
                            id="DD7-manufacturer",
                            clearable=False,
                            placeholder="Select manufacturer",
                        ),
                    ]),
                    dbc.Col([
                        dcc.Dropdown(
                            id="DD8-device",
                            clearable=False,
                            placeholder="Select device",
                        ),
                    ]), 
                    dbc.Button(
                        "Search", 
                        outline=True,
                        color="dark",
                        disabled=True,
                        id="AdvanceDeviceButton",
                        className="mr-3 ml-3",
                        href="/DevSearch"
                    ),
                ]),
            ]),
        ],
            className="shadow p-3 bg-white rounded",
        ),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.H5("Find device type"),
                dbc.Row(
                    [
                    dbc.Col([
                        dcc.Dropdown(
                            id="DD9",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in df["medical_field"].dropna().unique()],
                            clearable=False,
                            placeholder="Select medical field",
                        ),
                    ]), 
                    dbc.Col([
                        dcc.Dropdown(
                            id="DD10",
                            clearable=False,
                            placeholder="Select device type",
                        ),
                    ]), 
                    dbc.Button(
                        "Search",
                        outline=True,
                        color="dark",
                        disabled=True,
                        id="AdvanceDevTypeButton",
                        className="mr-3 ml-3",
                        href="/DevList"
                    ),
                ]),
            ]),
        ],
            className="shadow p-3 bg-white rounded",
        ),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.H5("Find device's events number"),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id="DD4",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in countries],
                            clearable=False,
                            placeholder="Select country",
                        ),
                    ]),
                    dbc.Col([
                        dcc.Dropdown(
                            id="DD5",
                            clearable=False,
                            #optionHeight=50,
                            placeholder="Select device",
                        ),
                    ]),
                    dbc.Col([
                        dbc.Input(
                            id='textarea',
                            disabled=True,
                            plaintext=True,
                            placeholder="Number of events"), 
                    ]),     
                ])
            ])
        ],
            className="shadow p-3 bg-white rounded",
        ),


        html.P(id='placeholder')
])