def shortest_path_faster(G, s):
    """find the shortest paths in a digraph

	This function provides a small improvement over bellman_ford.

    Arguments:

    G: Type List[List[int]]. A dense directed graph in the form of a square
        matrix. An element G[i][j] is the cost to go from node i to node j.

    s: Type int. The indice of the source node whose shortest paths are to be
        found.

    Returns:

    result[0]: Type List[int]. The shortest path lengths. Each element
        result[0][i] is the shortest distance from node s to node i.

    result[1]: Type List[int]. Path predecessors. Each element result[1][i] is
        the node j immediately prior to node i in the shortest path from node s
        to node i.
    """

    # Step 1: initialize graph
    n = len(G)
    dist = [999999999999999999999] * n
    prev = [None] * n
    nodes = range(n)
    dist[s] = 0              # The distance from the source to itself is, of course, zero

    # Step 2: relax edges repeatedly
    for k in range(n - 1):
        keep = [False] * n
        for i in nodes:
            for j in range(n):
                w = G[i][j]
                if dist[i] + w < dist[j]:
                    keep[j] = True
                    dist[j] = dist[i] + w
                    prev[j] = i
        nodes = [i for i in range(n) if keep[i]]
        if len(nodes) == 0:
            break

    # Step 3: check for negative-weight cycles
    for i in range(n):
        for j in range(n):
            if dist[i] + G[i][j] < dist[j]:
                raise ValueError("Graph contains a negative-weight cycle")

    return (dist, prev)

def all_pairs_shortest_paths(G):
	n = len(G)
	S = [None] * n
	P = [None] * n
	for i in range(n):
		(dist, prev) = shortest_path_faster(G, i)
		S[i] = dist
		P[i] = prev

	return (S, P)

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
		(S, P) = all_pairs_shortest_paths(G)
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
			if not is_in_path[v] and (path_cost + S[u][v] + S[v][n_m1]) < 1:
				i_p1 = i + 1
				is_in_path[v] = True
				path.append(v)
				path_cost += S[u][v]
				weights[i_p1] = S[u][v]
				contributions[i_p1] = [v]
				w = v
				while P[u][w] is not None:
					if not is_in_path[w]:
						is_in_path[w] = True
						contributions[i_p1].append(w)
					w = P[u][w]
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
