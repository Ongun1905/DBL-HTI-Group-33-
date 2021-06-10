# Import Node Link functions from another Python file
import NodeLinkFunctions as nlf

# Import settings to allow BASE_DIR to be used
from django.conf import settings

# Make sure you have plotly and networkx installed before running this code!
from dash.dependencies import Input, Output, State
from networkx.convert_matrix import to_numpy_matrix
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
import numpy as np
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
pauseDisabled = True
resumeDisabled = True

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
dcc.Store(id='session', storage_type='session', data={}),
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
                            persistence_type= 'session',
                        ),
                    ], style = {'width': '90%', 'margin-left':'5%', 'margin-bottom': '2rem'}
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
                        ),
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
                    style={'color':'#65cca9', 'margin': '12px 0'}
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
                    style={'color':'#65cca9'}
                ),
                html.Button(id='submit-button-state', className='button', n_clicks=0, children='Update Filters', style= {'margin': '1rem 0'}),
                html.Div(id='output-state')
            ], style={'display': 'flex', 'flex-direction': 'column','justify-content':'space-around', 'border-radius':'1rem', 'width': '100%', 'padding-left': '2rem'}
        ),

        
        html.Div(children=[ #top right component - uploading dropdown + text + animation
                    dcc.Markdown('''
                        **Select your data set here:**
                        ''', style={ 'margin-bottom': '4px' }),
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
                                style={'color':'black'}
                            )
                        ]
                    ), 
                    dcc.Markdown('''
                        The enron-v1 dataset is the default on this website.
                        The different versions differ in the amount of entries in the dataset.  
                        ''', style={ 'margin-top': '8px' }),
                    dcc.Markdown('''
                        **Animation Controls:**
                        ''', style={ 'margin': '12px 0 4px' }),
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
                            {'label': '10 seconds', 'value': '10000'},
                            {'label': '11 seconds', 'value': '11000'},
                            {'label': '12 seconds', 'value': '12000'},
                            {'label': '13 seconds', 'value': '13000'},
                            {'label': '14 seconds', 'value': '14000'},
                            {'label': '15 seconds', 'value': '15000'},
                            {'label': '16 seconds', 'value': '16000'},
                            {'label': '17 seconds', 'value': '17000'},
                            {'label': '18 seconds', 'value': '18000'},
                            {'label': '19 seconds', 'value': '19000'},
                            {'label': '20 seconds', 'value': '20000'}
                        ],
                        placeholder="Select Animation speed (in seconds - 3 default)",
                        persistence= True,
                        persistence_type= 'session',
                        style={'color':'black'}
                    ),
                    html.Br(),
                    dcc.Interval(
                        id='interval-component',
                        interval = 3000, # in milliseconds
                        n_intervals = 0,
                        disabled = True
                    ),
                    html.Button(id='play-button-state', className='button', n_clicks=0, children='Play Animation from the beginning'),
                    html.Br(),
                    html.Div(
                        children=[
                            html.Button(id='pause-button-state', className='button', n_clicks=0, disabled = True, children='Pause Animation', style={'width': '100%'}),
                            html.Button(id='resume-button-state', className='button', n_clicks=0, disabled = True, children='Resume Animation', style={'width': '100%', 'margin-left':'8px'}),
                        ],
                        style={'display': 'flex'}
                    ),
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
                        style={'height':'30px'},
                    ),
                ], className='three columns', style={'color':'#65cca9', 'display':'flex','justify-content':'flex-start','flex-direction':'column', 'border-radius':'1rem', 'width': '100%', 'padding-right': '2rem', 'margin-left': '2rem'})
], style={'display':'flex','flex-direction':'row','justify-content':'space-between', 'width':'100%', 'align-items':'flex-start'}
),

html.Div(
    className="graph-wrapper",
    children = [
        dcc.Graph(id="mail-graph", figure = nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year))
    ],
    style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-top': '3vw', 'width': '100%', 'height': '500px'}
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
    global dateStart, dateEnd, n_intervals_start, month, year, isLive, disableState, endMonth, endYear, pauseDisabled, resumeDisabled
    dateStart = pd.to_datetime(mailStartDate)
    dateEnd = pd.to_datetime(mailEndDate)
    toccSelect = tocc
    showhideNodes = showhide
    #month = (dateStart.month + n_intervals - n_intervals_start) % 12
    #if (month == 0):
    #    month = 12
    #year = dateStart.year + mt.floor((dateStart.month + n_intervals - n_intervals_start) / 12) - 1
    #if (not (month == 12)):
    #    year += 1
    ctx = dash.callback_context
    if (not ctx.triggered and n_clicks1 == 0 and n_clicks2 == 0 and n_clicks3 == 0 and n_clicks4 == 0):
        if (isLive):
            #return dash.no_update, disableState, 'Animation status: active. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), False, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
            return dash.no_update, disableState, 'Animation status: paused. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), pauseDisabled, resumeDisabled, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
        else:
            return dash.no_update, disableState, 'Animation status: not active.', True, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
    else:
        btn_id = [b['prop_id'] for b in dash.callback_context.triggered][0]
        if 'play-button-state' in btn_id:
            endMonth = dateEnd.month
            endYear = dateEnd.year
            isLive = True
            disableState = False
            n_intervals_start = n_intervals
            month = dateStart.month
            year = dateStart.year
            pauseDisabled = False
            resumeDisabled = True
            if animationSpeedInit is None:
                animationSpeedInit = 3000
            return animationSpeedInit, disableState, 'Animation status: active. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), False, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
        elif 'pause-button-state' in btn_id:
            isLive = True
            disableState = True
            pauseDisabled = True
            resumeDisabled = False
            return dash.no_update, disableState, 'Animation status: paused. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), True, False, dash.no_update
        elif 'resume-button-state' in btn_id:
            isLive = True
            disableState = False
            if animationSpeedInit is None:
                animationSpeedInit = 3000
            pauseDisabled = False
            resumeDisabled = True
            return animationSpeedInit, disableState, 'Animation status: active. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), False, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
        elif 'submit-button-state' in btn_id:
            isLive = False
            disableState = True
            n_intervals_start = n_intervals
            pauseDisabled = True
            resumeDisabled = True
            return dash.no_update, disableState, 'Animation status: not active.', True, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)
        else:
            if isLive:
                month = month + 1
                if(month == 13):
                    month = 1
                    year = year + 1
                if ((year == endYear and month > endMonth) or year > endYear):
                    isLive = False
                    disableState = True
                    return dash.no_update, disableState, 'Animation status: finished. Timestamps: Year: ' + str(endYear) + ', Month: ' + str(endMonth), True, True, dash.no_update
                else:
                    return dash.no_update, disableState, 'Animation status: active. Timestamps: Year: ' + str(year) + ', Month: ' + str(month), False, True, nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange, dateStart, dateEnd, toccSelect, showhideNodes, isLive, month, year)


@app.callback(output=dash.dependencies.Output('fileDropDown', 'options'),       # This app callback makes sure the media folder is
              inputs=[dash.dependencies.Input('refreshDropDown', 'n_clicks')])  # updated when clicking the dataset dropdown menu
def change_my_dropdown_options(n_clicks):                                       # The newly uploaded files can now also be selected
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    options = [{'label': j, 'value': j} for j in os.listdir(settings.MEDIA_ROOT)]
    return options


@app.callback(
    Output('session', 'data'),
    Input('submit-button-state', 'n_clicks'),
    Input('play-button-state', 'n_clicks'),
    Input('pause-button-state', 'n_clicks'),
    Input('resume-button-state', 'n_clicks'),
    Input('interval-component', 'n_intervals'),
    State('session', 'data'))
def update_session_graph(n_clicks1, n_clicks2, n_clicks3, n_clicks4, data, n_intervals):
    graph = nlf.filteredGraph
    graph.remove_nodes_from(list(nx.isolates(nlf.filteredGraph)))
    matrix = to_numpy_matrix(graph).astype(int).tolist()

    # Store the edge data in a list
    edgeData = []
    for edge in graph.edges(data=True):
        edgeList = list(edge)
        edgeDict = without_keys(edgeList[2], {'fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle'})
        edgeDict['date'] = edgeDict['date'].strftime("%Y-%m-%d")
        edgeList[2] = edgeDict
        
        edgeData.append(edgeList)

    # Store the node data in a list
    nodeData = []
    for node in graph.nodes:
        nodeData.append({
            "id": node,
            "email": graph.nodes[node]['Email'],
            "job": graph.nodes[node]['Job']
        })

    # Finding the max matrix element for normalization
    maxMatrixElement = 0
    for row in matrix:
        for cell in row:
            if cell > maxMatrixElement:
                maxMatrixElement = cell
            
    matrixdict = {
        'matrix': matrix,
        'normMatrix': np.vectorize(vectorizedNormalizing)(matrix, 1, maxMatrixElement),
        'nodeData': nodeData,
        'edgeData': edgeData
    }

    data = matrixdict or {}
    return data


# Normalization mathematics
def vectorizedNormalizing(z, norm, max):
    # This can be any arbitrary mathematical function
    return norm * mt.log(1 + z, max + 1)

# List comprehension object key exclusion
def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}



if __name__ == '__main__':
    app.run_server(debug=True)
