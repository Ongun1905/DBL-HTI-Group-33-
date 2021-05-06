import networkx as nx # Handling network graphs
import plotly.graph_objs as go # Graph drawing imports
import random
import math

displayMultiEdges = True

# The overarching function that does all the graph creating
def createGraph(graph):
    G = graph.copy()

    # Efficiently adding attributes to the nodes in the graph
    for edge in G.edges:        
        if (displayMultiEdges == False or edge[2] == 0):
            edgeAttribute = G.get_edge_data(*edge)

        if(G.nodes[edge[0]].get('Email') is None):
            G.nodes[edge[0]]['Email'] = edgeAttribute['fromEmail']
            G.nodes[edge[0]]['Job'] = edgeAttribute['fromJobtitle']
        if(G.nodes[edge[1]].get('Email') is None):
            G.nodes[edge[1]]['Email'] = edgeAttribute['toEmail']
            G.nodes[edge[1]]['Job'] = edgeAttribute['toJobtitle']
    
    generatePositions(G)

    return G


def filterGraph(graph, filterType, filterValue, props):
    # The `props` parameter is a so-called "overloading argument". That means that you can pass extra properties into the function that will end up in this `props` parameter.
    filteredGraph = graph.copy(as_view=False)

    if (filterType == 'checkbox'):
        # Remove the nodes that don't satisfy the selection
        nodesToRemove = []
        tickedBoxes = filterValue

        # Generate an array of numbers of length of job options
        allBoxes = []
        for i in range(len(props)):
            allBoxes.append(i)

        untickedBoxes = list(set(allBoxes) - set(tickedBoxes))

        # print("The ticked boxes are " + str(tickedBoxes))
        print("Removing nodes with jobs in the list " + str(untickedBoxes))

        for node in filteredGraph.nodes:
            # Check every node. If the node has a job that shouldn't be in the graph, remove it.
            # `props` contains an array with all possible job options (text)
            for box in untickedBoxes:
                if (filteredGraph.nodes[node]["Job"] == props[box]):
                    nodesToRemove.append(node)

        for node in nodesToRemove:
            filteredGraph.remove_node(node)

        return filteredGraph

    elif (filterType == 'range'):
        # Remove the edges that don't satisfy the range
        print("Filtering graph to fit sentiment of " + str(filterValue))
        for edge in graph.edges:
            edgeAttribute = graph.get_edge_data(*edge)
            if(edgeAttribute['sentiment'] < filterValue[0] or edgeAttribute['sentiment'] > filterValue[1]):
                filteredGraph.remove_edge(*edge)
    
    return filteredGraph


def renderGraph(graph):
    return generateGraphElements(graph)


# Generate random positions for the network nodes
def generatePositions(graph):
    random.seed(10)

    # Random position distributions
    # pos = {v: [random.gauss(0, 2), random.gauss(0, 2)] for v in graph.nodes}     # Gaussian position distribution
    # pos = {v: [random.random(), random.random()] for v in graph.nodes}           # Standard position distribution

    # Calculated position distribution
    nf = len(graph.nodes) / (2 * math.pi) # Normalization factor for normalizing the nodes to 2*pi (full circle)
    pos = {v: [math.sin(v / nf), math.cos(v / nf)] for v in sorted(graph.nodes)}   # Circular position distribution

    nx.set_node_attributes(graph, pos, "pos")


# Generate visual elements like nodes, edges and hover popups and return the figure
def generateGraphElements(G):
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