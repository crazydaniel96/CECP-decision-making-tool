import dash_html_components as html
import dash_bootstrap_components as dbc
import pages

def populateMedFieldPage():
  pages.pageCount=0 #reset page count
  tmp=len(pages.Search_Query.drop_duplicates(subset=['device_type']))
  progress=f"{(15+15*pages.pageCount) if (15+15*pages.pageCount)<=tmp else tmp}/{tmp}"
  layout=html.Div(
          [
            dbc.Row(
              [
                dbc.Col(
                  [
                    html.H2(pages.titlePage),
                  ],
                  className="shadow p-3 m-3 bg-white rounded",
                ),
              ],
            ),
            dbc.Row(
              [
                dbc.Col(
                  [
                    dbc.CardColumns(populateCardsTypes(pages.Search_Query),id="Types_Deck")    #dbc.Spinner
                  ],                  
                ),
              ],
            ),
            html.Div(
                html.Div(progress,className="lead",id="progressPageType",style={"font-size":"medium"}),
              style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
            ),
            html.Div([
                dbc.Button("Previous", color="dark",id="BtPrev2",className="m-3",style={"width":"6rem"}),
                dbc.Button("Next", color="dark",id="BtNext2",className="m-3",style={"width":"6rem"}),
              ],
              style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
            ),
          ],
        )   
  return layout

def populateCardsTypes(devices):
  cards=[]
  devices=devices["device_type"].unique()      #for unique results
  for i in range(0+15*pages.pageCount,15+15*pages.pageCount):
    if len(devices)<=i:
      break
    card_content = [

      #dbc.CardHeader(str(devices['name_manufacturer'][i])),      
      dbc.CardBody(
        [
          html.H5(str(devices[i]), className="card-title"),
          #dbc.CardLink("Open", href="/DevList="+str(devices[i])), #old button style
          dbc.Button("Open", outline=True, color="dark",href="/DevList="+str(devices[i])),  
        ]
      ),
    ]
    cards.append(dbc.Card(children=card_content, color="light"))
  return cards