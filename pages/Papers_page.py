import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import pages
import dash_table
from dash_extensions import Download

def populatePapersPage():
  PAGE_SIZE = 20
  pages.tmpPapers=pd.read_csv(pages.pathfileData+'papers/'+pages.dev_type_selected+'.csv', low_memory= False)
  layout=html.Div(
    [
      dbc.Row(dbc.Col(html.H2("Papers for "+pages.dev_type_selected)),className="shadow p-3 m-3 bg-white rounded"),
      dbc.Row(
          dbc.Col(
              dash_table.DataTable(
                  id='table', 
                  data=pages.tmpPapers.to_dict('records'),
                  columns=[
                      {'id':'title','name':'Title','type':'text'},
                      {'id':'ref','name':'Link','type':'text','presentation':'markdown'},
                      {'id':'tmp','name':'Abstract','type':'text'},
                      {'id':'country','name':'Country','type':'text'},
                      {'id':'type','name':'Type','type':'text'},
                      {'id':'date','name':'Date','type':'text'},
                      {'id':'checked','name':'Progress','presentation': 'dropdown'},

                  ],
                  style_cell={
                      'textAlign': 'left',
                      #'overflow': 'hidden',
                      'textOverflow': 'ellipsis',
                      'maxWidth': 0,
                    },
                  style_cell_conditional=[
                      {'if': {'column_id': 'title'},
                      'width': '50%'},
                      {'if': {'column_id': 'ref'},
                      'width': '7%'},
                      {'if': {'column_id': 'tmp'},
                      'width': '7%'},
                      {'if': {'column_id': 'checked'},
                      'width': '8%'},
                      {'if': {'column_id': 'type'},
                      'width': '12%'},
                      {'if': {'column_id': 'country'},
                      'width': '10%'},
                      {'if': {'column_id': 'date'},
                      'width': '6%'},
                  ],
                  style_header={
                    'fontWeight': 'bold'
                  },
                  style_as_list_view=True,
                  page_current= 0,
                  page_size= PAGE_SIZE,
                  page_action="native",
                  cell_selectable=False,

                  filter_action="native",
                  filter_query='',

                  row_selectable='multi',

                  sort_action="native",
                  sort_mode='multi',
                  selected_columns=[],
                  selected_rows=[],
                  editable=True,
                  dropdown={
                        'checked': {
                            'options': [
                                {'label': "Done", 'value': "Done"},
                                {'label': "Not done", 'value': "Not done"}
                            ]
                        },
                  },
                  
                  #tooltip_delay=0,
                  #tooltip_duration=None,
                  #tooltip_data=[
                  #        {'tmp': abstract}
                  #        for abstract in pages.tmpPapers["abstract"]
                  #],
              ),
          ),
      ),
      dbc.Row([
        dbc.Col(
          [
            dbc.Button("Download Selected", outline=True, color="dark",id="download",className="m-2",n_clicks=0),
            dbc.Button("Download All", outline=True, color="dark",id="downloadAll",className="m-2",n_clicks=0),
          ],
          className="col-lg-4",
          align="center"
        ),
        dbc.Col(
          dbc.Row(
            dbc.Button("Save changes", outline=True, color="dark",id="save-button",className="m-2",n_clicks=0),
            justify="center",  
          ),
          className="col-lg-3",
          align="center"
        ),
      ],
        justify="start"
      ),         
      dbc.Modal(
            [
                dbc.ModalBody("Changes correctly saved"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close-centered", className="ml-auto"
                    )
                ),
            ],
            id="modal-centered",
            centered=True,
      ),
      dbc.Modal(
            [
                dbc.ModalHeader(id="Head_Abs"),
                dbc.ModalBody(id="Body_Abs"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close2", className="ml-auto",n_clicks=0,
                    )
                ),
            ],
            id="modal2",
            centered=True,
            size="lg"
      ),
      Download(id="downloadFile"),
      html.Div(id="placeholder2")
    ]
  )
  return layout
