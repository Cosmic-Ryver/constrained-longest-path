# Constrained Longest Path

A solver for the following constrained longest path problem:

You are given a strongly connected directed graph with finite integer edge
weights, an initial negative cost, a source node, and a sink node. Edge weights
need not be positive. Negative cycles, that is closed paths whose edge weights
sum to a negative value, may exist.

For *the* path from source to sink subject to the constraints: **(1)** the
sum of the weights along the path and the initial cost, herein referred to as
the path's *cost-sum*, is non-positive; **(2)** the path includes the maximum
number of unique nodes of all paths satisfying constraint (1); and **(3)** the
sum of the indices of the unique intermediary nodes is the minimum out of all
paths satisfying constraints (1) and (2); return the indices of all unique intermediary
nodes in the path in ascending order.

The inputs are constrained such that there will always be a non-positive
cost-sum path from source to sink, the source and sink are disjoint, and the
weight of the self-edge for every node is zero.

## Observations

If a negative cycle exists in the graph, the solution is always the set of
indices of all the intermediary nodes. This holds true because the negative
cycle may be walked infinitely to decrease the path's cost-sum to negative
infinity. The graph is strongly connected, so there is no question of whether
any given path exists.

If a negative cycle does not exist, this problem is a true longest-path problem
and is therefore NP-hard.

Every edge that has a non-positive weight and is not part of a negative cycle
may be represented as a set of equivalent arcs of positive weight from every
other node to that edge's destination node. Such arcs may need to span several
nodes to accrue a positive cost-sum

*The following observations assume a negative cycle does not exist in the graph
and that all non-positive weight edges have been replaced with equivalent
positive cost-sum arcs. No differentiation between such arcs and normal edges is
made. Both are referred to simply as 'edges'. Note that the cost-sum of
traversing an arc is equivalent to the weight associated with traversing an
edge.*

If the graph consists only of edges of positive weight, every node in the graph
has one or more minimum cost-sum arcs to the sink. This will be herein referred
to as the *exit-cost* of a node.

Solving the longest-path problem necessitates a depth first search. At each step
of this search we need only consider edges where the weight combined with the
exit-cost of the destination node would not cause the current path's cost-sum to
be positive. Thus, the search is not infinite and the problem is tractable. Let
us call edges satisfying this condition *traversable*.

Finally, we need not explore all traversable edges at every step. Instead we can
consider only the minimum cost paths from the current node to each node not in
the current path. These costs are fixed and can be computed prior to the depth
first search. In fact, instead of performing the DFS on the original graph, we
can construct an *arc graph* from these minimum cost paths. Each node in the arc
graph corresponds to a shortest pair path in the original graph. Thus any node
of the arc graph may correspond to one or more nodes in the original graph.

## Algorithm

1. Find all minimum positive-cost arcs for all non-positive weight edges in the
   graph. If one of these arcs connects to itself before its cost-sum becomes
   positive, a negative cycle has been found. Exit and return the set of node
   indices.
2. Compute the minimum cost pair paths of the graph.
3. Construct the arc graph from the minimum cost pairs.
4. Initialize the solution set as empty and the solution-set-sum as null.
5. Perform a depth first search from the source along all traversable edges to
   nodes not in the current path.
6. When no such edge out of the current search node remains, compute the
   set of indices of unique intermediary nodes in the current path. If this
   *current set* contains more members than the solution set, replace the
   solution set and set the solution-set-sum to null. Else, if this set contains
   the same number of members as the solution set, compute the current-set-sum
   as the sum of indices in the current set and compare it to the
   solution-set-sum. If the solution-set-sum is null compute and save it as the
   sum of indices in the solution set. If the current-set-sum is smaller than
   the solution-set-sum, replace the solution set with the current set and the
   solution-set-sum with the current-set-sum. Finally, step out of the current
   node to its parent in the current path and mark that edge as explored for the
   current path.
