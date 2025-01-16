import InputProcessor as IP
import TwiceAroundTheTree as TAT
import Christofides as CF
import sys
import time

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <input_file>")
        sys.exit(1)
    FilePath = sys.argv[1]

    graph = IP.ReadGraphFromFile(FilePath)
    CompleteGraph = IP.CreateCompleteGraph(graph)
    WeightedGraph = IP.CreateWeightedGraph(CompleteGraph)

    start = time.time()
    TATtour, TATcost = TAT.TwiceAroundTheTree(WeightedGraph)
    end = time.time()
    print("TAT cost: ", TATcost)
    print("TAT took: ", end - start, "seconds to run")

    start = time.time()
    CFcircuit, CFcost = CF.Christofides(WeightedGraph)
    end = time.time()
    print("Christofides cost: ", CFcost)
    print("Christofides took: ", end - start, "seconds to run")

if __name__ == "__main__":
    main()
