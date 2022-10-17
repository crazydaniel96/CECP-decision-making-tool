import dash_bootstrap_components as dbc
import dash_core_components as dcc
#from dash_core_components.Link import Link
import dash_html_components as html

top_header = dbc.Row(           #goes into sidebar object 
    [
        dbc.Col(html.H2("Dashboard", className="display-4")),
        dbc.Col(            #show Menu
            [
                html.Button(
                    html.I(className="fa fa-bars fa-2x"),
                    className="navbar-toggler",
                    id="navbar-toggle",
                ),
                html.Button(
                    html.I(className="fa fa-bars fa-2x"),
                    className="navbar-toggler",
                    id="sidebar-toggle",
                ),
            ],
            width="auto",
            align="center",         
        ),
        dbc.Col([               #config 
            dbc.NavLink(
                html.Button(
                    html.I(className="fa fa-cog fa-2x"),
                    className="navbar-toggler",
                ),
                href="/settings",
                style={"padding":"0"},
                id="sidebar-settings",
            )],
            id="settings",
            width="auto",
            align="center", 
        ),
    ],
    style={"flex-direction": "row"},
)

sidebar_search= dbc.Row(                #search
    [      
        html.Button(
            html.I(className="fa fa-search fa-2x"),
            className="navbar-toggler ml-auto",
            id="popover-target",
        ),
        dbc.Popover(
            [
                dbc.PopoverHeader("Search engine (Beta)"),
                dbc.PopoverBody(
                    dcc.Dropdown(
                        id='inputSearch2',
                        value='',
                        placeholder="Search here",
                    ),
                ),
            ],
            id="popover",
            is_open=False,
            target="popover-target",
        ),
    ],
    id="searchIcon",
    style={"flex-direction": "row"},
)

sidebar_header=html.Div([
    top_header,
    html.Br(),
    sidebar_search
])

sidebar = html.Div(
    [
        sidebar_header,
        dbc.Col(
            [
            dcc.Dropdown(
                id='inputSearch1',
                value='',
                placeholder="Search here",
            )],
            style={"padding":"0"},
        ),
        dbc.Collapse(           #Collapse component to animate hiding / revealing links
            dbc.Nav(
                [
                    dbc.NavLink("General overview", href="/page-1", id="page-1-link"),
                    dbc.NavLink("Publications stats", href="/page-3", id="page-3-link"),
                    dbc.NavLink("Advanced search", href="/page-2", id="page-2-link"),
                    dbc.NavLink("settings",href="/settings",id="navbar-settings"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
        html.Div(
            [
                html.Hr(),
                html.P(
                    ["Croci Francesco",html.Br(),"d'Arenzo Daniele",html.Br(),"Fumagalli Alberto",html.Br(),"Gambaro Enrico",html.Br(),"Neri Francesco",html.Br(),"Samandari Ahmad"],
                    className="lead",
                    style={"font-size":"small"},
                ),
            ],
            id="blurb",
        ),
    ],
    id="sidebar",
    className='collapsed'
)

content = html.Div(id="page-content")           #variable page content