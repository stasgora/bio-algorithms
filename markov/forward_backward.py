import math


def forward_backward(Y, S, P, Tm, Em):
	forward_pass = []
	for i in range(len(Y)):
		current = {}
		for st in range(len(S)):
			current[st] = Em[st][Y[i] - 1] * (P[st] if i == 0 else sum(previous[k] * Tm[k][st] for k in range(len(S))))
		forward_pass.append(current)
		previous = current
	product = math.prod(current[k] for k in range(len(S)))

	backward_pass = []
	for i in range(len(Y), 0, -1):
		current = {}
		for st in range(len(S)):
			current[st] = 1 if i == len(Y) else sum(Tm[st][l] * Em[l][Y[i] - 1] * previous[l] for l in range(len(S)))
		backward_pass.insert(0, current)
		previous = current

	smooth = []
	for i in range(len(Y)):
		vals = [forward_pass[i][st] * backward_pass[i][st] / product for st in range(len(S))]
		smooth.append(S[vals.index(max(vals))])
	return smooth
