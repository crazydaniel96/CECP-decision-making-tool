from logging import debug
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from pages import navbar,page1,page2,page3,settings,Papers_page,device_page,MedField_page,DevList_page
import pages    #for global variables
import functions.callbacks

app.layout = html.Div([dcc.Location(id="url"), navbar.sidebar, navbar.content])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"))
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page1.layout
    elif pathname == "/page-2":
        return page2.layout
    elif pathname == "/page-3":
        return page3.layout
    elif pathname == "/settings":
        return settings.layout
    elif "/DevSearch" in pathname:
        if pathname=="/DevSearch":
            return device_page.populateDevPage(pages.Search_Query)
        return device_page.populateDevPage(pages.Search_Query[pages.Search_Query['device_id']==int(pathname.split('=')[1])])
    elif pathname == "/MedField":
        return MedField_page.populateMedFieldPage()
    elif "/DevList" in pathname:
        if pathname == "/DevList":  #if coming from device type or manufacturer search
            return DevList_page.populateDevListPage()
        pages.Search_Query=pages.Search_Query[pages.Search_Query['device_type']==pathname.split('=')[1].replace("%20"," ")].reset_index(drop=True) 
        pages.titlePage=f"Devices of type {pathname.split('=')[1].replace('%20',' ')}"
        return DevList_page.populateDevListPage()   #if coming from device type selection on medical field page 
    elif "/Publications" in pathname:
        pages.dev_type_selected=pathname.split('=')[1].replace("%20"," ")
        return Papers_page.populatePapersPage()
        

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} does not exist"),
        ]
    )

if __name__ == "__main__":
    app.run_server()