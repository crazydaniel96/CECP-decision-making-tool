import dash_core_components as dcc
import plotly.express as px
import dash_html_components as html
import dash_bootstrap_components as dbc
import os
import pandas as pd

#import functions
from functions.Queries import *
#import global variables
import pages

#import general info of all dev_type papers

plotData=[]
Countries=pd.Series()
Done=pd.Series()
types=pd.Series()
Trend=pd.Series()
for file in os.listdir(pages.pathfileData+ 'papers/'):
    tmp=pd.read_csv(pages.pathfileData+ 'papers/'+file,low_memory=False)
    plotData.append([file[:-4],len(tmp)])       #name, df count -> papers types distribution
    Countries=Countries.add(ExtractData(tmp,"country",1),fill_value=0)       # ->  papers distribution over countries
    Done=Done.add(ExtractData(tmp,"checked",1),fill_value=0)              # ->  Done/Not done
    types=types.add(ExtractData(tmp,"type",1),fill_value=0)         # -> papers type distribution
    Trend=Trend.add(ExtractData(tmp,"date",1),fill_value=0)         # -> papers trend over years

Donefigure=px.bar(x=Done.index, y=Done,title='Done/Not done distribution',labels={"x":"","y":""}).update_layout(margin=dict(l=10, r=10, t=60, b=10),height=300)

layout=html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row(html.H4("Overview",className="m-2")),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                            figure=px.bar(x=[x[0] for x in plotData], y=[x[1] for x in plotData],title='Number of papers for each device type',labels={"x":"","y":""}).update_layout(margin=dict(l=10, r=10, t=60, b=10),height=300)
                        ),
                    ],
                        className="shadow p-3 m-3 bg-white rounded col-lg-4",
                    ),
                     dbc.Col([
                        dcc.Graph(
                            figure=px.pie(values=Countries, names=Countries.index, title='Country distribution').update_layout(margin=dict(l=10, r=10, t=60, b=10),height=300).update_traces(textposition='inside')
                        ),
                    ],
                        className="shadow p-3 m-3 bg-white rounded col-lg-4",
                    ),
                    dbc.Col([
                        dcc.Graph(
                            figure=Donefigure
                        ),
                    ],
                        className="shadow p-3 m-3 bg-white rounded col-lg-3",
                    ),
                ]),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(x=types.index, y=types,title='Papers types distribution',labels={"x":"","y":""},color=types.index).update_layout(margin=dict(l=10, r=10, t=60, b=10),height=300)
                )
            ],
                className="shadow p-3 m-3 bg-white rounded col-lg-11",
            ),
        ],
            justify="center",
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.area(x=Trend.index, y=Trend,labels={"x":"Year","y":"Publications"}).update_xaxes(
                        rangeslider_visible=True,
                        dtick="M12",
                        rangeselector=dict(
                            buttons=list([
                                dict(count=6, label="6 month", step="month", stepmode="backward"),
                                dict(count=1, label="1 year", step="year", stepmode="backward"),
                                dict(count=2, label="2 years", step="year", stepmode="backward"),
                                dict(step="all")
                            ])
                        )
                    ).update_layout(margin=dict(l=0, r=10, t=60, b=0),title_text='Publications trend over years', title_x=0.5,height=300)
                )
            ],
                className="shadow p-3 m-3 bg-white rounded col-lg-11"
            ),
        ],
            justify="center"    
        ),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H4("Specific Statistics")),
                    dbc.Col([
                        dcc.Dropdown(
                            id="DD23",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in pages.dev_type],
                            placeholder="Select device type",
                            clearable=False,
                        ),
                    ],
                        className="col-lg-4"
                    ),     
                ],
                    justify="between"    
                ),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="Done/NotDone")
                        ],
                            className="shadow p-3 m-3 bg-white rounded col-lg-3",
                        ),
                        dbc.Col([
                            dcc.Graph(id="CountryDistr")
                        ],
                            className="shadow p-3 m-3 bg-white rounded col-lg-5",
                        ),
                        dbc.Col([
                            dcc.Graph(id="TypeDistr")
                        ],
                            className="shadow p-3 m-3 bg-white rounded col-lg-3",
                        ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="TrendSpec")
                        ],
                            className="shadow p-3 m-3 bg-white rounded col-lg-11",
                        ),
                    ],
                        justify="center"
                    ),
                ],
                    id="PapersSpec_graphs",
                    style={"display":"none"}
                )
            ]),
        ],
            className="shadow p-3 m-1 bg-white rounded col-lg-12",
        ),
    ])