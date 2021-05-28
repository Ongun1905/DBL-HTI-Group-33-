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

# -------------------------------------------------------
# Visualization 2
#
# This codes generates an adjacency matrix from the given
# data.
# -------------------------------------------------------

# Read CSV and setup NX graph data structure
#mailSet = pd.read_csv(settings.BASE_DIR / 'enron-v1.csv', engine='python')

#def getMultiMatrix():
 # mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph())
 # matrix = to_numpy_matrix(mailGraph).tolist()
 # return matrix

def getNormalizedMultiMatrix(norm):
 # mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph())
 # matrix = to_numpy_matrix(mailGraph).tolist()
 # G = mailGraph.copy()

  # Efficiently adding attributes to the nodes in the graph
  #for edge in G.edges:
   # edgeAttribute = G.get_edge_data(*edge)
   # if (edge[2] == 0):
    #  if(G.nodes[edge[0]].get('Email') is None):
     #   G.nodes[edge[0]]['Email'] = edgeAttribute['fromEmail']
      #  G.nodes[edge[0]]['Job'] = edgeAttribute['fromJobtitle']
      #if(G.nodes[edge[1]].get('Email') is None):
       # G.nodes[edge[1]]['Email'] = edgeAttribute['toEmail']
       # G.nodes[edge[1]]['Job'] = edgeAttribute['toJobtitle']
  matrix = to_numpy_matrix(nlf.filteredGraph).tolist()

  # Store the node info in a list
  nodeInfo = []
  for node in nlf.filteredGraph.nodes:
    nodeInfo.append({
      "id": node,
      "email": nlf.filteredGraph.nodes[node]['Email'],
      "job": nlf.filteredGraph.nodes[node]['Job']
    })

  # Return the numpy matrix and the nodes with their corresponding email and job
  return matrix, nodeInfo

def getNormalizedMultiMatrix(norm):
  mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph())
  matrix = to_numpy_matrix(mailGraph).tolist()

  # Finding the max matrix element for linear normalization
  maxMatrixElement = 0
  for row in matrix:
    for cell in row:
      if cell > maxMatrixElement:
        maxMatrixElement = cell
  
  # Linear normalization between 0 and norm
  # normalizedMatrix = np.multiply((norm / maxMatrixElement), matrix)

  # Logarithmic normalization between 0 and norm
  normalizedMatrix = np.vectorize(vectorizedNormalizing)(matrix, norm, maxMatrixElement)

  return normalizedMatrix

def getMatrix():
  mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.DiGraph())
  matrix = to_numpy_matrix(mailGraph).tolist()
  return matrix



# Normalization mathematics
def vectorizedNormalizing(z, norm, max):
  # This can be any arbitrary mathematical function
  return norm * math.log(1 + z, max + 1)
