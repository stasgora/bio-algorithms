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


def viterbi(O, S, P, Y, Tm, Em):
	T1 = [[0 for _ in range(len(Y))] for _ in range(len(S))]
	T2 = [[0 for _ in range(len(Y))] for _ in range(len(S))]
	for i in range(len(S)):
		T1[i][0] = P[i] * Em[i][Y[0] - 1]
		T2[i][0] = 0
	for j in range(1, len(Y)):
		for i in range(len(S)):
			k = 0
			func = lambda k: T1[k][j-1] * Tm[k][i] * Em[i][Y[j] - 1]
			max = func(k)
			for k_iter in range(len(S)):
				if max < func(k_iter):
					k = k_iter
					max = func(k)
			T1[i][j] = max
			T2[i][j] = k
	k = 0
	func = lambda k: T1[k][len(Y)-1]
	z = [0 for _ in range(len(Y))]
	max = func(k)
	for k_iter in range(len(S)):
		if max < func(k_iter):
			k = k_iter
			max = func(k)
	z[len(Y)-1] = k
	x = [0 for _ in range(len(Y))]
	x[len(Y)-1] = S[z[len(Y)-1]]
	for j in range(len(Y) - 1, 0, -1):
		z[j-1] = T2[z[j]][j]
		x[j-1] = S[z[j-1]]
	return x


print(''.join(map(str, Y2)))
print(D2)
print(''.join(viterbi(O, S, P, Y2, Tm, Em)))
