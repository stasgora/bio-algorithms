import math


O = [1, 2, 3, 4, 5, 6]
S = ['F', 'L']
P = [0.95, 0.05]
Y1 = [3, 1, 5, 1, 1, 6, 2, 4, 6, 4, 4, 6, 6, 4, 4, 2, 4, 5, 3, 1, 1, 3, 2, 1, 6, 3, 1, 1, 6, 4, 1, 5, 2, 1, 3, 3, 6, 2, 5, 1, 4, 4, 5, 4, 3, 6, 3, 1, 6, 5, 6, 6, 2, 6, 5, 6, 6, 6, 6, 6]
D1 = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFLLLLLLLLLLLLLLL'
Y2 = [6, 5, 1, 1, 6, 6, 4, 5, 3, 1, 3, 2, 6, 5, 1, 2, 4, 5, 6, 3, 6, 6, 6, 4, 6, 3, 1, 6, 3, 6, 6, 6, 3, 1, 6, 2, 3, 2, 6, 4, 5, 5, 2, 3, 6, 2, 6, 6, 6, 6, 6, 6, 2, 5, 1, 5, 1, 6, 3, 1]
D2 = 'LLLLLLFFFFFFFFFFFFLLLLLLLLLLLLLLLLFFFLLLLLLLLLLLLLLFFFFFFFFF'
Tm = [
	[0.95, 0.05],
	[0.1, 0.9]
]
Em = [
	[1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
	[0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
]


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
	return forward_pass, backward_pass, smooth


process_pass = lambda x: [('F' if i[0] > i[1] else 'L') for i in x]
forward_pass, backward_pass, smooth = forward_backward(Y2, S, P, Tm, Em)
print(''.join(map(str, Y2)))
print(D2)
print(''.join(process_pass(forward_pass)))
print(''.join(process_pass(backward_pass)))
print(''.join(smooth))
