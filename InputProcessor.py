import networkx as NX
import math

def ReadGraphFromFile(FilePath):
    graph = NX.Graph()

    with open(FilePath, 'r') as f:
        lines = f.readlines()

        for k in range(len(lines)):
            if not lines[k].strip()[0].isdigit():
                continue

            VertexData = lines[k].split()
            VertexID = int(VertexData[0])
            x, y = int(VertexData[1]), int(VertexData[2])

            graph.add_node(VertexID, pos=(x, y))

    return graph

def CreateCompleteGraph(graph):
    for i in graph.nodes:
        for j in graph.nodes:
            if i != j:
                graph.add_edge(i, j)

    return graph

def EuclideanDistance(node1, node2):
    x1, y1 = node1['pos']
    x2, y2 = node2['pos']
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def CreateWeightedGraph(graph):
    WeightedGraph = NX.Graph()
    for u, v in graph.edges():
        weight = EuclideanDistance(graph.nodes[u], graph.nodes[v])
        WeightedGraph.add_edge(u, v, weight=weight)
    
    return WeightedGraph