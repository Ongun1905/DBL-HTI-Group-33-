# Import Node Link functions from another Python file
from datetime import date
from dash import dependencies
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
import math as mt

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
isLive = False
disableState = True
month = 1
year = 1998
n_intervals_start = 0
endMonth = 12
endYear = 9999

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
        
        html.Div(children=[ #top right component - uploading dropdown + text + animation
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
                                placeholder="select dataset from uploaded files"
                            )
                        ], style={'color':'black'}
                    ), 
                    dcc.Markdown('''
                        The enron dataset contains is the default on this website.
                        The different versions differ in the amount of entries in the dataset.

                        **Animation Controls:**
                        ''',
                        style={'margin-left':'5%'}
                    ),
                    #html.Pre(id='click-data'),
                    dcc.Dropdown(
                        id='speed-dropdown',
                        options=[
                            {'label': '0.015625 seconds (for performant GPUs)', 'value': '15.625'},
                            {'label': '0.33 seconds (for performant GPUs)', 'value': '330'},
                            {'label': '0.5 seconds (for performant GPUs)', 'value': '500'},
                            {'label': '1 second (for performant GPUs)', 'value': '1000'},
                            {'label': '2 seconds (for performant GPUs)', 'value': '2000'},
                            {'label': '3 seconds', 'value': '3000'},
                            {'label': '4 seconds', 'value': '4000'},
                            {'label': '5 seconds', 'value': '5000'},
                            {'label': '6 seconds', 'value': '6000'},
                            {'label': '7 seconds', 'value': '7000'},
                            {'label': '8 seconds', 'value': '8000'},
                            {'label': '9 seconds', 'value': '9000'},
                            {'label': '10 seconds', 'value': '10000'}
                        ],
                        placeholder="Select Animation speed (in seconds - 3 default)",
                        style={'width': '94.9%','margin-left':'2.5%', 'color':'black'}
                    ),
                    html.Br(),
                    dcc.Interval(
                        id='interval-component',
                        interval = 3000, # in milliseconds
                        n_intervals = 0,
                        disabled = True
                    ),
                    html.Button(id='play-button-state', n_clicks=0, children='Play Animation from the beginning', style={'width': '90%', 'margin-left':'5%'}),
                    html.Br(),
                    html.Button(id='pause-button-state', n_clicks=0, disabled = True, children='Pause Animation', style={'width': '90%', 'margin-left':'5%'}),
                    html.Br(),
                    html.Button(id='resume-button-state', n_clicks=0, disabled = True, children='Resume Animation', style={'width': '90%', 'margin-left':'5%'}),
                    html.Br(),
                    dcc.Textarea(
                        id='text-year-month',
                        value='Animation status: not active.',
                        contentEditable = False,
                        draggable = False,
                        rows = 1,
                        readOnly = True,
                        persistence= True,
                        persistence_type= 'session',
                        style={'width': '89%', 'height':'15px', 'margin-left':'5%'},
                    ),
                ], className='three columns', style={'color':'#65cca9', 'background':'#363F48', 'width':'48.5%', 'height':'400px', 'display':'flex','justify-content':'flex-start','flex-direction':'column', 'border-radius':'1rem'})
], style={'display':'flex','flex-direction':'row','justify-content':'space-between', 'width':'100%', 'align-items':'center'}
),

html.Div(children = [dcc.Graph(id="mail-graph", #bottom component - graph
        figure=nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year))
        ], style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-top': '3vw','width': '100%', 'height': '500px'}
        )
], style={'display':'flex', 'flex-direction':'column','align-items':'center','justify-content': 'space-between'}
)


@app.callback(                                                              # This app callback updates the graph when played or paused
     [dash.dependencies.Output('interval-component', 'interval'),
      dash.dependencies.Output('interval-component', 'disabled'),
      dash.dependencies.Output('text-year-month', 'value'),
      dash.dependencies.Output('pause-button-state', 'disabled'),
      dash.dependencies.Output('resume-button-state', 'disabled'),
      dash.dependencies.Output('mail-graph', 'figure')],                  
     [dash.dependencies.Input('submit-button-state', 'n_clicks'),
      dash.dependencies.Input('play-button-state', 'n_clicks'),
      dash.dependencies.Input('pause-button-state', 'n_clicks'),
      dash.dependencies.Input('resume-button-state', 'n_clicks'),
      dash.dependencies.Input('interval-component', 'n_intervals'),
      dash.dependencies.State('speed-dropdown', 'value'),       
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
def update_play_output(n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_intervals, animationSpeed, value, jobFromInput, jobToInput, mailFromInput, mailToInput, mailStartDate, mailEndDate, tocc, showhide, file):
    if file != None:
        vis1Graph, jobFrom, jobTo, mailFrom, mailTo, minDate, maxDate = nlf.createGraph(file)
    else:
        vis1Graph, jobFrom, jobTo, mailFrom, mailTo, minDate, maxDate = nlf.createGraph('enron-v1.csv')
    sentimentRange = value
    jobFromRange = jobFromInput
    jobToRange = jobToInput
    mailFromRange = mailFromInput
    mailToRange = mailToInput
    animationSpeedInit = animationSpeed
    global dateStart, dateEnd
    dateStart = pd.to_datetime(mailStartDate)
    dateEnd = pd.to_datetime(mailEndDate)
    toccSelect = tocc
    showhideNodes = showhide
    global n_intervals_start
    global month, year
    month = (dateStart.month + n_intervals - n_intervals_start) % 12
    if (month == 0):
        month = 12
    year = dateStart.year + mt.floor((dateStart.month + n_intervals - n_intervals_start) / 12) - 1
    if (not (month == 12)):
        year += 1
    ctx = dash.callback_context
    if (not ctx.triggered and n_clicks1 == 0 and n_clicks2 == 0 and n_clicks3 == 0 and n_clicks4 == 0):
        global isLive, disableState
        isLive = False
        disableState = True
        return dash.no_update, disableState, 'Animation status: not active.', True, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
    else:
        btn_id = [b['prop_id'] for b in dash.callback_context.triggered][0]
        if 'play-button-state' in btn_id:
            global endMonth, endYear
            endMonth = dateEnd.month
            endYear = dateEnd.year
            isLive = True
            disableState = False
            n_intervals_start = n_intervals
            month = dateStart.month
            year = dateStart.year
            if animationSpeedInit is None:
                animationSpeedInit = 3000
            return animationSpeedInit, disableState, 'Animation: active. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), False, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
        elif 'pause-button-state' in btn_id:
            isLive = True
            disableState = True
            return dash.no_update, disableState, 'Animation: active. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), True, False, dash.no_update
        elif 'resume-button-state' in btn_id:
            isLive = True
            disableState = False
            if animationSpeedInit is None:
                animationSpeedInit = 3000
            return animationSpeedInit, disableState, 'Animation: active. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), False, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
        elif 'submit-button-state' in btn_id:
            isLive = False
            disableState = True
            n_intervals_start = n_intervals
            return dash.no_update, disableState, 'Animation status: not active.', True, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
        else:
            if ((year == endYear and month > endMonth) or year > endYear):
                isLive = False
                disableState = True
                return dash.no_update, disableState, 'Animation: active. Timestamps: Year: ' + str(endYear) + ', Month: ' + str(endMonth), True, True, dash.no_update
            if isLive:
                return dash.no_update, disableState, 'Animation: active. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), False, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)


@app.callback(output=dash.dependencies.Output('fileDropDown', 'options'),       # This app callback makes sure the media folder is
              inputs=[dash.dependencies.Input('refreshDropDown', 'n_clicks')])  # updated when clicking the dataset dropdown menu
def change_my_dropdown_options(n_clicks):                                       # The newly uploaded files can now also be selected
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    options = [{'label': j, 'value': j} for j in os.listdir(settings.MEDIA_ROOT)]
    return options

if __name__ == '__main__':
    app.run_server(debug=True)
