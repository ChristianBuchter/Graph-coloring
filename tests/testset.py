import chromatic        #CPLEX models
import graphtools       #I/O of graphs etc.
import lego, cubes      #Some special graph classes

from graphtools import readDimacs       #Read Dimacs text format examples
from graphtools import bipRandom, bestGreedyChi
from lego import legoG, legoGP          #Soren's graphs G, Gprime
from cubes import Qdu, Qdus             #Cube-like graphs, see course lecture notes
from chromatic import smartStatement    # ... and other models

# I set these globally, but they'd better be adjusted to specific examples
timeLimit = 100.0
ub = 10

testCases = {
    # Queen graphs
    "queen5_5": (readDimacs('data/queen5_5.col'), ub, timeLimit),
    "queen6_6": (readDimacs('data/queen6_6.col'), ub, timeLimit),
    "queen7_7": (readDimacs('data/queen7_7.col'), ub, timeLimit),
    "queen8_8": (readDimacs('data/queen8_8.col'), ub, timeLimit),
    "queen9_9": (readDimacs('data/queen9_9.col'), ub, timeLimit),
    "queen10_10": (readDimacs('data/queen10_10.col'), ub, timeLimit),
    "queen8_12": (readDimacs('data/queen8_12.col'), ub, timeLimit),
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
    "miles250": (readDimacs('data/miles250.col'), 10, timeLimit),
    "miles500": (readDimacs('data/miles500.col'), 30, timeLimit),
    "miles750": (readDimacs('data/miles750.col'), 35, timeLimit),
    "miles1000": (readDimacs('data/miles1000.col'), 48, timeLimit),
    "miles1500": (readDimacs('data/miles1500.col'), 100, timeLimit),
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
    "G_1_2_10_12": (legoG(1,2,10,12), 8, timeLimit),        
    "G_1_2_12_12": (legoG(1,2,12,12), 8, timeLimit),  
    # Generalized cube graphs
    "Q_7_4": (Qdu(7,4), 10, timeLimit),          
    "Q_8_2": (Qdu(8,2), 10, timeLimit),          
    "Q_8_4": (Qdu(8,4), 10, timeLimit),          
    "Q_9_2": (Qdu(9,2), 20, timeLimit),          
    "Q_9_4": (Qdu(9,4), 22, timeLimit),          
    "Q_10_4_3": (Qdus(10,4,3), 28, timeLimit),                      # Increase 28 if necessary - I'm not sure what the aswer is!. See when it finds something feasible
    "Q_10_4_5": (Qdus(10,4,5), 28, timeLimit),
    # Random bipartite graph
    "bip50": (bipRandom(50), 3, timeLimit),
    "bip200": (bipRandom(200), 3, timeLimit),
    "bip500": (bipRandom(500), 3, timeLimit),
}



results = {}

# Get only tests whose name matches a substring
def getByName(cases, str):
    return sorted([ name for name in testCases if str in name ])

# Go through all tests (or all tests in a group) and run them
# AHA: It would maybe be cool to also get the running time in case when it finished early i.e. before time limit
allTests = getByName(testCases, "")
allMethods = [smartStatement]

for name in allTests:
    case = testCases[name]
    graph = case[0]
    vert = len(graph)
    upper = case[1]
    timeLimit = case[2]
    for method in allMethods:
        print name, method.__name__
        obj, lower, status = method(graph, upper, timeLimit)
        results[(name, method.__name__)] = (vert, obj, lower, status, bestGreedyChi(graph, 10))

# Print results in a not too ugly way
print('=======================================================================')
for name in allTests:
    for method in allMethods:
        vert, obj, lower, status, greedy = results[(name, method.__name__)]
        print('{0:<10} (V={1:<4})  lb={2}, ub={3}, status={4}, greedy={5}'.format(name, vert, obj, lower if lower >= 0 else 'inf', status, greedy))

