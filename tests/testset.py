from __future__ import print_function
import chromatic        #CPLEX models
import graphtools       #I/O of graphs etc.
import lego, cubes      #Some special graph classes

from graphtools import readDimacs       #Read Dimacs text format examples
from graphtools import bipRandom, bestGreedyChi
from lego import legoG, legoGP          #Soren's graphs G, Gprime
from cubes import Qdu, Qdus             #Cube-like graphs, see course lecture notes
from chromatic import standard, scheduling, binary    # ... and other models

# I set these globally, but they'd better be adjusted to specific examples
timeLimit = 3600.0
threadLimit = 10

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
}



results = {}

# Get only tests whose name matches a substring
def getByName(cases, str):
    return sorted([ name for name in testCases if str in name ])

# Go through all tests (or all tests in a group) and run them
# AHA: It would maybe be cool to also get the running time in case when it finished early i.e. before time limit
allTests = getByName(testCases, "")
allMethods = [standard, scheduling, binary]

for name in allTests:
    case = testCases[name]
    graph = case[0]
    vert = len(graph)
    upper = case[1]
    timeLimit = case[2]
    for method in allMethods:
        print (name, method.__name__)
        lower, obj, status, elapsed = method(graph, upper, timeLimit, threadLimit)
        results[(name, method.__name__)] = (vert, lower, obj, status, elapsed, bestGreedyChi(graph, 10))

# Print results in a not too ugly way
with open('results/results.txt', 'w') as f:
	print('=======================================================================', file=f)
	for name in allTests:
		for method in allMethods:
			vert, lower, obj, status, elapsed, greedy = results[(name, method.__name__)]
			print('{0:<10} (V={1:<4}) ,{2}:  lb={3}, ub={4}, status={5},elapsed time ~={6} greedy={7}'.format(name, vert, method.__name__, lower if lower >= 0 else 'inf',obj, status, elapsed, greedy), file=f)
#TEX
with open('results/results.tex', 'w') as f:
	f.write('\\begin{table}[]\n')
	f.write('\\centering\n')
	f.write('\\caption{Results}\n')
	f.write('\\label{table}\n')
	f.write('\\begin{tabular}{l||l|l|l|l}\n')
	f.write('Graph & &{0} &{1}  &{2}\\\\\n\\toprule'.format(allMethods[0].__name__,allMethods[1].__name__,allMethods[2].__name__))
	
	for name in allTests:
		case = testCases[name]
		graph = case[0]
		vert = len(graph)
		f.write('\n{0}&&&&\\\\'.format(name.replace ('_', '\_')))
		statusList =[]
		ubList=[]
		lbList=[]
		timeList=[]
		for method in allMethods:
			vert, lower, obj, status, elapsed, greedy = results[(name, method.__name__)]
			statusList.append(status.replace ('_', '\_'))
			ubList.append(obj)
			lbList.append(lower)
			timeList.append(elapsed)
		f.write('\nVertices={3} &Status: &{0}  &{1} &{2}\\\\\n\\cline{{2-5}}'.format(statusList[0], statusList[1],statusList[2],vert))
		f.write('\nGreedy ub ={3}&Best objective: &{0}  &{1} &{2}\\\\\n\\cline{{2-5}}'.format(ubList[0], ubList[1],ubList[2],greedy))
		f.write('\n&Lower bound: &{0}  &{1} &{2}\\\\\n\\cline{{2-5}}'.format(lbList[0] if lbList[0] >= 0 else 'inf', lbList[1] if lbList[1] >= 0 else 'inf',lbList[2] if lbList[2] >= 0 else 'inf'))
		f.write('\n&Compute time: &{0} seconds  &{1} seconds &{2} seconds\\\\'.format(timeList[0], timeList[1],timeList[2]))
		f.write('\n\\hline')
	f.write('\n\\bottomrule\n\\end{tabular}\n\\end{table}')
