# Import settings to allow BASE_DIR to be used
from django.conf import settings

# Import Node Link functions from another Python file
import NodeLinkFunctions as nlf

# Make sure you have plotly and networkx installed before running this code!
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
import dash
import dash_core_components as dcc
import dash_html_components as html

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

# Read CSV and setup NX graph data structure
mailSet = pd.read_csv(settings.BASE_DIR / 'enron-v1.csv', engine='python')
mailSet['date'] = pd.to_datetime(mailSet['date']) # Filter the date for Dash

# Generate graph from CSV information
mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph() )

# Set up initial graph with positions and node attributes
vis1Graph, jobFrom, jobTo = nlf.createGraph(mailGraph)


# Filter the graph
#vis1GraphFilter = nlf.filterGraph(vis1Graph, sentimentRange)

# Get external styles for the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialise Dash app
from django_plotly_dash import DjangoDash
app = DjangoDash('SimpleExample')
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
    #html.Div(id='output-container-range-slider'),
    html.Div(
        children=[dcc.Graph(id="mail-graph", figure=nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange))]
    )
])

@app.callback(
    # Sentiment range slider input
    #dash.dependencies.Output('output-container-range-slider', 'children'),
    dash.dependencies.Output('mail-graph', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value'), dash.dependencies.Input('jobFrom-dropdown', 'value'), dash.dependencies.Input('jobTo-dropdown', 'value')]
)
def update_output(value, jobFromInput, jobToInput):
    #return 'You have selected the sentiment interval {}'.format(value)
    sentimentRange = value
    jobFromRange = jobFromInput
    jobToRange = jobToInput
    return nlf.filterGraph(vis1Graph, sentimentRange, jobFromRange, jobToRange)

