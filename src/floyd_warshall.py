def floyd_warshall(G):
	"""find all shortest paths in a dense integer weighted directed graph

	An implementation of the Floyd-Warshall algorithm[1][2]. Complexity is
	cubic: O(n**3). If the weights in G are small, complexity can be as low as
	O(n**2.575) [3].

    Arguments:

    G: Type List[List[int]]. A dense directed graph in the form of a square
        matrix. An element G[i][j] is the cost to go from node i to node j.

	Returns:

    result[0]: Type List[List[int]]. Matrix of shortest path lengths. Each element
        result[0][u][v] is the shortest distance from node u to node v.

    result[1]: Type List[List[int]]. Matrix of path successors. Each element result[1][u][v] is
        the node w immediately after node u in the shortest path from node u to node v.

	Raises:

	ValueError: If a negative cycle exists in G.

	References:

	[3] Zwick, Uri. "All pairs shortest paths using bridging sets and
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
