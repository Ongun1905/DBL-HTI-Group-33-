# Make sure you have plotly and networkx installed before running this code!
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
import plotly.graph_objs as go # Graph drawing imports
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
SentimentRange = [-1, 1]

# Read CSV and setup NX graph data structure
mailSet = pd.read_csv("enron-v1.csv", engine='python')
mailSet['date'] = pd.to_datetime(mailSet['date']) # Filter the date for Dash

mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph())

# Generate random positions for the network nodes
# We can generate our own random positions pretty easily as follows:
random.seed(10)
dim = 2 # The amount of dimensions in which to generate random positions
# pos = {v: [random.gauss(0, 2) for i in range(dim)] for v in mailGraph.nodes}  # Gaussian position distribution
# pos = {v: [random.random() for i in range(dim)] for v in mailGraph.nodes}      # Standard position distribution

nf = len(mailGraph.nodes) / (2 * math.pi) # Normalization factor for normalizing the nodes to 2*pi (full circle)
pos = {v: [math.sin(v / nf), math.cos(v / nf)] for v in sorted(mailGraph.nodes)}    # Circular position distribution

# This "circular" distribution looks oval because of the automatic rescaling of Plotly's graph viewer. 
# To make this look actually circular, set the width and height to the same value.

# Efficiently adding attributes to the nodes in mailGraph
for edge in mailGraph.edges:

    edgeAttribute = mailGraph.get_edge_data(*edge)

    if(edge[2] == 0):
        if(mailGraph.nodes[edge[0]].get('Email') is None):
            mailGraph.nodes[edge[0]]['Email'] = edgeAttribute['fromEmail']
            mailGraph.nodes[edge[0]]['Job'] = edgeAttribute['fromJobtitle']
        if(mailGraph.nodes[edge[1]].get('Email') is None):
            mailGraph.nodes[edge[1]]['Email'] = edgeAttribute['toEmail']
            mailGraph.nodes[edge[1]]['Job'] = edgeAttribute['toJobtitle']

nx.set_node_attributes(mailGraph, pos, "pos")

# Define the function that will filter the graph according to the interactive choices

def graphFilter(G, SentimentRange):
    # Create a copy of mailGraph where edges that don't satisfy the chosen properties are removed
    mailGraphFiltered = G.copy(as_view=False)
    for edge in G.edges:
        edgeAttribute = G.get_edge_data(*edge)
        if(edgeAttribute['sentiment'] < SentimentRange[0] or edgeAttribute['sentiment'] > SentimentRange[1]):
            mailGraphFiltered.remove_edge(*edge)

    edge_x = []
    edge_y = []

    # Initializing positions
    for edge in mailGraphFiltered.edges:
        x0, y0 = mailGraphFiltered.nodes[edge[0]]['pos']
        x1, y1 = mailGraphFiltered.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Drawing edge lines
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='rgba(152, 152, 152, 0.5)'),
        hoverinfo='none',
        mode='lines')

    # Initializing node positions
    node_x = []
    node_y = []
    for node in mailGraphFiltered.nodes():
        x, y = mailGraphFiltered.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    # Drawing nodes
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=1))

    # Coloring nodes by the amount of neighbors and adding tooltips
    node_adjacencies = []
    node_text = []
    for index, adjacencies in enumerate(mailGraphFiltered.adjacency()):
        node, nbrdict = adjacencies
        node_adjacencies.append(len(nbrdict))
        node_text.append(
            'ID: ' + str(node) +
            '<br>Email: '+ mailGraphFiltered.nodes[node]["Email"] +
            '<br>Job: '+ mailGraphFiltered.nodes[node]["Job"] +
            '<br>Connections: ' + str(len(nbrdict))
        )

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # Drawing the graph as a figure
    figure = go.Figure(data=[edge_trace, node_trace],
        layout=go.Layout(
        title='Network Graph Visualisation',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    return figure

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
    #html.Div(id='output-container-range-slider'),
    html.Div(
        children=[dcc.Graph(id="mail-graph", figure=graphFilter(mailGraph, SentimentRange))]
    )
])

@app.callback(
    #dash.dependencies.Output('output-container-range-slider', 'children'),
    dash.dependencies.Output('mail-graph', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    SentimentRange = value
    #return 'You have selected the sentiment interval {}'.format(value)
    return graphFilter(mailGraph, SentimentRange)

if __name__ == '__main__':
    app.run_server(debug=True)