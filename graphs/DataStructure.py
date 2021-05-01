import pandas as pd
import networkx as nx 

mailSet = pd.read_csv("enron-v1.csv")

mailGraph = nx.from_pandas_edgelist(mailSet, 'fromId', 'toId', ['fromEmail', 'fromJobtitle', 'toEmail', 'toJobtitle', 'messageType', 'sentiment', 'date'], create_using = nx.MultiDiGraph())

for edge in mailGraph.edges:
    #print(edge)
    edgeAttribute = mailGraph.get_edge_data(*edge)
    #print(edgeAttribute)
    if(edge[2] == 0):
        if(mailGraph.nodes[edge[0]].get('Email') is None):
            mailGraph.nodes[edge[0]]['Email'] = edgeAttribute['fromEmail']
            mailGraph.nodes[edge[0]]['Job'] = edgeAttribute['fromJobtitle']
        if(mailGraph.nodes[edge[1]].get('Email') is None):
            mailGraph.nodes[edge[1]]['Email'] = edgeAttribute['toEmail']
            mailGraph.nodes[edge[1]]['Job'] = edgeAttribute['toJobtitle']

#print(mailGraph.nodes(data=True))

#numberofNodes = mailGraph.number_of_nodes()
#for node in mailGraph.nodes:
    #print(node, mailGraph.nodes[node]["Email"], mailGraph.nodes[node]["Job"])
