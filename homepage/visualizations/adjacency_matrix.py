# Import functions for adjacency matrices
from networkx.convert_matrix import to_numpy_matrix
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
import numpy as np
import math
import NodeLinkFunctions as nlf
from datetime import datetime

# -------------------------------------------------------
# Visualization 2
#
# This file contains functions to generate the adjacency
# matrix in the required format for the Django template.
# -------------------------------------------------------
def getMultiMatrix():
  """
  Returns the adjacency matrix of the filteredGraph. The cells contain
  the amount of edges between the two nodes.
  """
  graph = nlf.filteredGraph
  graph.remove_nodes_from(list(nx.isolates(nlf.filteredGraph)))
  matrix = to_numpy_matrix(graph).astype(int).tolist()
  edgeData = []

  for edge in graph.edges(data=True):
    edgeList = list(edge)
    edgeDict = without_keys(edgeList[2], {'fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle'})
    edgeDict['date'] = edgeDict['date'].strftime("%Y-%m-%d")
    edgeList[2] = edgeDict
    
    edgeData.append(edgeList)

  # Store the node info in a list
  nodeInfo = []
  for node in graph.nodes:
    nodeInfo.append({
        "id": node,
        "email": graph.nodes[node]['Email'],
        "job": graph.nodes[node]['Job']
    })

  # Return the numpy matrix and the nodes with their corresponding email and job
  return matrix, nodeInfo, edgeData


def getNormalizedMultiMatrix(norm):
  """
  Returns a normalized form of the matrix where the amount of edges are
  are normalized between 0 and the given `norm`. The maximum value in
  the matrix will be mapped to the `norm`.
  """
  graph = nlf.filteredGraph
  graph.remove_nodes_from(list(nx.isolates(nlf.filteredGraph)))
  matrix = to_numpy_matrix(graph).astype(int).tolist()

  # Finding the max matrix element for normalization
  maxMatrixElement = 0
  for row in matrix:
    for cell in row:
      if cell > maxMatrixElement:
        maxMatrixElement = cell

  # Logarithmic normalization between 0 and norm
  if (len(matrix) > 0):
    normalizedMatrix = np.vectorize(logarithmicNormalizing)(matrix, norm, maxMatrixElement)
    print('Normalized matrix: ' + str(len(normalizedMatrix)))
    return normalizedMatrix
  else:
    return []


def getSentimentMultiMatrix(norm):
  """
  Returns a normalized form of the matrix where the amount of edges are
  are normalized between 0 and the given `norm`.
  Returns a normalized form of the matrix where the average sentiment
  of the edges represented by the cell are normalized cubically between
  -1 and 1.
  """
  graph = nlf.filteredGraph
  graph.remove_nodes_from(list(nx.isolates(nlf.filteredGraph)))
  matrix = to_numpy_matrix(graph).astype(int).tolist()

  # Initialize variables
  sentimentMatrix = []
  maxSentiment = 0

  for rIdx, row in enumerate(matrix):
    # Initialize variables
    cellArr = []

    for cIdx, cell in enumerate(row):
      # Get all single_edge_data here
      total_sentiment = 0

      # Edge is of structure (u, v) where u is the sender (row) and v the receiver (column)
      u = list(graph.nodes)[rIdx]
      v = list(graph.nodes)[cIdx]

      # Get all edge data between two nodes.
      edge_data = graph.get_edge_data(u, v)

      if (not edge_data):
        # This node-pair had 0 edges. Add an empty array to the array of cells in a row
        cellArr.append(0)
      else:
        # `edge_data` is a dictionary with the edge data of all edges between `u` and `v`.
        # Loop over it to find the sentiment per edge and calculate the average sentiment.
        for single_edge_data in edge_data:
          total_sentiment += edge_data[single_edge_data].get('sentiment')

        averageEdgeSentiment = total_sentiment / len(edge_data)
        normalizedAverageSentiment = cuberoot(norm * (averageEdgeSentiment))
        
        cellArr.append(normalizedAverageSentiment)
    
    sentimentMatrix.append(cellArr)
  
  return sentimentMatrix


# Normalization mathematics
def logarithmicNormalizing(z, norm, max):
  """
  Normalizes the input matrix based on a logarithmic equation
  `z`: the current matrix element
  `norm`: the maximum output of the function
  `max`: the largest input value in the matrix, the value to be mapped to `norm`
  :return: np.vectorize argument
  """
  return norm * math.log(1 + abs(z), max + 1)


def cubicNormalizing(z, norm, max):
  """
  Normalizes the input matrix based on a cubic equation
  `z`: the current matrix element
  `norm`: the maximum output of the function
  `max`: the largest input value in the matrix, the value to be mapped to `norm`
  :return: np.vectorize argument
  """
  return norm * (1 / max * z) ** (1/3)


# Calculate the cube root of a number for normalization
def cuberoot(x):
  if x >= 0:
    return x**(1/3)
  elif x < 0:
    return -(abs(x)**(1/3))


# List comprehension dictionary key exclusion
def without_keys(d, keys):
  return {x: d[x] for x in d if x not in keys}
