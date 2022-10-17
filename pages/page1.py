import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
#import functions
from functions.Queries import * 
#import global variables
import pages

#static plots
DevCountryPlot=ExtractData(pages.df,"country",1,unique="True") #number of devices per country
DevCountryPlot.name="devices"
X_dates,Y_dates=Merge_Dates(ExtractData(pages.df,"date",1))     #number of events per date -> trend

#table top of month
tmp1=ExtractData(ExtractData(pages.df,"date",4,keyWord="2018-10"),"medical_field",1)[0:5]  #extract occurrencies of each med_field in the selected date
tmp2=ExtractData(ExtractData(pages.df,"date",4,keyWord="2018-10"),"device_type",1)[0:5]  #extract occurrencies of each device_type in the selected date
rows=[]
for row in tmp1.index:   
    rows.append(html.Tr([html.Td(f"{row} ({tmp1[row]})")]))
table1=dbc.Table([html.Thead(html.Tr([html.Th("Medical Field")]))] + [html.Tbody(rows)], bordered=True,striped=True,style={"font-size" : "12px"})
rows=[]
for row in tmp2.index:   
    rows.append(html.Tr([html.Td(f"{row} ({tmp2[row]})")]))
table2=dbc.Table([html.Thead(html.Tr([html.Th("Device Type")]))] + [html.Tbody(rows)], bordered=True,striped=True,style={"font-size" : "12px"})

layout=html.Div([   
    dbc.Row([
        dbc.Col(
            [
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id="DD2",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in get_keys(countryFull(pages.df,"action_classification"))],
                            value='USA',
                            clearable=False,
                        ),
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="DD14",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in pages.years],
                            value='All-time',
                            clearable=False,
                        ),
                    ),
                ]),

                dcc.Graph(id='FreqActClass')
            ],
            className="shadow p-3 m-3 bg-white rounded col-lg-3",
        ),
        dbc.Col(
            [
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id="DD3",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in pages.df['type'].dropna().str.lower().unique()], 
                            value='recall',
                            optionHeight=55,
                            clearable=False,
                        ),
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="DD15",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in pages.years], 
                            value='All-time',
                            clearable=False,
                        ),
                    ),
                ]),
                
                dcc.Graph(id='RecallsPie')
            ],
            className="shadow p-3 m-3 bg-white rounded col-lg-3",
        ),
        dbc.Col([
            dbc.Row(html.H5("Top 5 current month"),justify="center"),
            dbc.Row([
                dbc.Col(table1),
                dbc.Col(table2),
            ]),
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-5"
        ),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="DD20",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.years],  
                        value='All-time',
                        clearable=False,
                    ),
                ),
                dbc.Col(html.H6("Event's type for each country\n(click to interact)"))
            ]),
            dcc.Graph(id="SunBurst"),
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-5",
        ),
        dbc.Col(
            [
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id="DD21",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in ['Class 1','Class 2',"Class 3"]],
                            value='Class 1',
                            clearable=False,
                        ),
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="DD22",
                            options=[{
                                'label': i,
                                'value': i
                            } for i in pages.years],
                            value='All-time',
                            clearable=False,
                        ),
                    ),
                ]),

                dcc.Graph(id='4grpahs')
            ],
            className="shadow p-3 m-3 bg-white rounded col-lg-6",
        ),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="WorldMap"),
            dcc.Checklist(id="WorldCheck",options=[{'label': 'Ratio', 'value': 'Ratio'}]),
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-5",
        ),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="DD1",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.countries_All],
                        value='all countries',
                        clearable=False,
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="DD16",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.years],
                        value='All-time',
                        clearable=False,
                    ),
                ),
            ]),

            dcc.Graph(id='Top5PieMan'),
            dcc.Checklist(id="Top5PieManCheck",options=[{'label': 'Ratio', 'value': 'Ratio'}]),
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-3"
        ),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="DD12",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.countries_All],
                        value='all countries',
                        clearable=False,
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="DD18",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.years],
                        value='All-time',
                        clearable=False,
                    ),
                ),
            ]),
            dcc.Graph(id='MedField_events'),
            dcc.Checklist(id="MedField_eventsCheck",options=[{'label': 'Ratio', 'value': 'Ratio'}]),
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-3"
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=px.choropleth(DevCountryPlot,locations=DevCountryPlot.index,color="devices",hover_name=get_keys(DevCountryPlot.index),range_color=[min(DevCountryPlot),max(DevCountryPlot)*2/3],color_continuous_scale=px.colors.sequential.Cividis_r).update_layout(height=300,title="Devices per country",title_x=0.5,margin=dict(l=0, r=0, t=40, b=0)),
            ),
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-5"
        ),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="DD11",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.countries_All],
                        value='all countries',
                        clearable=False,
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="DD17",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.years],
                        value='All-time',
                        clearable=False,
                    ),
                ),
            ]),
            dcc.Graph(id='Top5PieDev'),
            #dcc.Checklist(id="Top5PieDevCheck",options=[{'label': 'Ratio', 'value': 'Ratio'}]),
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-3"
        ),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="DD13",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.countries_All],
                        value='all countries',
                        clearable=False,
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="DD19",
                        options=[{
                            'label': i,
                            'value': i
                        } for i in pages.years],
                        value='All-time',
                        clearable=False,
                    ),
                ),
            ]),
            dcc.Graph(id='MedField_devices'),
            #dcc.Checklist(id="MedField_devicesCheck",options=[{'label': 'Ratio', 'value': 'Ratio'}]),
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-3"
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=px.area(x=X_dates, y=Y_dates,labels={"x":"Date","y":"Events"}).update_xaxes(
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
                ).update_layout(margin=dict(l=0, r=10, t=60, b=0),title_text='Events trend over years', title_x=0.5)
            )
        ],
            className="shadow p-3 m-3 bg-white rounded col-lg-11"
        ),
    ],
        justify="center"    
    ), 
])