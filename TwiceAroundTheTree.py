import networkx as NX

def EulerToHamilton(EulerianEdges):
    VisitedVertices = []
    TSPtour = []

    for edge in EulerianEdges:
        u, v = edge
        if u not in VisitedVertices:
            TSPtour.append(u)
            VisitedVertices.append(u)
        if v not in VisitedVertices:
            TSPtour.append(v)
            VisitedVertices.append(v)

    if TSPtour[0] != TSPtour[-1]:
        TSPtour.append(TSPtour[0])
    
    return TSPtour

def HamiltonCost(TSPtour, graph):
    TotalCost = 0

    for i in range(len(TSPtour) - 1):
        u = TSPtour[i]
        v = TSPtour[i + 1]
        TotalCost += graph[u][v]['weight']
        
    return TotalCost

def TwiceAroundTheTree(graph):
    mst = NX.minimum_spanning_tree(graph)
    
    multigraph = NX.MultiGraph(mst)
    for u, v in mst.edges():
        weight = mst[u][v]['weight']
        multigraph.add_edge(u, v, weight=weight)

    EulerianCircuit = NX.eulerian_circuit(multigraph)

    TSPtour = EulerToHamilton(EulerianCircuit)
    
    cost = HamiltonCost(TSPtour, graph)

    return TSPtour, cost