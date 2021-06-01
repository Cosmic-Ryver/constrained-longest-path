def all_pairs_shortest_paths(G):
	"""find all shortest paths in a complete, integer-weighted directed graph

	An implementation of the Floyd-Warshall algorithm[1]. Complexity is cubic:
	O(n**3). If the weights in G are small, other algorithms exist that can
	solve the problem with complexity as low as O(n**2.575) [2].

    Arguments:

    G: Type List[List[int]]. A complete directed graph in the form of a square
        matrix. An element G[i][j] is the cost to go from node i to node j.

	Returns:

    result[0]: Type List[List[int]]. Matrix of shortest path lengths. Each
        element result[0][u][v] is the shortest distance from node u to node v.

    result[1]: Type List[List[int]]. Matrix of path successors. Each element
        result[1][u][v] is the node w immediately after node u in the shortest
        path from node u to node v.

	Raises:

	ValueError: If a negative cycle exists in G.

	References:

	[1] https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm

	[2] Zwick, Uri. "All pairs shortest paths using bridging sets and
	rectangular matrix multiplication." Journal of the ACM (JACM) 49.3 (2002):
	289-317.
	"""

    # Step 1: initialize graph
	n = len(G)
	D = [[e for e in row] for row in G] # Minimum distance between nodes
	P = [[v for v in range(n)] for u in range(n)] # Successor of a node in its shortest path

    # Step 2: update edges repeatedly
	for w in range(n):
		for u in range(n):
			for v in range(n):
				diff = D[u][w] + D[w][v]
				if D[u][v] > diff:
					D[u][v] = diff
					P[u][v] = P[u][w]

    # Step 3: check for negative-weight cycles
	for v in range(n):
		if D[v][v] < 0:
			raise ValueError("Graph contains a negative-weight cycle")

	return (D, P)

def solution(G, c):
	"""solves the following constrained longest path problem

	You are given a complete directed graph with finite integer edge weights, an
	initial cost, a source node, and a sink node. Edge weights need not be
	positive. Negative cycles, that is closed paths whose edge weights sum to a
	negative value, may exist.

	For *the* path from source to sink subject to the constraints: **(1)** the
	sum of the weights along the path and the negated initial cost, herein
	referred to as the path's *cost-sum*, is non-positive; **(2)** the path
	includes the maximum number of unique nodes of all paths satisfying
	constraint (1); and **(3)** the sum of the indices of the unique
	intermediary nodes is the minimum out of all paths satisfying constraints
	(1) and (2); return the indices of all unique intermediary nodes in the path
	in ascending order.

	The inputs are constrained such that there will always be a non-positive
	cost-sum path from source to sink, the source and sink are disjoint, and the
	weight of the self-edge for every node is zero.

	Arguments:

    G: Type List[List[int]]. A complete directed graph in the form of a square
        matrix. An element G[i][j] is the cost to go from node i to node j. Node
        0 is the source. Node n, where n is len(G) is the sink.

	c: Type int. The initial cost.

	Returns:

	ids: Type List[int]. The ids of the unique intermediary nodes in the
		solution path, sorted in ascending order.
	"""

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
		(D, P) = all_pairs_shortest_paths(G)
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
