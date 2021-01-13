import networkx as nx

PROFIT = 'profit'
VALUE = 'value'
INITIAL = 'initial'

max_depth = 0
max_profit = 0
positive_errors = 0

def _create_graph(spect, l):
	G = nx.MultiDiGraph()
	vertices = list(set(map(lambda x: x[:-1], spect)))
	letters = ['A', 'C', 'T', 'G']
	arr = []
	for vertFrom in vertices:
		for vertTo in vertices:
			for ending in letters:
				el = vertFrom + ending
				isInSpec = 1
				if el in spect:
					isInSpec = 0
				for x in range(l-1, -1, -1):
					if x == 0:
						arr.append((el[:-1], vertTo, {PROFIT: max(x - isInSpec, 0), VALUE: el[-1], INITIAL: isInSpec == 0}))
						break
					elif el[l-x:] == vertTo[:x]:
						arr.append((el[:-1], vertTo, {PROFIT: x - isInSpec, VALUE: el[-1], INITIAL: isInSpec == 0}))
						break
	G.add_edges_from(arr)
	print("--------------GRAPH--------------")
	print(list(G.edges(data=True)))
	return G


def _find_euler(G, spectrum, neg_errors):
	arr = []
	print("--------------EULER--------------")
	for val in G.nodes:
		copy = G
		arr = _check_node(copy.copy(), val, max_depth, [val], spectrum, neg_errors)
		if type(arr) is list:
			break
	return arr


def _check_node(copy, node, depth, routes, spectrum, neg_errors_left):
	print("    " * (max_depth - depth) + "Checking " + node + "'s edges")
	for routeNode in copy[node]:
		for route in copy[node][routeNode]:
			for i in range(max_profit, -1, -1):
				if depth == 1:
					if neg_errors_left + copy[node][routeNode][route][PROFIT] - max_profit == 0:
						print("Finished checking! Returning results...")
						spec_copy = spectrum[:]
						if copy[node][routeNode][route][INITIAL]:
							spec_copy.remove(node + copy[node][routeNode][route][VALUE])
						if len(spec_copy) == positive_errors:
							lastVal = copy[node][routeNode][route][VALUE]
							return routes + [lastVal, copy[node][routeNode][route][PROFIT], routes[-1][-1] + lastVal]
					elif copy[node][routeNode][route][INITIAL]:
						spec_copy = spectrum[:]
						spec_copy.remove(node + copy[node][routeNode][route][VALUE])
						if len(spec_copy) == positive_errors:
							lastVal = copy[node][routeNode][route][VALUE]
							return routes + [lastVal, max_profit - neg_errors_left, routes[-1][-1] + lastVal]
				elif neg_errors_left + copy[node][routeNode][route][PROFIT] - max_profit >= 0 and copy[node][routeNode][route][PROFIT] == i:
					print("    " * (max_depth - depth) + "Going to " + routeNode + " by " + copy[node][routeNode][route][VALUE] + " with profit " + str(copy[node][routeNode][route][PROFIT]))
					spec_copy = spectrum[:]
					if copy[node][routeNode][route][INITIAL]:
						spec_copy.remove(node + copy[node][routeNode][route][VALUE])
					ret = _check_node(_remove_edges(copy, node, copy[node][routeNode][route][VALUE]), routeNode, depth - 1, routes + [copy[node][routeNode][route][VALUE], copy[node][routeNode][route][PROFIT], routeNode], spec_copy, neg_errors_left + copy[node][routeNode][route][PROFIT] - max_profit)
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


def _make_spectrum_nice_with_errors(arr, length):
	print(arr)
	if type(arr) is bool:
		print("Couldn't find proper spectrum....")
		return
	for i in range(len(arr)):
		if i == 0:
			continue
		elif i % 2 == 0:
			arr[i] = arr[i][-1]
	sp = ''.join(arr[0::2])
	# print(sp)
	values = []
	for i in range(len(sp)-length+1):
		values.append(sp[i:i+length])
	# print(values)


if __name__ == '__main__':
	positive_errors = 1
	negative_errors = 1
	spectrum = ["AAA", "GTA", "CGC", "ACA", "CAC", "ACG", "CAA", "GCA", "ACT", "TTA", "CTT", "TAA"]
	# spectrum = ["AAAAAACT", "AAAAACTA", "AAAACTAA", "AAACTAAG", "AACTAAGG", "ACTAAGGT", "CTAAGGTC", "TAAGGTCC", "AAGGTCCC", "AGGTCCCT", "GGTCCCTG", "GTCCCTGA"]
	# spectrum = ["ACG", "CCG", "CGA", "CGT", "GAC"]

	max_depth = len(spectrum) - positive_errors
	max_profit = len(spectrum[0]) - 1
	length = len(spectrum[0])

	stop = False
	for el in spectrum:
		if len(el) != length:
			print("Invalid input - wrong length!!!")
			stop = True
			break
	if not stop:
		graph = _create_graph(spectrum, length)
		_make_spectrum_nice_with_errors(_find_euler(graph, spectrum, negative_errors), length)

