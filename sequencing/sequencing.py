import networkx as nx


def _create_graph(spect, l):
	G = nx.MultiDiGraph()
	vertices = list(set(map(lambda x: x[:-1], spect)))
	arr = []
	for el in spect:
		for vert in vertices:
			for x in range(l-1, -1, -1):
				if x == 0:
					arr.append((el[:-1], vert, {'weight': x, 'value': el[-1]}))
				elif el[l-x:] == vert[:x]:
					arr.append((el[:-1], vert, {'weight': x, 'value': el[-1]}))
	G.add_edges_from(arr)
	print(list(G.edges(data=True)))
	return G


if __name__ == '__main__':
	spectrum, length = ["AAA", "AAC", "ACA", "CAC", "CAA", "ACG", "CGC", "GCA", "ACT", "CTT", "TTA", "TAA"], 3
	graph = _create_graph(spectrum, length)
