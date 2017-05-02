# Descriptions of Lego-related graphs

import graphtools
from graphtools import *

from itertools import product,chain,izip

'''
Coordinates of (p,q) blocks which touch an (a,b) block fixed at (0,0)
'''
def touch(a, b, p, q):
	return list(chain( product(range(-p+1,a),[-q,b]), product([-p,a],range(-q+1,b) )))

'''
Coordinates of (p,q) blocks which overlap an (a,b) block fixed at (0,0)
'''
def overlap(a, b, p, q):
	return list( product(range(-p+1,a), range(-q+1,b)) )

'''
Edges between two types of tiles
'''
def base_edges(a, b, p, q, c, d, o1, o2, l1, l2, relation):
	return list(set([( (o1,x,y,l1), (o2,(x+u+c)%c,(y+v+d)%d,l2) ) 
		for x,y in product(range(c),range(d))
		for u,v in relation(a,b,p,q)]))

'''
Edges between two levels subject to a relation
'''
def level_edges(a, b, c, d, l1, l2, r):
	if a==b:
		return base_edges(a,a,a,a,c,d,0,0,l1,l2,r)
	else:
		return base_edges(a,b,a,b,c,d,0,0,l1,l2,r) + base_edges(a,b,b,a,c,d,0,1,l1,l2,r) + base_edges(b,a,a,b,c,d,1,0,l1,l2,r) + base_edges(b,a,b,a,c,d,1,1,l1,l2,r)

'''
Edges of the graph gp(a,b,c,d)
'''
def gp_edges(a, b, c, d):
	return level_edges(a,b,c,d,0,0,touch)

'''
Edges of the graph g(a,b,c,d)
'''
def g_edges(a, b, c, d):
	return level_edges(a,b,c,d,0,0,touch)+level_edges(a,b,c,d,1,1,touch)+level_edges(a,b,c,d,0,1,overlap)+level_edges(a,b,c,d,1,0,overlap)

'''
Adjacency matrix of GP(a,b,c,d)
'''
def legoGP(a, b, c, d):
	if a==b:
		return canonical( list(product([0], range(c), range(d), [0])), gp_edges(a, b, c, d) )
	else:
		return canonical( list(product([0,1], range(c), range(d), [0])), gp_edges(a, b, c, d) )

'''
Adjacency matrix of G(a,b,c,d)
'''
def legoG(a, b, c, d):
	if a==b:
		return canonical( list(product([0], range(c), range(d), [0,1])), g_edges(a, b, c, d) )
	else:
		return canonical( list(product([0,1], range(c), range(d), [0,1])), g_edges(a, b, c, d) )