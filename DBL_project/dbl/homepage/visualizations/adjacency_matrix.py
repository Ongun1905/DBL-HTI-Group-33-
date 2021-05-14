# Import functions for adjacency matrices
from networkx.algorithms.clique import enumerate_all_cliques
from networkx.linalg.graphmatrix import adjacency_matrix
from networkx.readwrite.json_graph import adjacency
from networkx.convert_matrix import to_numpy_matrix
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
import numpy as np

# -------------------------------------------------------
# Visualization 2
#
# This codes generates an adjacency matrix from the given
# data.
# -------------------------------------------------------

# Read CSV and setup NX graph data structure
mailSet = pd.read_csv("enron-v1.csv", engine='python')

def getMultiMatrix():
  mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph())
  matrix = to_numpy_matrix(mailGraph).tolist()
  return matrix

def getNormalizedMultiMatrix(factor):
  mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph())
  matrix = to_numpy_matrix(mailGraph).tolist()
  

  maxMatrixElement = 0
  for row in matrix:
    for cell in row:
      if cell > maxMatrixElement:
        maxMatrixElement = cell
  
  normalized_matrix = np.multiply((factor / maxMatrixElement), matrix)
  return normalized_matrix

def getMatrix():
  mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.DiGraph())
  matrix = to_numpy_matrix(mailGraph).tolist()
  return matrix
