from ..complete_solution import solution

G = [[0, 2, 2, 2, -1],
	 [9, 0, 2, 2, -1],
	 [9, 3, 0, 2, -1],
	 [9, 3, 2, 0, -1],
	 [9, 3, 2, 2,  0]]
c = 1
result = solution(G, c)
print(result)

G = [[0, 1, 1, 1, 1],
	 [1, 0, 1, 1, 1],
	 [1, 1, 0, 1, 1],
	 [1, 1, 1, 0, 1],
	 [1, 1, 1, 1, 0]]
c = 3
result = solution(G, c)
print(result)
