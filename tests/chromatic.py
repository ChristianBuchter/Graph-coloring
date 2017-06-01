# Chromatic number by means of Cplex

# This is my rendition of your method
# for testing purposes

import cplex
from cplex.exceptions import CplexError

import sys, time, math

'''
graph - adjacency matrix (square, symmetric)
ub - upper bound, the number of colors we want to use
timeLimit - seconds

Returns:
bestObjective
objectiveLowerBound
solutionStatus
'''
def standard(graph, ub, timeLimit, threadLimit):
	try:
		my_prob = cplex.Cplex()
		my_prob.parameters.threads.set(threadLimit)
		my_prob.parameters.timelimit.set(timeLimit)
		my_prob.parameters.parallel.set(-1)
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
		for vertex in range(len(graph)):
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
		for vertex in range(len(graph)):
			tmp1 = []
			tmp2 = []
			for color in range(my_upperbound):
				tmp1.append("x"+str(vertex)+","+str(color))
				tmp2.append(1.0)
			rows.append([tmp1,tmp2])
		#A[v,u](x_{v,c}+x_{u,c}) <= 1 forall v,u
		for vertex in range(len(graph)):
			for color in range(my_upperbound):
				for adjVert in range(vertex+1,len(graph)):
					#maybe Cplex hanles integers alright, but for now I made it long and ugly.
					rows.append([["x"+str(vertex)+","+str(color), "x"+str(adjVert)+","+str(color)],[graph[vertex][adjVert]*1.0,graph[adjVert][vertex]*1.0]])
		#x_{v,c}-y_c <= 0 forall v
		for vertex in range(len(graph)):
			for color in range(my_upperbound):
				rows.append([["y"+str(color),"x"+str(vertex)+","+str(color)],[-1.0,1.0]])
		#rownames might be removeable        
		my_prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
									   rhs=my_rhs, names=my_rownames)

		# Only check feasibility
		#my_prob.parameters.mip.limits.solutions.set(1)
		start = my_prob.get_time();
		my_prob.solve()
		end = my_prob.get_time();
		elapsed = end - start
	except CplexError as exc:
		print(exc)
		return

	solsta = my_prob.solution.get_status()
	print(solsta, " ", my_prob.solution.status[solsta], elapsed)
	if solsta==103:
		# Infeasibility certificate
		return (ub+1,-1, my_prob.solution.status[solsta], elapsed)
	elif solsta==108:
		# Time limit infeasible
		return (-1, -1, my_prob.solution.status[solsta], elapsed)
	else:
		return (my_prob.solution.MIP.get_best_objective(), my_prob.solution.get_objective_value(), my_prob.solution.status[solsta], elapsed)
	
	
def binary(graph, ub, timeLimit, threadLimit):
	try:
		my_prob = cplex.Cplex()
		my_prob.parameters.threads.set(threadLimit)
		my_prob.parameters.timelimit.set(timeLimit)
		my_prob.parameters.parallel.set(-1)
		my_prob.parameters.timelimit.get()

		my_obj = []
		my_ub = []
		my_ctype = ""
		my_colnames = {}
		old_cols = []
		my_rhs = []
		my_rownames = []
		my_sense = ""
		my_upperbound = ub
		binLen = int(math.ceil(math.log(ub,2)))
		varCounter = 0
		print("greedy upperbound: ", my_upperbound)
		
		my_obj.append(1.0) # Max color
		my_ub.append(float(my_upperbound)) #max is our upperbound
		old_cols.append("C")
		my_colnames["C"] = varCounter
		varCounter += 1
		my_ctype += "I" #C is integral
		for vertex in range(len(graph)):
			for colorBit in range(binLen):
				my_obj.append(0.0) # x_{v,b}
				my_ub.append(1.0) #all x_{v,b} are binary
				old_cols.append("x{},{}".format(vertex,colorBit))
				my_colnames["x{},{}".format(vertex,colorBit)] = varCounter
				varCounter += 1
				my_ctype += "I" #all x_{v,b} are binary
				
				for adjVert in range(vertex):
					my_obj.append(0.0) #z_{v,u,b}
					my_ub.append(1.0)
					old_cols.append("z{},{},{}".format(vertex,adjVert,colorBit))
					my_colnames["z{},{},{}".format(vertex,adjVert,colorBit)]= varCounter
					varCounter += 1
					my_ctype += "I"
					my_obj.append(0.0) #t_{v,u,b}
					my_ub.append(1.0)
					old_cols.append("t{},{},{}".format(vertex,adjVert,colorBit))
					my_colnames["t{},{},{}".format(vertex,adjVert,colorBit)]= varCounter
					varCounter += 1
					my_ctype += "I"
		for vertex in range(len(graph)):
			my_rhs.append(-1.0) #sum_b{2^b*x_{v,b}} - c \leq -1" forall v
			my_sense += "L"
			my_rownames.append("sum_b{2^b*x_{"+str(vertex)+",b}} - c \leq -1")
			
			for adjVert in range(vertex):
				my_rhs.append(1.0*graph[vertex][adjVert]) # sum_b{z_{v,u,b}} \geq 1*A_{v,u}
				#print("graph["+str(vertex)+"]["+str(adjVert)+"]: "+str(graph[vertex][adjVert]))
				my_sense += "G"
				my_rownames.append("sum_b{z_{"+str(vertex)+","+str(adjVert)+",b}} \geq 1")
				for colorBit in range(binLen):
					my_rhs.append(0.0) #for z_{v,u,b}- 2t_{v,u,b}+x_{v,b} -x_{u,b} = 0 forall everything
					my_sense += "E"
					my_rownames.append("|x_{"+str(vertex)+","+str(colorBit)+"} - x_{"+str(adjVert)+","+str(colorBit)+"}|")
				
		
		my_prob.objective.set_sense(my_prob.objective.sense.minimize)
		# since lower bounds are all 0.0 (the default), lb is omitted here
		my_prob.variables.add(obj=my_obj, ub=my_ub, types=my_ctype,
						   names=old_cols)
		rows =[]
		#sum_b{2^b*x_{v,b}} - c \geq 0" forall v
		for vertex in range(len(graph)):
			tmp1 = [my_colnames["C"]]
			tmp2 = [-1.0]
			for bit in range(binLen):
				tmp1.append(my_colnames["x{},{}".format(vertex,bit)])
				tmp2.append(math.pow(2,bit))
			rows.append([tmp1,tmp2])
			
			# sum_b{z_{v,u,b}} \geq 1
			for adjVert in range(vertex):
				tmp1 =[]
				tmp2 =[]
				for colorBit in range(binLen):
					tmp1.append(my_colnames["z{},{},{}".format(vertex,adjVert,colorBit)])
					tmp2.append(1.0)
				rows.append([tmp1,tmp2])
				# z_{v,u,b}- 2t_{v,u,b}+x_{v,b} -x_{u,b} = 0 forall everything
				for colorBit in range(binLen):
					z = my_colnames["z{},{},{}".format(vertex,adjVert,colorBit)]
					t = my_colnames["t{},{},{}".format(vertex,adjVert,colorBit)]
					tmp1 = [z,t,my_colnames["x{},{}".format(vertex,colorBit)], my_colnames["x{},{}".format(adjVert,colorBit)]]
					tmp2 = [1.0,-2.0,1.0,-1.0]
					rows.append([tmp1,tmp2])
		my_prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
									rhs=my_rhs, names=my_rownames)
		# Only check feasibility
		#my_prob.parameters.mip.limits.solutions.set(1)
		start = my_prob.get_time();
		my_prob.solve()
		end = my_prob.get_time();
		elapsed = end - start
	except CplexError as exc:
		print(exc)
		return

	solsta = my_prob.solution.get_status()
	print(solsta, " ", my_prob.solution.status[solsta], elapsed)
	if solsta==103:
		# Infeasibility certificate
		return (ub+1,-1, my_prob.solution.status[solsta], elapsed)
	elif solsta==108:
		# Time limit infeasible
		return (-1, -1, my_prob.solution.status[solsta], elapsed)
	else:
		return (my_prob.solution.MIP.get_best_objective(), my_prob.solution.get_objective_value(), my_prob.solution.status[solsta], elapsed)

def scheduling(graph, ub, timeLimit, threadLimit):
	try:
		my_prob = cplex.Cplex()
		my_prob.parameters.threads.set(threadLimit)
		my_prob.parameters.timelimit.set(timeLimit)
		my_prob.parameters.parallel.set(-1)		
		my_prob.parameters.timelimit.get()
		my_obj = []
		my_ub = []
		my_ctype = ""
		my_colnames = []
		my_rhs = []
		my_rownames = []
		my_sense = ""
		my_upperbound = ub
		print("greedy upperbound: ", my_upperbound)
		
		for vertex in range(len(graph)):
			my_obj.append(0.0)
			my_ub.append(ub)
			my_colnames.append("X"+str(vertex))
			my_ctype += "I" #all colors are integral
			
			my_rhs.append(-1.0) #X_v - c =< -1 forall v
			my_sense += "L"
			my_rownames.append("less than highest color "+str(vertex))
		for vertex in range(len(graph)):
			for edge in range(vertex):
				if graph[vertex][edge] == 1:
					my_obj.append(0.0)
					my_ub.append(1.0) #x_{u,v} is binary
					my_colnames.append("x"+str(vertex)+","+str(edge))
					my_ctype += "I" #x_{u,v} is binary
					
					my_rhs.append(my_upperbound-1.0) #X_u - X_v + Kx_{u,v} =< K-1  , K >= c
					my_sense += "L" 
					my_rownames.append("1 nonAdj"+str(vertex)+","+str(edge))
					my_rhs.append(-1.0) #X_v - X_u - Kx_{u,v} =< -1
					my_sense += "L" 
					my_rownames.append("2 nonAdj"+str(vertex)+","+str(edge))
					
		my_obj.append(1.0)
		my_ub.append(ub)
		my_colnames.append("c")
		my_ctype += "I" #c is integral (but it will be even when real)
				
		
		my_prob.objective.set_sense(my_prob.objective.sense.minimize)
		# since lower bounds are all 0.0 (the default), lb is omitted here
		my_prob.variables.add(obj=my_obj, ub=my_ub, types=my_ctype,
						   names=my_colnames)
		rows =[]
		#X_v - c =< -1 forall v
		for vertex in range(len(graph)):
			rows.append([["c","X"+str(vertex)],[-1.0,1.0]])

		for vertex in range(len(graph)):
			for edge in range(vertex):
				if graph[vertex][edge] == 1:
					#X_u - X_v + Kx_{u,v} =< K-1  , K >= c
					rows.append([["X"+str(vertex),"X"+str(edge),"x"+str(vertex)+","+str(edge)],[1.0,-1.0,my_upperbound]])
					#X_v - X_u - Kx_{u,v} =< -1
					rows.append([["X"+str(edge),"X"+str(vertex),"x"+str(vertex)+","+str(edge)],[1.0,-1.0,-my_upperbound]])    
		my_prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
									rhs=my_rhs, names=my_rownames)
		# Only check feasibility
		#my_prob.parameters.mip.limits.solutions.set(1)
		start = my_prob.get_time();
		my_prob.solve()
		end = my_prob.get_time();
		elapsed = end - start
	except CplexError as exc:
		print(exc)
		return

	solsta = my_prob.solution.get_status()
	print(solsta, " ", my_prob.solution.status[solsta], elapsed)
	if solsta==103:
		# Infeasibility certificate
		return (ub+1,-1, my_prob.solution.status[solsta], elapsed)
	elif solsta==108:
		# Time limit infeasible
		return (-1, -1, my_prob.solution.status[solsta], elapsed)
	else:
		return (my_prob.solution.MIP.get_best_objective(), my_prob.solution.get_objective_value(), my_prob.solution.status[solsta], elapsed)

