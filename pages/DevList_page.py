import dash_html_components as html
import dash_bootstrap_components as dbc
import pages

def populateDevListPage():
  pages.pageCount=0 #reset page count 
  tmp=len(pages.Search_Query.drop_duplicates(subset=['device_id']))
  progress=f"{(15+15*pages.pageCount) if (15+15*pages.pageCount)<=tmp else tmp}/{tmp}"

  layout=html.Div(
          [
            dbc.Row(
              [
                dbc.Col(html.H2(pages.titlePage),width=10),
                dbc.Col(dbc.Button("Publications", outline=True, color="dark",href="/Publications="+pages.titlePage[pages.titlePage.find("type")+5:])) if "type" in pages.titlePage else html.Div(),  #href contains the device type string obtained from page title
              ],
              className="shadow p-3 m-3 bg-white rounded",
            ),
            dbc.Row(
              [
                dbc.Col(
                  [
                    dbc.CardColumns(populateCards(pages.Search_Query),id="Devices_Deck")    #dbc.Spinner, not necessary becouse animation is fast enough
                  ],                  
                ),
              ],
            ),
            html.Div(
              html.Div(progress,className="lead",id="progressPage",style={"font-size":"medium"}),
              style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
            ),
            html.Div([
                dbc.Button("Previous", color="dark",id="BtPrev",className="m-3",style={"width":"6rem"}),
                dbc.Button("Next", color="dark",id="BtNext",className="m-3",style={"width":"6rem"}),
              ],
              style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
            ),
          ])
  return layout

def populateCards(devices):
  cards=[]
  # next 3 lines convert devices df to a new df with counts of events in a new column and order the new df by this column
  new_device = devices.groupby(['device_id']).first()
  new_device = new_device.join(devices['device_id'].value_counts().to_frame('events'))
  new_device.sort_values(by=['events'],inplace=True,ascending=False)

  for i in range(0+15*pages.pageCount,15+15*pages.pageCount):   
    if len(new_device)<=i:
      break
    card_content = [

      dbc.CardHeader(str(new_device['name_manufacturer'].iloc[i])),       #all converted to str type becouse of possibility of NaN
      dbc.CardBody(
        [
          html.H5(str(new_device['name'].iloc[i]), className="card-title"),
          html.P(
            [
              "Device type: "+str(new_device['device_type'].iloc[i]),
              html.Br(),
              "Medical field: "+str(new_device['medical_field'].iloc[i]),
              html.Br(),
              "parent_company: "+str(new_device['parent_company'].iloc[i]),
              html.Br(),
              "Events: "+str(new_device["events"].iloc[i]),
            ],
            className="card-text",
          ),
          #dbc.CardLink("Open", href="/DevSearch="+str(devices['device_id'].iloc[i])),   #old button style
          dbc.Button("Open", outline=True, color="dark",href="/DevSearch="+str(new_device.index[i])),
        ]
      ),
    ]
    cards.append(dbc.Card(children=card_content, color="light"))
  return cards