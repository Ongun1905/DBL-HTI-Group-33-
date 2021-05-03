import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go
import pandas as pd
from colour import Color
from datetime import datetime
from textwrap import dedent as d
import json

mailSet = pd.read_csv("graphs/enron-v1.csv")

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Email Network"

app.layout = html.Div([
    dcc.RangeSlider(
        id='my-range-slider',
        min=-1,
        max=1,
        step=0.01,
        marks={
        -1: {'label': '-1: Very Negative Email', 'style': {'color': '#f50'}},
        0: {'label': '0: Neutral Email'},
        1: {'label': '1: Very Positive Email', 'style': {'color': '#77b0b1'}},
        },
        value=[0, 0],
        allowCross=False
    ),
    html.Div(id='output-container-range-slider')
])


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected the sentiment interval {}'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
