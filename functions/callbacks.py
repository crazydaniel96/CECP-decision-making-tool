from app import app
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash_extensions.snippets import send_data_frame
#import functions
from functions.Queries import *
from functions.Tips_Engine import *
from pages import MedField_page,DevList_page   
#import global variables
import pages

#NAVBAR CALLBACKS

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, so the button is visually selected 
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")])
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(              #collapse/extend sidebar (large screen)
    [Output("sidebar", "className"),
    Output("popover-target","style")],
    [Input("sidebar-toggle", "n_clicks"),
    Input("url", "pathname")],
    [State("sidebar", "className")])
def toggle_classname(n, url, classname):
    if dash.callback_context.triggered[0]['prop_id'].split('.')[0]=='url':
        return "collapsed",{"display": "inline-block"}
    elif n and classname == "collapsed":
        return "",{"display": "none"}       
    return "collapsed",{"display": "inline-block"}     


@app.callback(              #collapse/extend navbar (small screen)
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


#SEARCH CALLBACKS
@app.callback(                               #popover animation
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")])
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(                  #search2 (popover) tips update
    Output('inputSearch2', 'options'),
    Input('inputSearch2', 'search_value'))
def update_tips(value):
    if value:
        return Tips(value)
    else:
        return [{
                    'label': "",
                    'value': ""
                }]


@app.callback(                  #search1 (sidebar) tips update
    Output('inputSearch1', 'options'),
    Input('inputSearch1', 'search_value'))
def update_tips(value):
    if value:
        return Tips(value) 
    else:
        return [{
                    'label': "",
                    'value': ""
                }]


@app.callback(                  #search redirect 
    Output('url', 'pathname'),
    [Input('inputSearch2', 'value'),
    Input('inputSearch1', 'value')])
def change_url(value2,value1): 
    if value2 or value1:   
        id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        key=value1 if id=="inputSearch1" else value2        #choose the correct dropdown menu from which value is taken
        keyType=key.split('&=')[0]
        keyValue=key.split('&=')[1]
        if keyType=="id":
            pages.Search_Query=pages.df[pages.df['device_id']==int(keyValue)]
            return "/DevSearch"
        elif keyType=="mf":   #if key is medical field
            pages.Search_Query=pages.df[pages.df['medical_field']==keyValue].reset_index(drop=True)    #page with all dev types of med field selected
            pages.titlePage=f"Device types of field {keyValue}"
            return "/MedField"
        elif keyType=="dt":   #if key is device type
            pages.Search_Query=pages.df[pages.df['device_type']==keyValue].reset_index(drop=True)    #page with all devices of dev type selected   
            pages.titlePage=f"Devices of type {keyValue}"
            return "/DevList"
        elif keyType=="man":   #if key is manufacturer
            pages.Search_Query=pages.df[pages.df['name_manufacturer']==keyValue].reset_index(drop=True)    #page with all devices of manufacturer selected  
            pages.titlePage=f"Devices of manufacturer {keyValue}"
            return "/DevList"
    else:
        raise PreventUpdate


@app.callback(                               #next/previous buttons for dev list page
    [Output("Devices_Deck", "children"),
    Output("progressPage","children"),
    Output("BtNext","disabled"),
    Output("BtPrev","disabled")],
    [Input("BtNext", "n_clicks"),
    Input("BtPrev", "n_clicks")])
def movePage(button1, button2):
    id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if id=="BtNext" and button1:
        pages.pageCount+=1
    elif id=="BtPrev" and button2:
        pages.pageCount-=1
    else:
        raise PreventUpdate
    tmp=len(pages.Search_Query.drop_duplicates(subset=['device_id']))
    progress=f"{(15+15*pages.pageCount) if (15+15*pages.pageCount)<=tmp else tmp}/{tmp}"
    if pages.pageCount==0:
        return DevList_page.populateCards(pages.Search_Query),progress,False,True
    elif (15+15*pages.pageCount)>tmp:
        return DevList_page.populateCards(pages.Search_Query),progress,True,False
    else:
        return DevList_page.populateCards(pages.Search_Query),progress,False,False


@app.callback(                               #next/previous buttons for dev types page
    [Output("Types_Deck", "children"),
    Output("progressPageType","children"),
    Output("BtNext2","disabled"),
    Output("BtPrev2","disabled")],
    [Input("BtNext2", "n_clicks"),
    Input("BtPrev2", "n_clicks")])
def movePage(button1, button2):
    id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if id=="BtNext2" and button1:
        pages.pageCount+=1
    elif id=="BtPrev2" and button2:
        pages.pageCount-=1
    else:
        raise PreventUpdate
    tmp=len(pages.Search_Query.drop_duplicates(subset=['device_type']))
    progress=f"{(15+15*pages.pageCount) if (15+15*pages.pageCount)<=tmp else tmp}/{tmp}"
    if pages.pageCount==0:
        return MedField_page.populateCardsTypes(pages.Search_Query),progress,False,True
    elif (15+15*pages.pageCount)>tmp:
        return MedField_page.populateCardsTypes(pages.Search_Query),progress,True,False
    else:
        return MedField_page.populateCardsTypes(pages.Search_Query),progress,False,False  


# PAGE 1 CALLBACKS

@app.callback(
    Output('FreqActClass', 'figure'),
    [Input('DD2', 'value'),
    Input("DD14","value")])
def update_G2(DD2,DD14):                             #frequencies of act_class values
    if DD14=="All-time":
        tmp=ExtractData(pages.df,"action_classification",2,country=DD2) 
    else:
        tmp=ExtractData(ExtractData(pages.df,"date",4,keyWord=DD14),"action_classification",2,country=DD2)

    return {
        'data': [
                {'x': tmp.index,
                 'y': tmp,
                 'type': 'bar'}
            ],
        'layout':{
            "title":"Class distribution - {}".format(DD2),
            'margin':{"l":30,"r":0,"t":40,"b":40},
            'height':300,
        }
    }


@app.callback(
    Output('RecallsPie', 'figure'),
    [Input('DD3', 'value'),
    Input('DD15', 'value')])
def update_G3(DD3,DD15):                              # n. of (type) for each country
    if DD15=="All-time":
        tmp=ExtractData(pages.df,"type",3,keyWord=DD3)
    else:
        tmp=ExtractData(ExtractData(pages.df,"date",4,keyWord=DD15),"type",3,keyWord=DD3)
    
    figure=px.pie(values=tmp, names=get_keys(tmp.index), title=f"{DD3} for each country (n={tmp.sum()})")
    figure.update_traces(textposition='inside')
    figure.update_layout(margin=dict(l=0, r=0, t=40, b=10),height=300,font={"size":10})
    return figure


@app.callback(
    Output('Top5PieMan', 'figure'),
    [Input('DD1', 'value'),
    Input('DD16', 'value'),
    Input('Top5PieManCheck','value')])
def update_G1(DD1,DD16,ratio):                              # top5 manufacturer for each country (events)
    if DD16=="All-time":
        x=pages.df
    else:
        x=ExtractData(pages.df,"date",4,keyWord=DD16)

    if DD1=="all countries" and ratio:
        tmp=ExtractData(x,"name_manufacturer",1)[0:5].divide(ExtractData(x,"name_manufacturer",1,unique="")[0:5])  #events/devices
    elif DD1=="all countries":
        tmp=ExtractData(x,"name_manufacturer",1)[0:5]
    elif ratio:
        tmp=ExtractData(x,"name_manufacturer",2,country=DD1)[0:5].divide(ExtractData(x,"name_manufacturer",2,country=DD1,unique="")[0:5])
    else:
        tmp=ExtractData(x,"name_manufacturer",2,country=DD1)[0:5]

    figure=px.pie(values=tmp, names=tmp.index)
    figure.update_traces(textposition='inside',textinfo='percent+label')
    figure.update_layout(margin=dict(l=0, r=0, t=40, b=10),height=300,showlegend=False,title=dict(text=f"Top 5 {DD1}'s manufacturers (events)",font=dict(size=12)))
    return figure
    

@app.callback(
    Output('Top5PieDev', 'figure'),
    [Input('DD11', 'value'),
    Input('DD17', 'value')])
def update_G11(DD11,DD17):                              # top5 manufacturer for each country (devices)
    if DD17=="All-time":
        x=pages.df
    else:
        x=ExtractData(pages.df,"date",4,keyWord=DD17)
    
    if DD11=="all countries":
        tmp=ExtractData(x,"name_manufacturer",1,unique="")[0:5]
    else:
        tmp=ExtractData(x,"name_manufacturer",2,country=DD11,unique="")[0:5]

    figure=px.pie(values=tmp, names=tmp.index)
    figure.update_traces(textposition='inside',textinfo='percent+label')
    figure.update_layout(margin=dict(l=0, r=0, t=40, b=10),height=300,showlegend=False,title=dict(text=f"Top 5 {DD11}'s manufacturers (devices)",font=dict(size=12)))
    return figure


@app.callback(                                      #number of events per country World map
    Output('WorldMap', 'figure'),
    Input('WorldCheck', 'value'))
def updateWorldMap(ratio):
    if ratio:
        EventsCountryPlot=ExtractData(pages.df,"country",1).divide(ExtractData(pages.df,"country",1,unique=""))  #events/devices  
    else:
        EventsCountryPlot=ExtractData(pages.df,"country",1)
    EventsCountryPlot.name="events"
    figure=px.choropleth(EventsCountryPlot,locations=EventsCountryPlot.index,color="events",hover_name=get_keys(EventsCountryPlot.index),range_color=[min(EventsCountryPlot),max(EventsCountryPlot)*2/3],color_continuous_scale=px.colors.sequential.Cividis_r)
    figure.update_layout(height=300,title="Events per country",title_x=0.5,margin=dict(l=0, r=0, t=40, b=0))

    return figure


@app.callback(
    Output('MedField_events', 'figure'),
    [Input('DD12', 'value'),
    Input('DD18', 'value'),
    Input("MedField_eventsCheck","value")])
def update_G12(DD12,DD18,ratio):                              # medical fields distribution (events)

    if DD18=="All-time":
        x=pages.df
    else:
        x=ExtractData(pages.df,"date",4,keyWord=DD18)

    if DD12=="all countries" and ratio:
        tmp=ExtractData(x,"medical_field",1).divide(ExtractData(x,"medical_field",1,unique="")) #events/devices
    elif DD12=="all countries":
        tmp=ExtractData(x,"medical_field",1)
    elif ratio:
        tmp=ExtractData(x,"medical_field",2,country=DD12).divide(ExtractData(x,"medical_field",2,country=DD12,unique=""))
    else:
        tmp=ExtractData(x,"medical_field",2,country=DD12)

    figure=px.pie(values=tmp, names=tmp.index)
    figure.update_traces(textposition='inside',textinfo='percent+label')
    figure.update_layout(margin=dict(l=0, r=0, t=40, b=10),height=300,showlegend=False,title=dict(text=f"Events per medical field in {DD12}",font=dict(size=12)))
    return figure


@app.callback(
    Output('MedField_devices', 'figure'),
    [Input('DD13', 'value'),
    Input('DD19', 'value')])
def update_G13(DD13,DD19):                              # medical fields distribution (devices)

    if DD19=="All-time":
        x=pages.df
    else:
        x=ExtractData(pages.df,"date",4,keyWord=DD19)

    if DD13=="all countries":
        tmp=ExtractData(x,"medical_field",1,unique="")
    else:
        tmp=ExtractData(x,"medical_field",2,country=DD13,unique="")


    figure=px.pie(values=tmp, names=tmp.index)
    figure.update_traces(textposition='inside',textinfo='percent+label')
    figure.update_layout(margin=dict(l=0, r=0, t=40, b=10),height=300,showlegend=False,title=dict(text=f"Devices per medical field in {DD13}",font=dict(size=12)))
    return figure


@app.callback(
    Output('SunBurst', 'figure'),
    [Input('DD20', 'value')])
def update_G14(DD20):                              # Event's type for each country

    if DD20!="All-time":
        tmp=ExtractData(pages.df,"date",4,keyWord=DD20)
    else:
        tmp=pages.df

    return px.sunburst(tmp, path=['Continent', 'country', 'type'], values=[1]*len(tmp)).update_layout(height=400,margin=dict(l=0, r=0, t=10, b=0))


@app.callback(
    Output('4grpahs', 'figure'),
    [Input('DD21', 'value'),
    Input('DD22', 'value')])
def update_G15(DD21,DD22):                              # 4 country plots (medical fields for each risk class)

    figure=make_subplots(rows=2, cols=2,subplot_titles=("USA", "El Salvador", "Canada", "Australia"))
    if DD22=="All-time":
        x=pages.df
    else:
        x=ExtractData(pages.df,"date",4,keyWord=DD22)

    tmp=ExtractData(x,"action_classification",4,keyWord=DD21)
    i=1
    j=1
    for var in ['USA','SLV','CAN','AUS']:
        tmp2=ExtractData(ExtractData(tmp,"country",4,keyWord=var),"medical_field",1)
        figure.add_trace(go.Bar(x=[i[0:10]+".." if len(i)>10 else i for i in tmp2.index], y=tmp2),row=j, col=i).update_layout(xaxis_tickangle=-45)
        j=j+1 if i==2 else j
        i=i+1 if i<2 else i-1
    figure.update_layout(showlegend=False,margin=dict(l=0, r=0, t=40, b=0),title="medical fields for risk "+DD21)
    return figure


# PAGE 2 CALLBACKS

@app.callback(
    Output('DD7-manufacturer', 'options'),
    Input('DD6-med_field', 'value'))
def update_DD7(DD6):                             #update DD7 with manufacturer of selected medical field
    global device
    if DD6:
        device=pages.df[pages.df['medical_field'] == DD6]
        return [{
                    'label': i,
                    'value': i
                } for i in device['name_manufacturer'].dropna().unique()]
    else:
        return [{
                    'label': "",
                    'value': ""
                }]


@app.callback(
    Output('DD8-device', 'options'),
    Input('DD7-manufacturer', 'value'))
def update_DD8(DD7):                             #update DD8 with devices of selected manufacturer
    global device,device2
    if DD7:
        device2=device[device['name_manufacturer']==DD7] 
        return [{
                    'label': i["name"][0:40] + '...' if len(i)>40 else i["name"][0:40],
                    'value': i["device_id"]
                } for index,i in device2.drop_duplicates(subset=["device_id"]).iterrows()]
    else:
        return [{
                    'label': "",
                    'value': ""
                }]


@app.callback(
    Output('AdvanceDeviceButton', 'disabled'),
    Input('DD8-device', 'value'))
def enableButton(DD8):                             #update button 1
    global device2,device3
    if DD8:
        device3=device2[device2['device_id']==DD8]  
        return False
    else:
        return True


@app.callback(
    Output('DD10', 'options'),
    Input('DD9', 'value'))
def update_DD10(DD9):                             #update DD10 with device types of selected medical fields
    global device4
    if DD9:
        device4=pages.df[pages.df['medical_field'] == DD9]
        return [{
                    'label': "insulin pump",
                    'value': "insulin pump"
                }]    #insulin pump is the only one becouse of necessity of a demo
    else:
        return [{
                    'label': "",
                    'value': ""
                }]


@app.callback(
    Output('AdvanceDevTypeButton', 'disabled'),
    Input('DD10', 'value'))
def enableButton2(DD10):                             #update button 2
    global device4,device5
    if DD10:
        device5=device4[device4['name'].str.contains(DD10,case=False, na=False) | device4['device_type'].str.contains(DD10,case=False, na=False)] #is a demo, works only with insulin pump type 
        return False
    else:
        return True


@app.callback(
    Output("placeholder","value"),
    [Input("AdvanceDeviceButton", "n_clicks"),
    Input("AdvanceDevTypeButton","n_clicks")],
    State("DD10","value")
    )
def SearchDevice(click1,click2,DD10):                             #action on click (all buttons of page here)
    global device3,device5
    id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if id=="AdvanceDeviceButton":
        pages.Search_Query=device3
    elif id== "AdvanceDevTypeButton":
        pages.Search_Query=device5
        pages.titlePage=f"Devices of type {DD10}"
    return ""


@app.callback(
    Output('DD5', 'options'),
    Input('DD4', 'value'))
def update_DD5(DD4):                             #update DD5 with devices of selected country
    if DD4:
        tmp=ExtractData(pages.df,"name",2,country=DD4)
        return [{
                    'label': i[0:40] + '...' if len(i)>40 else i[0:40],
                    'value': i
                } for i in tmp.index]
    else:
        return [{
                    'label': "",
                    'value': ""
                }]


@app.callback(
    Output('textarea', 'value'),
    [Input('DD5', 'value')],
    State('DD4', 'value'))
def Give_number(DD5,DD4):                              # update textbox with devices events count
    if DD5:
        tmp=ExtractData(pages.df,"name",2,country=DD4)
        return "Number of events: "+str(tmp.loc[DD5])
    else:
        return ""


# PAGE 3 CALLBACKS

@app.callback(
    Output('Done/NotDone', 'figure'),
    Output('CountryDistr', 'figure'),
    Output('TypeDistr','figure'),
    Output('TrendSpec','figure'),
    Output('PapersSpec_graphs', 'style'),
    Input('DD23', 'value'))
def update_PapersSpec(DD23):                              # update graphs for specific dev_type papers 

    if DD23:
        #import csv 
        papers=pd.read_csv(pages.pathfileData+"papers/"+DD23+".csv",low_memory=False)
        #data1= ExtractData(papers,"checked",1)
        data2=ExtractData(papers,"country",1)
        data3=ExtractData(papers,"type",1)
        data4=ExtractData(papers,"date",1)
        #plot data
        #figure1=px.bar(x=data1.index, y=data1,title='Done/Not Done',labels={"x":"","y":""})
        figure1=px.sunburst(papers, path=['checked', 'type'], values=[1]*len(papers))
        figure1.update_layout(margin=dict(l=10, r=10, t=60, b=10),height=300,title='Done/Not Done (click to interact)')
        
        figure2=px.pie(values=data2, names=data2.index, title='Country distribution')
        figure2.update_traces(textposition='inside')
        figure2.update_layout(margin=dict(l=10, r=10, t=60, b=10),height=300)

        figure3=px.pie(values=data3, names=data3.index, title='Paper\'s type distribution')
        figure3.update_traces(textposition='inside')
        figure3.update_layout(margin=dict(l=10, r=10, t=60, b=10),height=300)
        
        figure4=px.area(x=data4.index, y=data4,labels={"x":"Year","y":"Publications"})
        figure4.update_xaxes(
                        rangeslider_visible=True,
                        dtick="M12",
                        rangeselector=dict(
                            buttons=list([
                                dict(count=6, label="6 month", step="month", stepmode="backward"),
                                dict(count=1, label="1 year", step="year", stepmode="backward"),
                                dict(count=2, label="2 years", step="year", stepmode="backward"),
                                dict(step="all")])))
        figure4.update_layout(margin=dict(l=0, r=10, t=60, b=0),title_text='Publications trend over years', title_x=0.5,height=300)

        return figure1,figure2,figure3,figure4,{"display":"block"}
    
    else:
        raise PreventUpdate


#PAPERS PAGE
""" not used anymore, bugs with custom mode sorting
operators = [['ge ', '>='],
            ['le ', '<='],
            ['lt ', '<'],
            ['gt ', '>'],
            ['ne ', '!='],
            ['eq ', '='],
            ['contains '],
            ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

@app.callback(                      # table content management 
    Output('table', 'data'),
    Input('table', "page_current"),
    Input('table', "page_size"),
    Input('table', 'sort_by'),
    Input('table', 'filter_query'))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = pages.tmpPapers
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')
"""

@app.callback(                  #download papers data 
    Output("downloadFile","data"),
    Input("download","n_clicks"),
    Input("downloadAll","n_clicks"),
    [State('table', "derived_virtual_data"),
    State('table', "derived_virtual_selected_rows")])
def DownloadData(Dow_selected,Dow_All,data1,data2):
    if Dow_selected or Dow_All:
        id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if id=='download':
            data=[]
            for item in data2:
                data.append(data1[item])
            data2=pd.DataFrame.from_dict(data)
            return send_data_frame(data2[["title","ref","type","abstract"]].to_csv, pages.dev_type_selected+"_Selection.csv")
        else:
            return send_data_frame(pages.tmpPapers[["title","ref","type","abstract"]].to_csv, pages.dev_type_selected+".csv")
    else:
        raise PreventUpdate


@app.callback(                   #button to close modal / save progress 
    Output("modal-centered", "is_open"),
    Input("close-centered", "n_clicks"),
    Input("save-button", "n_clicks"),
    State("modal-centered", "is_open"),
    State("table","derived_virtual_data"))
def toggle_modal(b1,b2, is_open,table):
    trigger=dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger=="close-centered":
        return False             #open modal form
    elif trigger=="save-button":
        pd.DataFrame(table).to_csv(pages.pathfileData+"papers/"+pages.dev_type_selected+".csv",index=False) #update dev_type file with papers
        for file in os.listdir(pages.pathfileData+ 'papers/'):
            pages.page3.Done=pd.Series()                #update papers stats data of done/not done
            pages.page3.Done=pages.page3.Done.add(ExtractData(pd.read_csv(pages.pathfileData+ 'papers/'+file,low_memory=False),"checked",1),fill_value=0)
        pages.page3.Donefigure.update_traces(x=pages.page3.Done.index, y=pages.page3.Done)

        return True             #open modal form
    return is_open


@app.callback(                  #show abstract
    Output("modal2","is_open"),
    Output("Head_Abs","children"),
    Output("Body_Abs","children"),
    Output("placeholder2","children"),
    Input("table","active_cell"),
    Input("close2", "n_clicks"),
    State('table', "derived_virtual_data"))
def OpenAbstract(cell,close,data):
    if cell or close:
        trigger=dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if cell is None:
            cell={"column":0}
        if trigger=="table" and cell['column']==2:
            return True,data[cell['row']]['title'],data[cell['row']]['abstract']," "
        elif trigger=="close2":
            return False,"",""," "
        else:
            raise PreventUpdate
    else:
        return False,"",""," "


@app.callback(          #workaround for a dash bug, which does not permit same input as output
    Output("table","active_cell"),
    Input("placeholder2","children"))
def temp(x):
    return None


#SETTINGS PAGE

@app.callback(                  #progress bar
    [Output("progress", "value"), Output("progress", "children")],
    [Input("progress-interval", "n_intervals")])
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    progress = min(n % 110, 100)
    # only add text after 5% progress to ensure text isn't squashed too much
    return progress, f"{progress} %" if progress >= 5 else ""