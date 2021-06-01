from .shortest_path_faster import shortest_path_faster

def all_pairs_shortest_paths(G):
	n = len(G)
	S = [None] * n
	P = [None] * n
	for i in range(n):
		(dist, prev) = shortest_path_faster(G, i)
		S[i] = dist
		P[i] = prev

	return (S, P)
