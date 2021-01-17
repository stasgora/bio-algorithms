import networkx as nx

PROFIT = 'profit'
VALUE = 'value'
INITIAL = 'initial'
MAX_ANSWERS = 1
FILE = 'data.txt'

max_depth = 0
max_profit = 0
positive_errors = 0
length = 0
answers = []
negative_errors = 0


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
	print("--------------EULER--------------")
	for val in G.nodes:
		copy = G
		ret = _check_node(copy.copy(), val, max_depth, [val], spectrum, neg_errors)
		if type(ret) is not bool:
			break
	return


def _check_node(copy, node, depth, routes, spectrum, neg_errors_left):
	for routeNode in copy[node]:
		for route in copy[node][routeNode]:
			for i in range(max_profit, -1, -1):
				if depth == 1 and copy[node][routeNode][route][PROFIT] == i:
					global answers
					lastVal = copy[node][routeNode][route][VALUE]
					if neg_errors_left + copy[node][routeNode][route][PROFIT] - max_profit == 0:
						spec_copy = spectrum[:]
						if copy[node][routeNode][route][INITIAL]:
							spec_copy.remove(node + copy[node][routeNode][route][VALUE])
						if len(spec_copy) == positive_errors:
							answer = routes + [lastVal, copy[node][routeNode][route][PROFIT], routes[1:][-1] + lastVal]
							if answer not in answers:
								answers = answers + [answer]
								if len(answers) == MAX_ANSWERS:
									return []
					elif copy[node][routeNode][route][INITIAL] and routes[1:][-1] + lastVal not in copy.nodes:
						spec_copy = spectrum[:]
						spec_copy.remove(node + copy[node][routeNode][route][VALUE])
						if len(spec_copy) == positive_errors:
							answer = routes + [lastVal, copy[node][routeNode][route][PROFIT], routes[1:][-1] + lastVal]
							if answer not in answers:
								answers = answers + [answer]
								if len(answers) == MAX_ANSWERS:
									return []
				elif neg_errors_left + copy[node][routeNode][route][PROFIT] - max_profit >= 0 and copy[node][routeNode][route][PROFIT] == i:
					spec_copy = spectrum[:]
					if copy[node][routeNode][route][INITIAL]:
						spec_copy.remove(node + copy[node][routeNode][route][VALUE])
					ret = _check_node(_remove_edges(copy, node, copy[node][routeNode][route][VALUE]), routeNode, depth - 1, routes + [copy[node][routeNode][route][VALUE], copy[node][routeNode][route][PROFIT], routeNode], spec_copy, neg_errors_left + copy[node][routeNode][route][PROFIT] - max_profit)
					if type(ret) is not bool:
						return ret
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


def _make_answers_nice():
	global answers
	if len(answers) == 0:
		print("Couldn't find anything...")
	j = 0
	for answer in answers:
		spec = [answer[0]]
		j += 1
		values = []
		err_sum = 0
		for i in range(len(answer)):
			if i == len(answer) - 1:
				pass
			elif i % 3 == 0:
				values.append(answer[i] + answer[i+1])
			elif i % 3 == 2:
				if i == len(answer) - 2:
					if err_sum == 0 and negative_errors > 1 and length < 4:
						spec.append(answer[i - 1] + 'X' * max(0, negative_errors - length + 1) + answer[i + 1])
					else:
						spec.append(answer[i + 1][len(answer[i + 1]) - negative_errors + err_sum - 1:])
				else:
					err_sum += max_profit - answer[i]
					if answer[i] == 0 and length < 4:
						spec.append(answer[i - 1] + answer[i + 1][answer[i]:])
					else:
						spec.append(answer[i+1][answer[i]-1:])
		print("Answer " + str(j) + ": ")
		print(answer)
		print(values)
		print(''.join(spec) + ", Length: " + str(len(''.join(spec))))
	return


if __name__ == '__main__':
	f = open(FILE, "r")
	spectrum = f.readline().split()
	positive_errors = int(f.readline())
	negative_errors = int(f.readline())
	f.close()

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
		_find_euler(graph, spectrum, negative_errors)
		_make_answers_nice()

