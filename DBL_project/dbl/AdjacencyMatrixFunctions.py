from django.conf import settings  # Import settings to allow BASE_DIR to be used
import networkx as nx             # Handling network graphs
import plotly.graph_objs as go    # Graph drawing imports
import pandas as pd
from datetime import date
import plotly.figure_factory as ff
from networkx.convert_matrix import to_numpy_matrix
import numpy as np


# The overarching function that does all the graph creating
def createGraph(filename):
    # Read CSV and setup NX graph data structure
    #mailSet = pd.read_csv(settings.BASE_DIR / 'enron-v1.csv', engine='python')
    mailSet = pd.read_csv(settings.BASE_DIR / 'media/enron-jesse-mini.csv', engine='python')
    mailSet['date'] = pd.to_datetime(mailSet['date'])  # Filter the date for Dash
    mailSet['month'] = mailSet['date'].dt.month
    mailSet['year'] = mailSet['date'].dt.year

    # Generate graph from CSV information
    mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date', 'month', 'year'], create_using=nx.MultiDiGraph())
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

    return G, jobFrom_set, jobTo_set, mailFrom_set, mailTo_set, minDate, maxDate


def filterGraph(graph, sentimentValue, jobFromValue, jobToValue, mailFromValue, mailToValue, mailDateStart, mailDateEnd, toccSelect, showhide, isLive, month, year):
    global filteredGraph
    filteredGraph = graph.copy(as_view=False)
    mailDateStart = pd.to_datetime(mailDateStart)
    mailDateEnd = pd.to_datetime(mailDateEnd)

    # Remove the edges that don't satisfy the range
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
            flag = True
            if(edgeAttribute['toJobtitle'] in jobToValue):
                flag = False
        if(not flag and mailFromValue):
            flag = True
            if(edgeAttribute['fromEmail'] in mailFromValue):
                flag = False
        if(not flag and mailToValue):
            flag = True
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

    if(showhide == 'False'):
        for node in graph.nodes:
            if(filteredGraph.degree(node) == 0):
                filteredGraph.remove_node(node)

    return drawMatrix(filteredGraph)


def drawMatrix(filteredGraph):
    matrix = to_numpy_matrix(filteredGraph).astype(int).tolist()
    z = np.random.rand(5, 5)
    roundedz = z * 2 - 1

    # Drawing the graph as a figure
    cc = [[0, 'rgb(204, 102, 136)'], [0.5, 'rgb(45, 53, 60)'], [1, 'rgb(101, 204, 169)']]
    figure = ff.create_annotated_heatmap(matrix, colorscale=cc)
    return figure


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
