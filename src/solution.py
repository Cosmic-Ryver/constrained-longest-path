from .floyd_warshall import floyd_warshall

def solution(G, c):
	# Initializations
	i = 0
	n = len(G)
	n_m1 = n - 1
	result = []
	result_sum = None
	path = [0]
	path_cost = -c # Negate the initial budget to make main-loop calculations cheaper
	is_in_path = [False] * n
	is_in_path[0] = True # source always in path
	is_in_path[n_m1] = True # sink always implicitly in path
	next_edge = [1] * n # next_edge always starts at 1, because the source is always in the path
	contributions = [[] for k in range(n)] # each element is an array of new nodes added to the path by that level
	weights = [0] * n

	# Step 1: Solve the APSP Problem
	try:
		(D, P) = floyd_warshall(G)
	except ValueError:
		# Negative cycle exists
		return range(n - 2)

	# Step 2: Depth First Search
	while True:
		if next_edge[i] < n_m1:
			# May be able to advance from this level
			u = path[i]
			v = next_edge[i]
			next_edge[i] += 1

			# Advance only if we could exit from the next node, otherwise check another edge
			if not is_in_path[v] and (path_cost + D[u][v] + D[v][n_m1]) < 1:
				i_p1 = i + 1
				is_in_path[v] = True
				path.append(v)
				path_cost += D[u][v]
				weights[i_p1] = D[u][v]
				contributions[i_p1] = [v]
				u = P[u][v]
				while u is not v:
					if not is_in_path[u]:
						is_in_path[u] = True
						contributions[i_p1].append(u)
					u = P[u][v]
				i = i_p1
		else:
			# Cannot advance from this level

			# Break if we've explored all paths
			if i == 0:
				break

			# Update the result, if necessary
			candidate = [k - 1 for k in range(1, n_m1) if is_in_path[k]]
			if len(candidate) > len(result):
				result = candidate
				result_sum = None
			elif len(candidate) == len(result):
				if result_sum is None:
					result_sum = sum(result)
				candidate_sum = sum(candidate)
				if candidate_sum < result_sum:
					result = candidate
					result_sum = candidate_sum

			# Retreat one level
			next_edge[i] = 1
			path.pop()
			for c in contributions[i]:
				is_in_path[c] = False
			contributions[i] = []
			path_cost -= weights[i]
			weights[i] = 0
			i -= 1

	# Step 3: Sort and Return
	result.sort()
	return result
