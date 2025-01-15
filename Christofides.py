import networkx as NX

def FindOddDegreeVertices(G):
    OddVertices = []
    
    for v, degree in G.degree():
        if degree % 2 == 1:
            OddVertices.append(v)
    
    return OddVertices

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

def Christofides(G):
    mst = NX.minimum_spanning_tree(G)
    
    OddVertices = FindOddDegreeVertices(mst)
    
    OddSubgraph = NX.subgraph(G, OddVertices)
    
    matching = NX.min_weight_matching(OddSubgraph, weight='weight')
    
    multigraph = NX.MultiGraph(mst)
    for u, v in matching:
        weight = G[u][v]['weight']
        multigraph.add_edge(u, v, weight=weight)

    EulerianCircuit = NX.eulerian_circuit(multigraph)
    
    TSPtour = EulerToHamilton(EulerianCircuit)
    
    cost = HamiltonCost(TSPtour, G)

    return TSPtour, cost
