import chromatic		#CPLEX models
import graphtools		#I/O of graphs etc.
import lego, cubes		#Some special graph classes

from graphtools import readDimacs		#Read Dimacs text format examples
from lego import legoG, legoGP			#Soren's graphs G, Gprime
from cubes import Qdu, Qdus				#Cube-like graphs, see course lecture notes
from chromatic import smartStatement	# ... and other models

# I set these globally, but they'd better be adjusted to specific examples
timeLimit = 60.0
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
	"myciel3": (readDimacs('data/myciel3.col'), ub, timeLimit),
    "myciel4": (readDimacs('data/myciel4.col'), ub, timeLimit),
    "myciel5": (readDimacs('data/myciel5.col'), ub, timeLimit),
    "myciel6": (readDimacs('data/myciel6.col'), ub, timeLimit),
	"myciel7": (readDimacs('data/myciel7.col'), ub, timeLimit),
	# Real application (register allocation) graphs (large chromatic numbers!)
	"reg1": (readDimacs('data/zeroin.i.1.col'), 50, timeLimit),
    "reg2": (readDimacs('data/zeroin.i.2.col'), 50, timeLimit),
    "reg3": (readDimacs('data/zeroin.i.3.col'), 50, timeLimit),
    "reg4": (readDimacs('data/mulsol.i.1.col'), 50, timeLimit),
    "reg5": (readDimacs('data/mulsol.i.2.col'), 50, timeLimit),

}

results = {}

def getByName(cases, str):
	return [ name for name in testCases if str in name.lower() ]

for name in getByName(testCases, "reg5"):
	case = testCases[name]
	graph = case[0]
	vert = len(graph)
	upper = case[1]
	limit = case[2]
	for method in [smartStatement]:
		obj, lower, status = method(graph, upper, limit)
		results[(name, method.__name__)] = (vert, obj, lower, status)

print results

