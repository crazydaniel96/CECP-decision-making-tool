import dash_html_components as html
import dash_bootstrap_components as dbc
from functions.Import_dictionaries import get_keys
import pandas as pd

def populateDevPage(device):
  data=[]
  listCol=["name",'device_id','name_manufacturer','parent_company','medical_field','device_type']
  for item in listCol:
    if not pd.isnull(device[item].iloc[0]):
      data.append(html.Tr([html.Th(item), html.Td(device[item].iloc[0])]))
  
  dev_info=dbc.Table(html.Tbody(data), striped=True, bordered=True, hover=True)  #dark=True
  
  data=[]
  listCol=['id_events','source','type','country','documents','action_classification']
  for index,event in device.iterrows():
    children=[]
    children.append(html.Tr(html.Th(event['date'],rowSpan=len(listCol)+1)))
    for item in listCol:
      if item == 'country' and not pd.isnull(event["country"]):
        children.append(html.Tr([html.Td(get_keys(event[item]))]))
      elif item == 'documents' and not pd.isnull(event["documents"]):
        children.append(html.Tr([html.Td(html.A("Document",href=event[item]))]))  #here
      elif not pd.isnull(event[item]):
        children.append(html.Tr([html.Td(event[item])]))
    data.append(html.Tbody(children))
  dev_events=dbc.Table(data, striped=True, bordered=True, hover=True)

  layout=html.Div(
          [
            dbc.Row(
              [
                dbc.Col(
                  dbc.Row(
                    dbc.Col(
                      [
                        html.H3("Characteristics"),
                        dev_info,
                      ],
                      className="shadow p-3 m-3 bg-white rounded",
                    ),
                  ),
                  width=4,
                ),
                dbc.Col(
                  [
                    html.H3("Events"),
                    dev_events,
                  ],
                  width=7,
                  className="shadow p-3 m-3 bg-white rounded",
                ),
              ],
            )
          ],
        )   
  return layout