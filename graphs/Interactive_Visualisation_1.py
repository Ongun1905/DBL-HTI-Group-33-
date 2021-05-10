# Import Node Link functions from another Python file
import NodeLinkFunctions as nlf

# Make sure you have plotly and networkx installed before running this code!
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from colour import Color
from datetime import date
from textwrap import dedent as d
import json
import math

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

input_file = "enron-v1.csv"

# Set up initial graph with positions and node attributes
vis1Graph, jobFrom, jobTo, mailFrom, mailTo, minDate, maxDate = nlf.createGraph(input_file)

dateStart = minDate 
dateEnd = maxDate

# Get external styles for the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialise Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
    html.Div(
        children = [
            html.Div(
                children = [
                    dcc.RangeSlider(
                        id='my-range-slider',
                        min=-1,
                        max=1,
                        step=0.01,
                        marks={
                        -1: {'label': ': Very Negative Email : - 1', 'style': {'color': '#f50'}},
                        0: {'label': '0: Neutral Email'},
                        1: {'label': '1: Very Positive Email', 'style': {'color': '#77b0b1'}},
                        },
                        value=[-1, 1],
                        allowCross=False,   
                    ),
                    html.Br(),#breaks space between the interactive elements
                    html.Br(),
                ],
                style = {'width': '400px'}
            ),
            
            html.Div(
                children = [
                    dcc.Dropdown(
                        id='jobFrom-dropdown',
                        options=[
                            {'label': j, 'value': j} for j in sorted(jobFrom)
                        ],
                        multi = True,
                        placeholder="Select from Job, Nothing = all"
                    ),

                    dcc.Dropdown(
                        id='jobTo-dropdown',
                        options=[
                            {'label': j, 'value': j} for j in sorted(jobTo)
                        ],
                        multi = True,
                        placeholder="Select to Job, Nothing = all"
                    ),
                ],
                style = {'width': '300px'}
            ),

            html.Div(
                children = [
                    dcc.Dropdown(
                        id='mailFrom-dropdown',
                        options=[
                            {'label': j, 'value': j} for j in sorted(mailFrom)
                        ],
                        multi = True,
                        placeholder="Select from Email, Nothing = all"
                    ),

                    dcc.Dropdown(
                        id='mailTo-dropdown',
                        options=[
                            {'label': j, 'value': j} for j in sorted(mailTo)
                        ],
                        multi = True,
                        placeholder="Select to Email, Nothing = all"
                    ),
                ],
                style = {'width': '300px'}
            ),

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
                        first_day_of_week = 2,
                        display_format='MMM Do, YYYY'
                ) 
            ),

            html.Div(
                dcc.Checklist(
                    id = 'to-cc-checklist',
                    options=[
                        {'label': 'TO', 'value': 'TO'},
                        {'label': 'CC', 'value': 'CC'}
                    ],
                    value=['TO', 'CC'],
                    labelStyle={'display': 'inline-block'}
                ) 
            ),

                html.Div(
                    dcc.RadioItems(
                    id = 'node-radio-items',
                    options=[
                        {'label': 'Show unlinked nodes', 'value': 'True'},
                        {'label': 'Hide unlinked nodes', 'value': 'False'}
                    ],
                    value='True',
                    labelStyle={'display': 'inline-block'}
                )
            )
        ]    
    ),

    html.Div(
        children=[dcc.Graph(id="mail-graph", 
        figure=nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange, mailFromRange, mailToRange,
                               dateStart, dateEnd, toccSelect, showhideNodes))]
    )
])

@app.callback(
     dash.dependencies.Output('mail-graph', 'figure'),
     [dash.dependencies.Input('my-range-slider', 'value'), 
      dash.dependencies.Input('jobFrom-dropdown', 'value'), 
      dash.dependencies.Input('jobTo-dropdown', 'value'), 
      dash.dependencies.Input('mailFrom-dropdown', 'value'), 
      dash.dependencies.Input('mailTo-dropdown', 'value'), 
      dash.dependencies.Input('mail-date-range', 'start_date'),
      dash.dependencies.Input('mail-date-range', 'end_date'),
      dash.dependencies.Input('to-cc-checklist', 'value'),
      dash.dependencies.Input('node-radio-items', 'value')])

def update_output(value, jobFromInput, jobToInput, mailFromInput, mailToInput, mailStartDate, mailEndDate, tocc, showhide):
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

if __name__ == '__main__':
    app.run_server(debug=True)