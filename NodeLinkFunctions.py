# Import settings to allow BASE_DIR to be used
from django.conf import settings

import networkx as nx # Handling network graphs
import plotly.graph_objs as go # Graph drawing imports
import pandas as pd
import random
import math
from datetime import date
import datetime as dt


# The overarching function that does all the graph creating
def createGraph(filename):
    # Read CSV and setup NX graph data structure
    mailSet = pd.read_csv(settings.BASE_DIR / 'media' / str(filename), engine='python')
    mailSet['date'] = pd.to_datetime(mailSet['date']) # Filter the date for Dash
    mailSet['month'] = mailSet['date'].dt.month
    mailSet['year'] = mailSet['date'].dt.year

    # Generate graph from CSV information
    mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date', 'month', 'year'], create_using = nx.MultiDiGraph() )
    G = mailGraph.copy()

    jobFrom_set = []
    jobTo_set = []
    mailFrom_set = []
    mailTo_set = []
    minDate = date.max
    maxDate = date.min


    # Efficiently adding attributes to the nodes in the graph
    for edge in G.edges:    
        edgeAttribute = G.get_edge_data(*edge)
        if(edgeAttribute['date'] < minDate):
            minDate = edgeAttribute['date']
        if(edgeAttribute['date'] > maxDate):
            maxDate = edgeAttribute['date']  
        if (edge[2] == 0):
            if(G.nodes[edge[0]].get('Email') is None):
                G.nodes[edge[0]]['Email'] = edgeAttribute['fromEmail']
                G.nodes[edge[0]]['Job'] = edgeAttribute['fromJobtitle']
            if(G.nodes[edge[1]].get('Email') is None):
                G.nodes[edge[1]]['Email'] = edgeAttribute['toEmail']
                G.nodes[edge[1]]['Job'] = edgeAttribute['toJobtitle']
            if(edgeAttribute['fromJobtitle'] not in jobFrom_set):
                jobFrom_set = jobFrom_set + [edgeAttribute['fromJobtitle']]
            if(edgeAttribute['toJobtitle'] not in jobTo_set):
                jobTo_set = jobTo_set + [edgeAttribute['toJobtitle']]
            if(edgeAttribute['fromEmail'] not in mailFrom_set):
                mailFrom_set = mailFrom_set + [edgeAttribute['fromEmail']]
            if(edgeAttribute['toEmail'] not in mailTo_set):
                mailTo_set = mailTo_set + [edgeAttribute['toEmail']]
    
    generatePositions(G)

    return G, jobFrom_set, jobTo_set, mailFrom_set, mailTo_set, minDate, maxDate;


def filterGraph(graph, sentimentValue, jobFromValue, jobToValue, mailFromValue, mailToValue, mailDateStart, mailDateEnd, toccSelect, showhide, isLive, month, year):
    # This global variable will be used as a data structure for both the graph and the matrix as well
    global filteredGraph
    filteredGraph = graph.copy(as_view=False)
    mailDateStart = pd.to_datetime(mailDateStart)
    mailDateEnd = pd.to_datetime(mailDateEnd)

    # Remove the edges that don't satisfy the filters
    for edge in graph.edges:
        edgeAttribute = graph.get_edge_data(*edge)
        flag = False
        if(edgeAttribute['sentiment'] < sentimentValue[0] or edgeAttribute['sentiment'] > sentimentValue[1]):
            flag = True
        if(not flag and jobFromValue):
            flag = True
            if(edgeAttribute['fromJobtitle'] in jobFromValue):
                flag = False
        if(not flag and jobToValue):
            flag  = True
            if(edgeAttribute['toJobtitle'] in jobToValue):
                flag = False
        if(not flag and mailFromValue):
            flag = True
            if(edgeAttribute['fromEmail'] in mailFromValue):
                flag = False
        if(not flag and mailToValue):
            flag  = True
            if(edgeAttribute['toEmail'] in mailToValue):
                flag = False
        if (isLive == True):
            if(not (edgeAttribute['month'] == month and edgeAttribute['year'] == year)):
                flag = True
        else:
            if(edgeAttribute['date'] < mailDateStart or edgeAttribute['date'] > mailDateEnd):
                flag = True
        if(not flag and toccSelect):
            flag = True
            if(edgeAttribute['messageType'] in toccSelect):
                flag = False
        if(flag):
            filteredGraph.remove_edge(*edge)
    
    # Remove the nodes if the hiding option was chosen
    if(showhide == 'False'):
        for node in graph.nodes:
            if(filteredGraph.degree(node) == 0):
                filteredGraph.remove_node(node)

    return drawGraph(filteredGraph)

def drawGraph(filteredGraph):

    edge_x = []
    edge_y = []

    # Initializing positions
    for edge in filteredGraph.edges:
        x0, y0 = filteredGraph.nodes[edge[0]]['pos']
        x1, y1 = filteredGraph.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Drawing edge lines
    edge_trace = go.Scattergl(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='rgba(152, 152, 152, 0.5)'),
        hoverinfo='none',
        mode='lines')

    # Initializing node positions
    node_x = []
    node_y = []
    for node in filteredGraph.nodes():
        x, y = filteredGraph.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    # Drawing nodes
    node_trace = go.Scattergl(
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
    for index, adjacencies in enumerate(filteredGraph.adjacency()):
        node, nbrdict = adjacencies
        node_adjacencies.append(len(nbrdict))
        node_text.append(
            'ID: ' + str(node) +
            '<br>Email: '+ filteredGraph.nodes[node]["Email"] +
            '<br>Job: '+ filteredGraph.nodes[node]["Job"] +
            '<br>Connections: ' + str(len(nbrdict))
        )

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # Drawing the graph as a figure
    figure = go.Figure(data=[node_trace, edge_trace],
        layout=go.Layout(
        title='Network Graph Visualisation',
        titlefont_size=16,
        height=600,
        plot_bgcolor='#363F48',
        paper_bgcolor='#363F48',
        font_color='#65cca9',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    figure.update_layout(clickmode = 'event+select')#on click the selected node is highlighted
    return figure


# Generate random positions for the network nodes
def generatePositions(graph):
    random.seed(10)

    # Calculated position distribution
    nf = len(graph.nodes) / (2 * math.pi) # Normalization factor for normalizing the nodes to 2*pi (full circle)
    pos = {v: [math.sin(v / nf), math.cos(v / nf)] for v in sorted(graph.nodes)}   # Circular position distribution

    nx.set_node_attributes(graph, pos, "pos")
    
    
#Select a certain node and highlight its edges
def update_point(nodes, figure):
    c = list(nodes.marker.color)
    #s = list(nodes.marker.size)
    for i in nodes.point_inds:
        c[i] = '#bae2be'
       # s[i] = 20
        with figure.batch_update():
            nodes.marker.color = c
            #nodes.marker.size = s
