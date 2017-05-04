# Chromatic number by means of Cplex

# This is my rendition of your method
# for testing purposes

import cplex
from cplex.exceptions import CplexError

import sys, time

'''
graph - adjacency matrix (square, symmetric)
ub - upper bound, the number of colors we want to use
timeLimit - seconds

Returns:
bestObjective
objectiveLowerBound
solutionStatus
'''
def smartStatement(graph, ub, timeLimit):
	for row in range (1,len(graph)):
		if len(graph[row-1]) != len(graph[row]):
			print("Input a proper adjacency matrix")
			return
	try:
		my_prob = cplex.Cplex()
		my_prob.parameters.timelimit.set(timeLimit)
		my_prob.parameters.timelimit.get()
		my_obj = []
		my_ub = []
		my_ctype = ""
		my_colnames = []
		my_rhs = []
		my_rownames = []
		my_sense = ""
		my_upperbound = ub
		print("initial upperbound: ", my_upperbound)
		
		for color in range(0, my_upperbound):
			my_obj.append(1.0) # sum y_c
			my_ub.append(1.0) #all y_c are binary
			my_colnames.append("y"+str(color))
			my_ctype += "I" #all y_c are binary
		for vertex in range(0,len(graph)):
			my_rhs.append(1.0) #for sum_c x_{v,c} = 1 forall v
			my_sense += "E" 
			my_rownames.append("oneColor"+str(color))
		for vertex in range(0,len(graph)):
			for color in range(my_upperbound):
				my_obj.append(0.0) # x_{v,c}
				my_ub.append(1.0) #all x_{v,c} are binary
				my_colnames.append("x"+str(vertex)+","+str(color))
				my_ctype += "I" #all x_{v,c} are binary
				for adjVert in range(vertex+1,len(graph)):
					my_rhs.append(1.0) #for A[v,u](x_{v,c}+x_{u,c}) <= 1 forall v,u
					my_sense += "L" 
					my_rownames.append("noAdjCols"+str(vertex)+","+str(color)+","+str(adjVert))
		for vertex in range(len(graph)):
			for color in range(my_upperbound):
				my_rhs.append(0.0) #for x[v,c]-y[c] <= 0 forall v
				my_sense += "L"
				my_rownames.append("colorIsUsed"+str(color))
				
		
		my_prob.objective.set_sense(my_prob.objective.sense.minimize)
		# since lower bounds are all 0.0 (the default), lb is omitted here
		my_prob.variables.add(obj=my_obj, ub=my_ub, types=my_ctype,
						      names=my_colnames)
		rows =[]
		#sum_c x_{v,c} = 1 forall v
		for vertex in range(0,len(graph)):
			tmp1 = []
			tmp2 = []
			for color in range(0,my_upperbound):
				tmp1.append("x"+str(vertex)+","+str(color))
				tmp2.append(1.0)
			rows.append([tmp1,tmp2])
		#A[v,u](x_{v,c}+x_{u,c}) <= 1 forall v,u
		for vertex in range(0,len(graph)):
			for color in range(0,my_upperbound):
				for adjVert in range(vertex+1,len(graph)):
					#maybe Cplex hanles integers alright, but for now I made it long and ugly.
					rows.append([["x"+str(vertex)+","+str(color), "x"+str(adjVert)+","+str(color)],[graph[vertex][adjVert]*1.0,graph[adjVert][vertex]*1.0]])
		#x_{v,c}-y_c <= 0 forall v
		for vertex in range(0,len(graph)):
			for color in range(0,my_upperbound):
				rows.append([["y"+str(color),"x"+str(vertex)+","+str(color)],[-1.0,1.0]])
		#rownames might be removeable        
		my_prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
									   rhs=my_rhs, names=my_rownames)

		# Only check feasibility
		#my_prob.parameters.mip.limits.solutions.set(1)
		my_prob.solve()
	except CplexError as exc:
		print(exc)
		return

	solsta = my_prob.solution.get_status()
	print(solsta, " ", my_prob.solution.status[solsta])
	if solsta==103:
		# Infeasibility certificate
		return (ub+1,-1, my_prob.solution.status[solsta])
	elif solsta==108:
		# Time limit infeasible
		return (-1, -1, my_prob.solution.status[solsta])
	else:
		return (my_prob.solution.MIP.get_best_objective(), my_prob.solution.get_objective_value(), my_prob.solution.status[solsta])
	
