def viterbi(S, P, Y, Tm, Em):
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
