from __future__ import print_function
import chromatic        #CPLEX models
import graphtools       #I/O of graphs etc.
import lego, cubes      #Some special graph classes
import math, sys, numpy

from graphtools import readDimacs       #Read Dimacs text format examples
from graphtools import bipRandom, randomGraph, bestGreedyChi
from lego import legoG, legoGP          #Soren's graphs G, Gprime
from cubes import Qdu, Qdus             #Cube-like graphs, see course lecture notes
from chromatic import standard, scheduling, binary    # ... and other models

# timelimit of 30 minutes on 8 threads
timeLimit = 60.0*30*1
threadLimit = 8
numpy.random.seed(12345)

testCases = {
    # Queen graphs
    "queen5_5": (readDimacs('data/queen5_5.col'), 5, timeLimit),
    "queen6_6": (readDimacs('data/queen6_6.col'), 8, timeLimit),
    "queen7_7": (readDimacs('data/queen7_7.col'), 10, timeLimit),
    "queen8_8": (readDimacs('data/queen8_8.col'), 11, timeLimit),
    "queen9_9": (readDimacs('data/queen9_9.col'), 13, timeLimit),
    "queen10_10": (readDimacs('data/queen10_10.col'), 14, timeLimit),
    "queen8_12": (readDimacs('data/queen8_12.col'), 14, timeLimit),
    # Mycielski graphs
    "myciel3": (readDimacs('data/myciel3.col'), 4, timeLimit),
    "myciel4": (readDimacs('data/myciel4.col'), 5, timeLimit),
    "myciel5": (readDimacs('data/myciel5.col'), 6, timeLimit),
    "myciel6": (readDimacs('data/myciel6.col'), 7, timeLimit),
    "myciel7": (readDimacs('data/myciel7.col'), 8, timeLimit),
    # Real application (register allocation) graphs (large chromatic numbers!)
    "reg1": (readDimacs('data/zeroin.i.1.col'), 50, timeLimit),
    "reg2": (readDimacs('data/zeroin.i.2.col'), 50, timeLimit),
    "reg3": (readDimacs('data/zeroin.i.3.col'), 50, timeLimit),
    "reg4": (readDimacs('data/mulsol.i.1.col'), 50, timeLimit),
    "reg5": (readDimacs('data/mulsol.i.2.col'), 50, timeLimit),
    # (Almost) real application - proximity graphs of US road network at various scales, V=128 always
    "miles250": (readDimacs('data/miles250.col'), 8, timeLimit),
    "miles500": (readDimacs('data/miles500.col'), 21, timeLimit),
    "miles750": (readDimacs('data/miles750.col'), 31, timeLimit),
    "miles1000": (readDimacs('data/miles1000.col'), 43, timeLimit),
    "miles1500": (readDimacs('data/miles1500.col'), 73, timeLimit),
    # Some of the LEGO graphs
    # G(2,2)
    "G_2_2_6_6": (legoG(2,2,6,6), 5, timeLimit),
    "G_2_2_8_8": (legoG(2,2,8,8), 8, timeLimit),    
    "G_2_2_9_10": (legoG(2,2,9,10), 8, timeLimit),
    "G_2_2_10_10": (legoG(2,2,10,10), 5, timeLimit),    
    # G(3,3)
    "G_3_3_6_6": (legoG(3,3,6,6), 7, timeLimit),
    "G_3_3_8_8": (legoG(3,3,8,8), 7, timeLimit),
    "G_3_3_10_10": (legoG(3,3,10,10), 7, timeLimit),    
    "G_3_3_12_12": (legoG(3,3,12,12), 7, timeLimit),    
    # G(1,2)                                    
    # For G(1,2) it is also interesting to ask directly if they are 4-colorable ! May be faster to decide    
    # And also to compare when upper bound is smaller
    "G_1_2_4_4": (legoG(1,2,4,4), 8, timeLimit),
    "G_1_2_4_6": (legoG(1,2,4,6), 8, timeLimit),
    "G_1_2_4_10": (legoG(1,2,4,10), 8, timeLimit),
    "G_1_2_4_12": (legoG(1,2,4,12), 8, timeLimit),
    "G_1_2_6_6": (legoG(1,2,6,6), 8, timeLimit),
    "G_1_2_6_10": (legoG(1,2,6,10), 8, timeLimit),
    "G_1_2_6_12": (legoG(1,2,6,12), 8, timeLimit),
    "G_1_2_8_12": (legoG(1,2,8,10), 8, timeLimit),    
    "G_1_2_10_10": (legoG(1,2,10,10), 5, timeLimit),        
    "G_1_2_10_12": (legoG(1,2,10,12), 8, timeLimit),        
    "G_1_2_12_12": (legoG(1,2,12,12), 8, timeLimit),        
    # Generalized cube graphs
    "Q_7_4": (Qdu(7,4), 9, timeLimit),          
    "Q_8_2": (Qdu(8,2), 10, timeLimit),          
    "Q_8_4": (Qdu(8,4), 10, timeLimit),          
    "Q_9_2": (Qdu(9,2), 20, timeLimit),		          
    "Q_9_4": (Qdu(9,4), 22, timeLimit),     
    "Q_10_4_3": (Qdus(10,4,3), 20, timeLimit),                      # Increase 28 if necessary - I'm not sure what the aswer is!. See when it finds something feasible
    "Q_10_4_5": (Qdus(10,4,5), 31, timeLimit),
    # Random bipartite graph
    "bip50": (bipRandom(50), 3, timeLimit),
    "bip200": (bipRandom(200), 3, timeLimit),
    "bip500": (bipRandom(500), 3, timeLimit),
	# Completely random small graphs, just to test if we get the same answer
	"random1": (randomGraph(30,0.1), 30, timeLimit),
    "random2": (randomGraph(30,0.2), 30, timeLimit),
    "random3": (randomGraph(30,0.3), 30, timeLimit),
    "random4": (randomGraph(30,0.4), 30, timeLimit),
    "random5": (randomGraph(30,0.5), 30, timeLimit),
    "random6": (randomGraph(30,0.6), 30, timeLimit),
    "random7": (randomGraph(30,0.7), 30, timeLimit),
    "random8": (randomGraph(30,0.8), 30, timeLimit),
    "random9": (randomGraph(30,0.9), 30, timeLimit),
	# Some random sparse graphs, to check if the "sparse" scheduling formulation does beter
    "sparse1": (randomGraph(100,0.1), 10, timeLimit),
    "sparse2": (randomGraph(200,0.08), 20, timeLimit),
    "sparse3": (randomGraph(300,0.06), 30, timeLimit),
    "sparse4": (randomGraph(400,0.04), 40, timeLimit),
}

# Get only tests whose name matches a substring
def getByName(str):
    return sorted([ name for name in testCases if str in name ])

# Format the number of seconds
def formatTime(t):
    if t<60:
        return '{0:.0f}s'.format(t)
    elif t<3600:
        return '{0:.1f}m'.format(t/60)
    else:
        return '{0:.1f}h'.format(t/3600)

# Format the lower bound
def formatLower(lower, status):
    if lower and lower>0:
        return int(math.ceil(lower-0.001))
    else:
        return '?'

# Format the upper bound
def formatUpper(obj, status):
    if obj and obj>=0:
        return int(obj)
    else:
        return '?'

# Run a particular group of tests
def runGroup(tests):
    allMethods = [standard]
    #allMethods = [standard, scheduling, binary]
    #allMethods = [standard, scheduling]
    #allMethods = [binary]
    for name in tests:
        case = testCases[name]
        graph = case[0]
        vert = len(graph)
        upper = case[1]
        timeLimit = case[2]
        greedy = bestGreedyChi(graph, 10)
        if greedy<upper:
            upper=greedy
        # I need to write results to a file
        output = '{0:<10} {1:<4} {2:<4}'.format(name, vert, greedy)
        for method in allMethods:
            print(name, method.__name__)
            lower, obj, status, elapsed = method(graph, upper, timeLimit, threadLimit)
            output += '  {0:<4} {1:<4} {2:<7}'.format(formatLower(lower, status), formatUpper(obj, status), formatTime(elapsed))
        print(output)
        with open('results-single/{0}'.format(name), 'a') as f:
            print(output, file=f)

# Main method
# 3 parallel processes
def main():
    import concurrent.futures as cofu
    with cofu.ProcessPoolExecutor(3) as pool:
        cache = []
        for name in getByName(sys.argv[1]):
            cache.append( pool.submit(runGroup, [name]) )
        cofu.wait(cache)

if __name__ == "__main__": main()