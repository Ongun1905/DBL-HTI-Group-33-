# Import Node Link functions from another Python file
from networkx.algorithms.tree.coding import to_nested_tuple
from networkx.algorithms.tree.mst import maximum_spanning_edges
from networkx.generators.geometric import thresholded_random_geometric_graph
import NodeLinkFunctions as nlf

# Import settings to allow BASE_DIR to be used
from django.conf import settings

# Make sure you have plotly and networkx installed before running this code!
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
import dash
import dash_core_components as dcc
import dash_html_components as html
import os

# -------------------------------------------------------
# Visualisation 1
#
# This codes generates an interactive graph for the first
# visualization.
# -------------------------------------------------------

# Global Filtering Variables
sentimentRange = [-1, 1]
jobFromRange = []
jobToRange = []
mailFromRange = []
mailToRange = []
toccSelect = []
showhideNodes = True

# Set up initial graph with positions and node attributes
vis1Graph, jobFrom, jobTo, mailFrom, mailTo, minDate, maxDate = nlf.createGraph('enron-v1.csv')

dateStart = minDate 
dateEnd = maxDate

# Get external styles for the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialise Dash app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
from django_plotly_dash import DjangoDash
app = DjangoDash('GraphVisualisation')
app.title = "Email Network"

####
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Generating Layout
app.layout = html.Div([
html.Div(children = [ #top compontent - containes two subdivs
        html.Div(children = [ #top left compontent - containes all filter options (54-149)
                html.Div(children = [
                        dcc.RangeSlider(
                            id='my-range-slider',
                            min=-1,
                            max=1,
                            step=0.01,
                            marks={
                            -1: {'label': '-1: Very Negative Email', 'style': {'color': '#f50', 'width':'50px'}},
                            0: {'label': '0: Neutral Email', 'style': {'color': '#ffffff'}},
                            1: {'label': '1: Very Positive Email', 'style': {'color': '#77b0b1'}},
                            },
                            value=[-1, 1],
                            allowCross=False,   
                            persistence= True,
                            persistence_type= 'session'
                        ),
                        html.Br(),#breaks space between the interactive elements
                        html.Br(),#breaks space between the interactive elements
                    ], style = {'width': '90%', 'margin-left':'5%'}
                ),
                html.Div(children = [
                        dcc.Dropdown(
                            id='jobFrom-dropdown',
                            options=[
                                {'label': j, 'value': j} for j in sorted(jobFrom)
                            ],
                            multi = True,
                            placeholder="Select from Job, Nothing = all",
                            persistence= True,
                            persistence_type= 'session'                        ),
                        dcc.Dropdown(
                            id='jobTo-dropdown',
                            options=[
                                {'label': j, 'value': j} for j in sorted(jobTo)
                            ],
                            multi = True,
                            placeholder="Select to Job, Nothing = all",
                            persistence= True,
                            persistence_type= 'session'                            
                        )
                    ], style = {'width': '100%'}
                ),
                html.Div(children = [
                        dcc.Dropdown(
                            id='mailFrom-dropdown',
                            options=[
                                {'label': j, 'value': j} for j in sorted(mailFrom)
                            ],
                            multi = True,
                            placeholder="Select from Email, Nothing = all",
                            persistence= True,
                            persistence_type= 'session'                            
                        ),
                        dcc.Dropdown(
                            id='mailTo-dropdown',
                            options=[
                                {'label': j, 'value': j} for j in sorted(mailTo)
                            ],
                            multi = True,
                            placeholder="Select to Email, Nothing = all",
                            persistence= True,
                            persistence_type= 'session'                            
                        )
                    ], style = {'width': '100%'}
                ),
                html.Br(),
                html.Div(
                    dcc.DatePickerRange(
                        id='mail-date-range',
                            min_date_allowed=minDate,
                            max_date_allowed=maxDate,
                            initial_visible_month=minDate,
                            start_date = minDate,
                            end_date = maxDate,
                            start_date_placeholder_text="MMM Do, YYYY",
                            end_date_placeholder_text="MMM Do, YYYY",
                            first_day_of_week = 1,
                            display_format='MMM Do, YYYY',
                            persistence= True,
                            persistence_type= 'session'                            
                        ), style={'width':'100%', 'margin-left':'21.5%'} # does not work somehow
                ),
                html.Br(),
                dcc.Checklist(
                    id = 'to-cc-checklist',
                    options=[
                        {'label': 'TO', 'value': 'TO'},
                        {'label': 'CC', 'value': 'CC'}
                    ],
                    value=['TO', 'CC'],
                    persistence= True,
                    persistence_type= 'session',                    
                    labelStyle={'display': 'inline-block'},
                    style={'color':'#65cca9', 'margin-left':'41.75%'}
                ), 
                dcc.RadioItems(
                    id = 'node-radio-items',
                    options=[
                        {'label': 'Show unlinked nodes', 'value': 'True'},
                        {'label': 'Hide unlinked nodes', 'value': 'False'}
                    ],
                    value='True',
                    persistence= True,
                    persistence_type= 'session',
                    labelStyle={'display': 'inline-block'},
                    style={'color':'#65cca9', 'margin-left':'18%'}
                ),
                html.Button(id='submit-button-state', n_clicks=0, children='Update Graph', style={'width': '90%', 'margin-left':'5%'}),
                html.Div(id='output-state')
            ], style={'display': 'flex', 'flex-direction': 'column','justify-content':'space-around', 'background-color': '#363F48', 'width':'48.5%', 'height':'400px', 'border-radius':'1rem'}
        ),
        
        html.Div(children=[ #top right component - uploading dropdown +text
                    html.Div(
                        id='refreshDropDown',
                        children = [
                            dcc.Dropdown(
                                id='fileDropDown',
                                options=[
                                    {'label': j, 'value': j} for j in os.listdir(settings.BASE_DIR / 'media')
                                ],
                                value = "enron-v1.csv",
                                placeholder="select dataset from uploaded files"
                            )
                        ], style={'color':'black'}
                    ), 
                    dcc.Markdown('''
                        **select your data set here**

                        The enron dataset contains is the default on this website.
                        The different versions differ in the amount of entries in the dataset.

                        To visualize the selected dataset please hit the 'update graph' button on the left.

                        For large datasets, it may take a while before the graph is loaded.

                        '''), 
                    html.Pre(id='click-data')
                ], className='three columns', style={'color':'#65cca9', 'background':'#363F48', 'width':'48.5%', 'height':'400px', 'display':'flex','justify-content':'flex-start','flex-direction':'column', 'border-radius':'1rem'})
], style={'display':'flex','flex-direction':'row','justify-content':'space-between', 'width':'100%', 'align-items':'center'}
),

html.Div(children = [dcc.Graph(id="mail-graph", #bottom component - graph
        figure=nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes))
        ], style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-top': '3vw','width': '100%', 'height': '500px'}
        )
], style={'display':'flex', 'flex-direction':'column','align-items':'center','justify-content': 'space-between'}
)

@app.callback(                                                              # This app callback updates the graph with all 
     dash.dependencies.Output('mail-graph', 'figure'),                      # selected filters and dataset with the press
     [dash.dependencies.Input('submit-button-state', 'n_clicks'),           # of the 'update graph' button
      dash.dependencies.State('my-range-slider', 'value'), 
      dash.dependencies.State('jobFrom-dropdown', 'value'), 
      dash.dependencies.State('jobTo-dropdown', 'value'), 
      dash.dependencies.State('mailFrom-dropdown', 'value'), 
      dash.dependencies.State('mailTo-dropdown', 'value'), 
      dash.dependencies.State('mail-date-range', 'start_date'),
      dash.dependencies.State('mail-date-range', 'end_date'),
      dash.dependencies.State('to-cc-checklist', 'value'),
      dash.dependencies.State('node-radio-items', 'value'),
      dash.dependencies.State('fileDropDown', 'value')])
def update_output(n_clicks, value, jobFromInput, jobToInput, mailFromInput, mailToInput, mailStartDate, mailEndDate, tocc, showhide, file):
    if file != None:
        vis1Graph, jobFrom, jobTo, mailFrom, mailTo, minDate, maxDate = nlf.createGraph(file)
        #vis1Graph = nlf.createGraph(file)[0]
    else:
        vis1Graph, jobFrom, jobTo, mailFrom, mailTo, minDate, maxDate = nlf.createGraph('enron-v1.csv')
        #vis1Graph = nlf.createGraph(['enron-v1.csv'])[0]
    sentimentRange = value
    jobFromRange = jobFromInput
    jobToRange = jobToInput
    mailFromRange = mailFromInput
    mailToRange = mailToInput
    dateStart = pd.to_datetime(mailStartDate)
    dateEnd = pd.to_datetime(mailEndDate)
    toccSelect = tocc
    showhideNodes = showhide
    return nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes)

@app.callback(output=dash.dependencies.Output('fileDropDown', 'options'),       # This app callback makes sure the media folder is
              inputs=[dash.dependencies.Input('refreshDropDown', 'n_clicks')])  # updated when clicking the dataset dropdown menu
def change_my_dropdown_options(n_clicks):                                       # The newly uploaded files can now also be selected
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    options = [{'label': j, 'value': j} for j in os.listdir('media')]
    return options

if __name__ == '__main__':
    app.run_server(debug=True)
