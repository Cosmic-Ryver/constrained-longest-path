from ..bellman_ford import bellman_ford

G = [[0, 10, 2, 4, 6],
	 [2,  0, 4, 8, 1],
	 [3,  7, 0, 1, 9],
	 [7,  3, 6, 0, 4],
	 [6,  3, 7, 1, 0]]
s = 0

(dist, prev) = bellman_ford(G, s)
print(dist)
print(prev)
