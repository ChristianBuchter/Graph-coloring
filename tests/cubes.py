# Descriptions of Cube-like graphs 

import graphtools
from graphtools import *

from itertools import product,chain,izip

'''
Q_d(u,s) - subgraph of d-cube with s coordinates equal to 1 and edges at distance u
This is a unit distance graph in R^{d-1}
'''
def Qdus(d,u,s):
	n = 2**d
	binSum = lambda n: 0 if n==0 else binSum(n/2) + n%2
	hamming = lambda n,m: binSum(n^m)
	v = [ x for x in range(n) if binSum(x)==s ]
	e = [ (x,y) for x,y in product(v,v) if hamming(x,y)==u ]
	return canonical(v, e)

'''
Q_d(u) - d-cube with edges at distance u, only the component with even hamming weight
Only reasonnable when u is even
This is a unit distance graph in R^{d}
'''
def Qdu(d,u):
	n = 2**d
	binSum = lambda n: 0 if n==0 else binSum(n/2) + n%2
	hamming = lambda n,m: binSum(n^m)
	v = [ x for x in range(n) if binSum(x)%2==0 ]
	e = [ (x,y) for x,y in product(v,v) if hamming(x,y)==u ]
	return canonical(v, e)