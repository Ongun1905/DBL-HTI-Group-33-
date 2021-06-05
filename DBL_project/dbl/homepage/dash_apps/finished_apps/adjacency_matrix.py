# Import Node Link functions from another Python file
from dash.dependencies import Input, Output, State
import AdjacencyMatrixFunctions as amf

# Import settings to allow BASE_DIR to be used
from django.conf import settings
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
nxGraph, jobFrom, jobTo, mailFrom, mailTo, minDate, maxDate = amf.createGraph('enron-jesse-mini.csv')

dateStart = minDate 
dateEnd = maxDate

# Get external styles for the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialise Dash app
from django_plotly_dash import DjangoDash
app = DjangoDash('AdjacencyMatrix')
app.title = "Adjacency Matrix"

####
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


# Defining the app layout
app.layout = html.Div([
    html.Div(children = [
            
            # Top left compontent: Data filtering options
            html.Div(children = [
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
                                persistence_type= 'session'     ,
                                style={'width':'100%','text-align':'center'}                    
                            ), style={'width':'100%', 'margin':'auto'}
                    ),
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


            # Top right component: Selecting datasets
            html.Div(children=[
                dcc.Markdown('''
                    **Select your data set here:**
                    ''',
                    style={'margin-left':'5%'}
                ),
                html.Div(
                    id='refreshDropDown',
                    children = [
                        dcc.Dropdown(
                            id='fileDropDown',
                            options=[
                                {'label': j, 'value': j} for j in os.listdir(settings.BASE_DIR / 'media')
                            ],
                            value = "enron-v1.csv",
                            placeholder="select dataset from uploaded files",
                            persistence= True,
                            persistence_type= 'session',
                        )
                    ], style={'color':'black'}
                ), 
                dcc.Markdown(
                    '''
                    The enron-v1 dataset is the default on this website.
                    The different versions differ in the amount of entries in the dataset.
                    ''',
                    style={'margin-left':'5%'}
                ),
            ], className='three columns', style={'color':'#65cca9', 'background':'#363F48', 'width':'48.5%', 'height':'400px', 'display':'flex','justify-content':'flex-start','flex-direction':'column', 'border-radius':'1rem'})
            # End of right box wrapper

    ], style={'display':'flex','flex-direction':'row','justify-content':'space-between', 'width':'100%', 'align-items':'center'}),
    # End of wrapper for top 2 boxes

    html.Div(children = [
        dcc.Graph(id="adjacency-matrix-graph", figure=amf.filterGraph(nxGraph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, False, 0, 0))
    ])
], style={'display':'flex', 'flex-direction':'column','align-items':'center','justify-content': 'space-between'})


# Updates the matrix when the "update" button is pressed
@app.callback(
     [Output('adjacency-matrix', 'figure')],
     [State('my-range-slider', 'value'),
      State('jobFrom-dropdown', 'value'),
      State('jobTo-dropdown', 'value'),
      State('mailFrom-dropdown', 'value'),
      State('mailTo-dropdown', 'value'),
      State('mail-date-range', 'start_date'),
      State('mail-date-range', 'end_date'),
      State('to-cc-checklist', 'value'),
      State('node-radio-items', 'value'),
      State('fileDropDown', 'value')])
def update_adjacency_matrix(sentimentValue, jobFromInput, jobToInput, mailFromInput, mailToInput, mailStartDate, mailEndDate, tocc, showhide, file):
    # Create the NX graph from the file if given
    if file != None: nxGraph = amf.createGraph(file)[0]
    else: nxGraph = amf.createGraph('enron-v1.csv')[0]
    
    # Save the variables for potential manipulation
    sentimentRange = sentimentValue
    jobFromRange = jobFromInput
    jobToRange = jobToInput
    mailFromRange = mailFromInput
    mailToRange = mailToInput
    global dateStart, dateEnd
    dateStart = pd.to_datetime(mailStartDate)
    dateEnd = pd.to_datetime(mailEndDate)
    toccSelect = tocc
    showhideNodes = showhide

    # Return the figure to the 'adjacency-matrix' element
    return amf.filterGraph(nxGraph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, False, 0, 0)


# Makes sure the media folder is updated when clicking the dataset dropdown menu
@app.callback(output=Output('fileDropDown', 'options'),
              inputs=[Input('refreshDropDown', 'n_clicks')])
def change_my_dropdown_options(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    options = [{'label': j, 'value': j} for j in os.listdir(settings.MEDIA_ROOT)]
    return options


if __name__ == '__main__':
    app.run_server(debug=True)
