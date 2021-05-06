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
from datetime import datetime
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

# Read CSV and setup NX graph data structure
mailSet = pd.read_csv("enron-v1.csv", engine='python')
mailSet['date'] = pd.to_datetime(mailSet['date']) # Filter the date for Dash

# Generate graph from CSV information
displayMultiEdges = True
mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = (nx.MultiDiGraph() if displayMultiEdges else nx.DiGraph()))

# Set up initial graph with positions and node attributes
vis1Graph = nlf.createGraph(mailGraph)


# Puts all values of the given `attribute` in the given list `list`
def getNodeAttributeValues(graph, attribute, list):
    j = 0
    for i in range(1, len(graph.nodes)):
        if graph.nodes[i][attribute] not in list:
            list.append(graph.nodes[i][attribute])
            j += 1

# Apply above function to find all possible jobs
jobOptions = []
getNodeAttributeValues(vis1Graph, "Job", jobOptions)

# Set up options checkboxes
jobOptionsSelect = []
jobOptionsNumbers = []
for i in range(len(jobOptions)):
    jobOptionsSelect.append({
        'label': jobOptions[i],
        'value': i
    })
    jobOptionsNumbers.append(i)


# Filter the graph
vis1GraphFilter1 = nlf.filterGraph(vis1Graph, "range", sentimentRange, None)
vis1GraphFiltered = nlf.filterGraph(vis1GraphFilter1, "checkbox", jobOptionsNumbers, jobOptions)

# Get external styles for the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialise Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Email Network"

# Generating Layout
app.layout = html.Div([
    dcc.RangeSlider(
        id='my-range-slider',
        min=-1,
        max=1,
        step=0.01,
        marks={
        -1: {'label': '-1: Very Negative Email', 'style': {'color': '#f50'}},
        0: {'label': '0: Neutral Email'},
        1: {'label': '1: Very Positive Email', 'style': {'color': '#77b0b1'}},
        },
        value=[-1, 1],
        allowCross=False
    ),
    dcc.Checklist(
        id='job-options-checklist',
        options=jobOptionsSelect,
        value=jobOptionsNumbers # Makes all job options be selected when ran
    ),
    #html.Div(id='output-container-range-slider'),
    html.Div(
        children=[dcc.Graph(id="mail-graph", figure=nlf.renderGraph(vis1GraphFiltered))]
    )
])

@app.callback(
    # Sentiment range slider input
    #dash.dependencies.Output('output-container-range-slider', 'children'),
    dash.dependencies.Output('mail-graph', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value')],
    
    # Job checkbox select input
    dash.dependencies.Input('job-options-checklist', 'value'),
)
def update_output(sentimentValue, jobChecklistValue):
    #return 'You have selected the sentiment interval {}'.format(value)
    originalGraph = vis1Graph
    filter_1 = nlf.filterGraph(originalGraph, "range", sentimentValue, None)
    filter_2 = nlf.filterGraph(filter_1, "checkbox", jobChecklistValue, jobOptions)
    return nlf.renderGraph(filter_2)

if __name__ == '__main__':
    app.run_server(debug=True)