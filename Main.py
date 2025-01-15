import InputProcessor as IP
import TwiceAroundTheTree as TAT
import Christofides as CF
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <input_file>")
        sys.exit(1)
    FilePath = sys.argv[1]

    graph = IP.ReadGraphFromFile(FilePath)
    CompleteGraph = IP.CreateCompleteGraph(graph)
    WeightedGraph = IP.CreateWeightedGraph(CompleteGraph)

    TATtour, TATcost = TAT.TwiceAroundTheTree(WeightedGraph)
    print("TAT cost:", TATcost)

    CFcircuit, CFcost = CF.Christofides(WeightedGraph)
    print("Christofides cost: ", CFcost)

if __name__ == "__main__":
    main()