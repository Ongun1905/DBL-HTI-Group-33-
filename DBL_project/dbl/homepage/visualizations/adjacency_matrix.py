# Import settings to allow BASE_DIR to be used
from typing import Generator
from django.conf import settings

# Import functions for adjacency matrices
from networkx.algorithms.clique import enumerate_all_cliques
from networkx.linalg.graphmatrix import adjacency_matrix
from networkx.readwrite.json_graph import adjacency
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
# This codes generates an adjacency matrix from the given
# data.
# -------------------------------------------------------

# Read CSV and setup NX graph data structure
#mailSet = pd.read_csv(settings.BASE_DIR / 'enron-v1.csv', engine='python')

def getMultiMatrix():
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


# Get a normalized form of the matrix where the amount of edges
# are normalized between 0 and the given `norm`.
def getNormalizedMultiMatrix(norm):
  graph = nlf.filteredGraph
  graph.remove_nodes_from(list(nx.isolates(nlf.filteredGraph)))
  matrix = to_numpy_matrix(graph).astype(int).tolist()

  # Finding the max matrix element for normalization
  maxMatrixElement = 0
  for row in matrix:
    for cell in row:
      if cell > maxMatrixElement:
        maxMatrixElement = cell
  
  # Linear normalization between 0 and norm
  # normalizedMatrix = np.multiply((norm / maxMatrixElement), matrix)

  # Logarithmic normalization between 0 and norm
  print(len(matrix))
  if (len(matrix) > 0):
    normalizedMatrix = np.vectorize(vectorizedNormalizing)(matrix, norm, maxMatrixElement)
    return normalizedMatrix
  else:
    return []



# Normalization mathematics
def vectorizedNormalizing(z, norm, max):
  # This can be any arbitrary mathematical function
  return norm * math.log(1 + z, max + 1)

# List comprehension object key exclusion
def without_keys(d, keys):
  return {x: d[x] for x in d if x not in keys}
