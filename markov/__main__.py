import sys
from forward_backward import *
from viterbi import *


O = [1, 2, 3, 4, 5, 6]
S = ['F', 'L']
P = [0.95, 0.05]
Tm = [
	[0.95, 0.05],
	[0.1, 0.9]
]
Em = [
	[1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
	[0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
]

if len(sys.argv) < 2:
	exit()
with open(sys.argv[1]) as input:
	lines = input.readlines()
	lines[0] = lines[0].strip()
	print('Rolls:     ' + lines[0])
	print('Die:       ' + lines[1])
	observations = [int(i) for i in lines[0]]
	print('Viterbi:   ' + ''.join(viterbi(S, P, observations, Tm, Em)))
	print('Posterior: ' + ''.join(forward_backward(observations, S, P, Tm, Em)))
