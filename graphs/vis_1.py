# Make sure you have plotly and networkx installed before running this code!
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
import plotly.graph_objs as go # Graph drawing imports
import random

# ------------------------------------------------------------
# Visualisation 1
#
# This codes generates a graph for the first visualization. At
# this point in time, that visualisation is a network graph
# with randomly positioned nodes.
# ------------------------------------------------------------

# Functions
def random_geometric_directed_network_graph(n, dim=2, pos=None, seed=None):
    """Returns a random geometric directed network graph in the unit cube
    of dimensions `dim`.

    Parameters
    ----------
    n : int or iterable
        Number of nodes or iterable of nodes
    dim : int, optional
        Dimension of graph
    pos : dict, optional
        A dictionary keyed by node with node positions as values.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    Graph
        A random geometric graph, undirected and without self-loops.
        Each node has a node attribute ``'pos'`` that stores the
        position of that node in Euclidean space as provided by the
        ``pos`` keyword argument or, if ``pos`` was not provided, as
        generated by this function.

    """
    nodes = n
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    
    # If no positions are provided, choose uniformly random vectors in
    # Euclidean space of the specified dimension.
    
    if pos is None:
        random.seed(seed)
        pos = {v: [random.random() for i in range(dim)] for v in nodes}
    
    nx.set_node_attributes(G, pos, "pos")

    return G


# Read CSV and setup NX graph
mailSet = pd.read_csv(r"graphs/enron-v1.csv", engine='python')

mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph())

# [DEBUG] Printing the emails from a certain ID in a dataframe
employeeId = 90
mailsFromId = mailSet.loc[mailSet['fromId'] == employeeId]
uniqueMailsFromId = mailsFromId.drop_duplicates('toId')
print(uniqueMailsFromId)
print("Employee " + str(employeeId) + " has emailed to " + str(uniqueMailsFromId['fromId'].size) + " unique collegues.")

# Generate random positions for the network nodes
# We can generate our own random positions pretty easily as follows:
random.seed(10)
dim = 2 # The amount of dimensions in which to generate random positions
#pos = {v: [random.gauss(0, 2) for i in range(dim)] for v in mailGraph.nodes}  # Gaussian position distribution
pos = {v: [random.random() for i in range(dim)] for v in mailGraph.nodes}      # Standard position distribution

# Create a graph with the given nodes at random positions
G = random_geometric_directed_network_graph(mailGraph.nodes, pos=pos, seed=10)



# Adding the edges from our mailGraph into the rendered graph G and initializing edge information
for edge in mailGraph.edges:
    G.add_edge(edge[0], edge[1])
    
    edgeAttribute = mailGraph.get_edge_data(*edge)
    
    if(edge[2] == 0):
        if(G.nodes[edge[0]].get('Email') is None):
            G.nodes[edge[0]]['Email'] = edgeAttribute['fromEmail']
            G.nodes[edge[0]]['Job'] = edgeAttribute['fromJobtitle']
        if(G.nodes[edge[1]].get('Email') is None):
            G.nodes[edge[1]]['Email'] = edgeAttribute['toEmail']
            G.nodes[edge[1]]['Job'] = edgeAttribute['toJobtitle']

edge_x = []
edge_y = []

# Initializing positions
for edge in G.edges:
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
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
for node in G.nodes():
    x, y = G.nodes[node]['pos']
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
for index, adjacencies in enumerate(G.adjacency()):
    node, nbrdict = adjacencies
    node_adjacencies.append(len(nbrdict))
    node_text.append(
        'ID: ' + str(node) +
        '<br>Email: '+ G.nodes[node]["Email"] +
        '<br>Job: '+ G.nodes[node]["Job"] +
        '<br>Connections: ' + str(len(nbrdict))
    )

node_trace.marker.color = node_adjacencies
node_trace.text = node_text



# Drawing the graph as a figure
fig = go.Figure(data=[edge_trace, node_trace],
    layout=go.Layout(
    title='Network graph testing using Plotly',
    titlefont_size=16,
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20,l=5,r=5,t=40),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
)
fig.show()