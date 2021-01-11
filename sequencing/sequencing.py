import networkx as nx

PROFIT = 'profit'
VALUE = 'value'

max_depth = 0

def _create_graph(spect, l):
	G = nx.MultiDiGraph()
	vertices = list(set(map(lambda x: x[:-1], spect)))
	arr = []
	for el in spect:
		for vert in vertices:
			for x in range(l-1, -1, -1):
				if x == 0:
					arr.append((el[:-1], vert, {PROFIT: x, VALUE: el[-1]}))
					break
				elif el[l-x:] == vert[:x]:
					arr.append((el[:-1], vert, {PROFIT: x, VALUE: el[-1]}))
					break
	G.add_edges_from(arr)
	print("--------------GRAPH--------------")
	print(list(G.edges(data=True)))
	return G


def _find_euler(G):
	arr = []
	print("--------------EULER--------------")
	for val in G.nodes:
		copy = G
		arr = _check_node(copy.copy(), val, max_depth, [val])
		if type(arr) is list:
			break
	return arr


def _check_node(copy, node, depth, routes):
	print("    " * (max_depth - depth) + "Checking " + node + "'s edges")
	for routeNode in copy[node]:
		for route in copy[node][routeNode]:
			if depth == 1:
				print("Finished checking! Returning results...")
				lastVal = copy[node][routeNode][route][VALUE]
				return routes + [lastVal,  routes[-1][-1] + lastVal]
			if copy[node][routeNode][route][PROFIT] == len(node):
				print("    " * (max_depth - depth) + "Going to " + routeNode + " by " + copy[node][routeNode][route][VALUE] + " with profit " + str(copy[node][routeNode][route][PROFIT]))
				ret = _check_node(_remove_edges(copy, node, copy[node][routeNode][route][VALUE]), routeNode, depth - 1, routes + [copy[node][routeNode][route][VALUE], routeNode])
				if type(ret) is not bool:
					return ret
				else:
					print("    " * (max_depth - depth) + "Bad route :( Moving back....")
	print("    " * (max_depth - depth) + "Really bad node!!! Moving back harder.....")
	return False


def _remove_edges(G, node, val):
	arr = []
	copied = G.copy()
	for n, nbrsdict in G.adjacency():
		for nbr, keydict in nbrsdict.items():
			for key, eattr in keydict.items():
				if n == node and eattr[VALUE] == val:
					arr.append((n, nbr, key))
	copied.remove_edges_from(arr)
	return copied


def _make_spectrum_nice_no_errors(arr, length):
	if type(arr) is bool:
		print("Couldn't find proper spectrum....")
		return
	for i in range(len(arr)):
		if i == 0:
			continue
		elif i % 2 == 0:
			arr[i] = arr[i][-1]
	sp = ''.join(arr[0::2])
	print(sp)
	values = []
	for i in range(len(sp)-length+1):
		values.append(sp[i:i+length])
	print(values)


if __name__ == '__main__':
	# spectrum = ["AAA", "AAT", "AAC", "ACA", "CAC", "CAA", "ACG", "CGC", "GCA", "ACT", "CTT", "TTA", "TAA"]
	spectrum = ["PPPPPPct", "PPPPPcta", "PPPPctaa", "PPPctaaG", "PPctaaGG", "PctaaGGT", "ctaaGGTC", "taaGGTCC", "aaGGTCCC", "aGGTCCCT", "GGTCCCTe", "GTCCCTea"]
	# spectrum = ["ACG", "CCG", "CGA", "CGT", "GAC"]

	max_depth = len(spectrum)
	length = len(spectrum[0])
	graph = _create_graph(spectrum, length)
	_make_spectrum_nice_no_errors(_find_euler(graph), length)

