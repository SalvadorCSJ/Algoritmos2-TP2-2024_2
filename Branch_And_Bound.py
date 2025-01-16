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

    UnvisitedNodes = BoundsArray[~np.in1d(
        np.arange(1, len(BoundsArray) + 1), CurrentPath)]
    Total = np.sum(UnvisitedNodes)

    return math.ceil(Total / 2)


def SmallestEdgeWeight(G, v1, v2):
    MinEdge = math.inf
    for _, _, data in G.edges(v1, data=True):
        CurrentEdgeWeight = data['weight']

        if _ == v2:
            continue
        if CurrentEdgeWeight < MinEdge:
            MinEdge = CurrentEdgeWeight

    return MinEdge


def TwoSmallestEdges(G, v):
    MinEdgeWeight1 = math.inf
    MinEdgeWeight2 = math.inf

    for _, _, data in G.edges(v, data=True):
        CurrentEdgeWeight = data['weight']

        if CurrentEdgeWeight < MinEdgeWeight1:
            MinEdgeWeight2 = MinEdgeWeight1
            MinEdgeWeight1 = CurrentEdgeWeight
        elif CurrentEdgeWeight < MinEdgeWeight2:
            MinEdgeWeight2 = CurrentEdgeWeight

    return MinEdgeWeight1, MinEdgeWeight2


def UpdateBoundsAddEdge(BoundsArray, G, v1, v2, CurrentPath):
    CommonEdgeWeight = G[v1][v2]['weight']

    if v1 == CurrentPath[0]:
        MinEdgeWeight1 = SmallestEdgeWeight(G, v1, v2)
    else:
        index = int(np.where(CurrentPath == v1)[0])
        v0 = CurrentPath[index-1]
        MinEdgeWeight1 = G[v0][v1]['weight']

    BoundsArray[v1-1] = MinEdgeWeight1 + CommonEdgeWeight

    MinEdgeWeight2 = SmallestEdgeWeight(G, v2, v1)
    BoundsArray[v2-1] = MinEdgeWeight2 + CommonEdgeWeight


def UpdateBoundsRemoveEdge(BoundsArray, G, v1, v2, CurrentPath):
    if v1 == CurrentPath[0]:
        MinEdgeWeight1, MinEdgeWeight2 = TwoSmallestEdges(G, v1)
        BoundsArray[v1-1] = MinEdgeWeight1+MinEdgeWeight2
    else:
        index = int(np.where(CurrentPath == v1)[0])
        vertex0 = CurrentPath[index-1]
        MinEdgeWeight1 = G[vertex0][v1]['weight']

        MinEdgeWeight2 = SmallestEdgeWeight(G, v1, vertex0)
        BoundsArray[v1-1] = MinEdgeWeight1+MinEdgeWeight2

    MinEdgeWeight1, MinEdgeWeight2 = TwoSmallestEdges(G, v2)
    BoundsArray[v2-1] = MinEdgeWeight1+MinEdgeWeight2


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

            UpdateBoundsAddEdge(
                BoundsArray, G, CurrentPath[CurrentDepth - 1], v, CurrentPath)

            NewBound = BoundUnvisitedNodes(BoundsArray, CurrentPath)
            if NewCost + NewBound < BestCostSoFar:
                BestCostSoFar = BranchAndBoundRec(
                    G, BoundsArray, CurrentPath, NewCost, BestCostSoFar, VisitedNodes, CurrentDepth + 1)

            VisitedNodes[v-1] = False
            CurrentPath[CurrentDepth] = 0
            UpdateBoundsRemoveEdge(
                BoundsArray, G, CurrentPath[CurrentDepth-1], v, CurrentPath)

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