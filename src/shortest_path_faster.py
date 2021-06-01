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
