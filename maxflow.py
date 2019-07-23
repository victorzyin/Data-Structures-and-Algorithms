import collections

def initializeResidualGraph(graph):
	residualGraph = {}
	for u in graph.keys():
		if residualGraph.get(u, -1) == -1:
			residualGraph[u] = {}
		for v in graph[u].keys():
			residualGraph[u][v] = graph[u][v]
			if residualGraph.get(v, -1) == -1:
				residualGraph[v] = {}
			residualGraph[v][u] = 0
	return residualGraph

def initializeFlows(graph):
	flows = {}
	for u in graph.keys():
		flows[u] = {}
		for v in graph[u].keys():
			flows[u][v] = 0
	return flows

def residPath(graph, minimumEdge):
	queue = ["s"]
	visited = set()
	visited.add("s")
	parents = {}

	while queue:
		u = queue.pop()
		for v in graph[u].keys():
			if v not in visited and graph[u][v] > minimumEdge:
				parents[v] = u
				if v == "t":
					p = []
					mincap = graph[parents[v]][v]
					while v != "s":
						parent = parents[v]
						p.append((parent, v))
						mincap = min(mincap, graph[parent][v])
						v = parent
					return (p, mincap)
				queue.append(v)
				visited.add(v)
	return (None, None)

def augmentFlows(graph, p, mincap):
	for u, v in p:
		if graph[u].get(v, -1) == -1:
			graph[v][u] -= mincap
		else:
			graph[u][v] += mincap
	return graph

def changeCapacities(graph, p, mincap):
	for u, v in p:
		graph[u][v] -= mincap
		graph[v][u] += mincap
	return graph

def shortestResidPath(graph, minEdge):
	queue = collections.deque(["s"])
	parents = {}
	visited = set()
	visited.add("s")
	while queue:
		u = queue.popleft()
		if graph.get(u, -1) != -1:
			for v in graph[u]:
				if v not in visited and graph[u][v] > minEdge:
					parents[v] = u
					visited.add(v)
					queue.append(v)
					if v == "t":
						path = []
						vertex = v
						mincap = graph[parents[v]][v]
						while vertex != "s":
							path.append((parents[vertex], vertex))
							mincap = min(mincap, graph[parents[vertex]][vertex])
							vertex = parents[vertex]
						return (path, mincap)
	return (None, None)

def fordFulkerson(graph):
	residualGraph = initializeResidualGraph(graph)
	p, mincap = residPath(residualGraph, 0)
	while p != None:
		changeCapacities(residualGraph, p, mincap)
		p, mincap = residPath(residualGraph, 0)

	maxFlow = 0
	for v in residualGraph["s"]:
		if residualGraph["s"][v] == 0:
			maxFlow += graph["s"][v]
	return maxFlow

def edmondsKarp(graph):
	residualGraph = initializeResidualGraph(graph)
	flows = initializeFlows(graph)
	p, mincap = shortestResidPath(residualGraph, 0)
	while p != None:
		augmentFlows(flows, p, mincap)
		changeCapacities(residualGraph, p, mincap)
		p, mincap = shortestResidPath(residualGraph, 0)

	maxFlow = 0
	for v in flows["s"]:
		maxFlow += flows["s"][v]
	return maxFlow

