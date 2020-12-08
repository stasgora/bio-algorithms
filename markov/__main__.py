import getopt
import sys
from forward_backward import *
from viterbi import *


O = [1, 2, 3, 4, 5, 6]
S = ['F', 'L']


def parse_args():
	probabilities_file = None
	rolls_file = None
	optlist, args = getopt.getopt(sys.argv[1:], 'p:o:')
	for option, val in optlist:
		if option == '-p':
			probabilities_file = val
		elif option == '-o':
			rolls_file = val

	if probabilities_file is None:
		print('-p argument is required')
		exit()
	return probabilities_file, rolls_file


def parse_probabilities(file):
	with open(file) as prob_file:
		lines = prob_file.read().splitlines()
		P = list(map(float, lines[0].split(' ')))
		Tm = []
		Em = []
		for i in range(2):
			Tm.append(list(map(float, lines[1 + i].split(' '))))
		for i in range(2):
			Em.append(list(map(float, lines[3 + i].split(' '))))
		return P, Tm, Em


probabilities_file, rolls_file = parse_args()
P, Tm, Em = parse_probabilities(probabilities_file)
with open(rolls_file) as input:
	lines = input.read().splitlines()
	# generate if not given
	print('Rolls:     ' + lines[0])
	print('Die:       ' + lines[1])
	observations = [int(i) for i in lines[0]]
	print('Viterbi:   ' + ''.join(viterbi(S, P, observations, Tm, Em)))
	print('Posterior: ' + ''.join(forward_backward(observations, S, P, Tm, Em)))
