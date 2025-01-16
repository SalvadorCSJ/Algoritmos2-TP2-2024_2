import math
import numpy as np

def StartingBoundsAllNodes(G):
    BoundsArray = np.zeros(len(G.nodes), dtype=float)

    for V in G.nodes:
        AdjacentEdges = G.edges(V, data=True)

        if len(AdjacentEdges) < 2:
            continue

        MinWeight1 = math.inf
        MinWeight2 = math.inf

        for u, v, data in AdjacentEdges:
            CurrentEdgeWeight = data['weight']

            if CurrentEdgeWeight < MinWeight1:
                MinWeight2 = MinWeight1
                MinWeight1 = CurrentEdgeWeight
            elif CurrentEdgeWeight < MinWeight2:
                MinWeight2 = CurrentEdgeWeight

        BoundsArray[V-1] = MinWeight1 + MinWeight2

    return BoundsArray


def BoundUnvisitedNodes(BoundsArray, CurrentPath):

    UnvisitedNodes = BoundsArray[~np.in1d(np.arange(1, len(BoundsArray) + 1), CurrentPath)]
    Total = np.sum(UnvisitedNodes)

    return math.ceil(Total / 2)


def BranchAndBoundRec(G, BoundsArray, CurrentPath, CurrentCost, BestCostSoFar, VisitedNodes, CurrentDepth=0):
    if CurrentDepth == len(G.nodes):
        PreviousNode = CurrentPath[CurrentDepth - 1]
        FirstNode = CurrentPath[0]
        CurrentCost += G[PreviousNode][FirstNode]['weight']
        BestCostSoFar = min(BestCostSoFar, CurrentCost)
        return BestCostSoFar

    for v in G.nodes:
        if not VisitedNodes[v-1]:
            CurrentPath[CurrentDepth] = v
            VisitedNodes[v-1] = True

            PreviousNode = CurrentPath[CurrentDepth - 1]
            NewCost = CurrentCost + G[PreviousNode][v]['weight']

            NewBound = BoundUnvisitedNodes(BoundsArray, CurrentPath)
            if NewCost + NewBound < BestCostSoFar:
                BestCostSoFar = BranchAndBoundRec(G, BoundsArray, CurrentPath, NewCost, BestCostSoFar, VisitedNodes, CurrentDepth + 1)

            VisitedNodes[v-1] = False
            CurrentPath[CurrentDepth] = 0

    return BestCostSoFar

def BranchAndBoundTSP(G, ChristofidesCost):
    BoundsArray = StartingBoundsAllNodes(G)
    
    BestCost = ChristofidesCost
    VisitedNodes = np.zeros(len(G.nodes), dtype=bool)
    
    CurrentPath = np.zeros(len(G.nodes) + 1, dtype=int)
    CurrentPath[0] = 1
    VisitedNodes[0] = True

    BestCost = BranchAndBoundRec(G, BoundsArray, CurrentPath, 0, BestCost, VisitedNodes, 1)
    
    return BestCost
