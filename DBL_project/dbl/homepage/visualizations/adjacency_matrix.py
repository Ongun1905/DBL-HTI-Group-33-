# Import functions for adjacency matrices
from networkx.linalg.graphmatrix import adjacency_matrix
from networkx.readwrite.json_graph import adjacency
from networkx.convert_matrix import to_numpy_matrix
import pandas as pd # General data handling
import networkx as nx # Handling network graphs
from colour import Color
from datetime import datetime
from textwrap import dedent as d
import json
import math

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
  return to_numpy_matrix(mailGraph)

def getMatrix():
  mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.DiGraph())
  return to_numpy_matrix(mailGraph)
