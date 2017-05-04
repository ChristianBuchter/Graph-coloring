# Generic tools for manipulating graphs

from itertools import product,chain,izip
from random import shuffle

'''
Test symmetric + zeros on diagonal
'''
def testAdj(A):
	n, m = len(A), len(A[0])
	if n!=m: raise "Not square"
	for i in range(n): 
		if A[i][i]==1: raise "Loops"
	for i,j in product(range(n), range(n)):
		if A[i][j]!=A[j][i]: raise "Not symmetric"
	return A

'''
Canonicalize the graph into an adjacency matrix using the given vertex set
'''
def canonical(vertices, edges):
	n = len(vertices)
	v = { x:i for x,i in izip(vertices, range(n)) }
	A = [[0 for i in range(n)] for j in range(n)]
	for e in edges:
		A[v[e[0]]][v[e[1]]] = 1
	return testAdj(A)

'''
Print graph (adj matrix) to a file in DIMACS compatible format
'''
def printDimacs(A, filename):
	n = len(A)
	m = sum([sum(x) for x in A]) // 2
	with open(filename, 'w') as f:
		f.write("p edge {0} {1}\n".format(n, m))
		for i in range(n):
			for j in range(i,n):
				if A[i][j]==1:
					f.write("e {0} {1}\n".format(i+1, j+1))

'''
Read graph in DIMACS format. Return adjacency matrix.
Vertices are numbered 1..n, we map it to 0..n-1
'''
def readDimacs(filename):
	v = 0
	e = 0
	edgesBoth = []
	with open(filename) as f:
		for line in f.readlines():
			if line[0]=="p":
				_, _, v, e = line.split()
				v, e = int(v), int(e)
			if line[0]=="e":
				_, x, y = line.split()
				edgesBoth.append((int(x)-1,int(y)-1))				
				edgesBoth.append((int(y)-1,int(x)-1))
	return canonical(range(v), edgesBoth)

'''
Return graph complement in matrix format
'''
def complement(A):
	n = len(A)
	B = [[1-x for x in row] for row in A]
	for i in range(n): B[i][i] = 0
	return B

'''
Return the edge list of a graph from matrix format
'''
def intoEdges(A):
	n = len(A)
	return [ (x,y) for x,y in product(range(n),range(n)) if A[x][y]==1 ]

'''
Return the best greedy chromatic number of A over a course of s random vertex orderings
'''
def bestGreedyChi(A, s):
	n = len(A)
	best = 10**9
	for _ in range(s):
		o = range(n)
		shuffle(o)
		col = [-1] * n
		for x in o:
			used = [False] * n
			for y in range(n):
				if A[x][y]==1 and col[y]!=-1:
					used[col[y]] = True
			col[x] = min([c for c in range(n) if not used[c]])
		best = min(best, max(col)+1)
	return best

'''
Random bipartite graph on n vertices
'''
def bipRandom(n):
	m = 2*n
	A = [[0 for i in range(m)] for j in range(m)]
	for i,j in product(range(0,n),range(n,m)):
		if (i*i+j*j)%17 < 4:
			A[i][j] = A[j][i] = 1
	return A