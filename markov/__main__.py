import getopt
import random
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


def generate_rolls():
	lines = ['', '']
	state = 0
	if random.random() < P[1]:
		state = 1
	for i in range(60):
		switched_state = (state + 1) % 2
		if i > 0 and random.random() < Tm[state][switched_state]:
			state = switched_state
		lines[0] += str(random.choices(list(range(1, 7)), Em[state])[0])
		lines[1] += 'F' if state == 0 else 'L'
	return lines


probabilities_file, rolls_file = parse_args()
P, Tm, Em = parse_probabilities(probabilities_file)
if rolls_file is None:
	lines = generate_rolls()
else:
	with open(rolls_file) as input:
		lines = input.read().splitlines()

print('Rolls:     ' + lines[0])
print('Die:       ' + lines[1])
observations = [int(i) for i in lines[0]]
viter = viterbi(S, P, observations, Tm, Em)
forw_back = forward_backward(observations, S, P, Tm, Em)
percent = lambda obs: str(round(sum([obs[i] == lines[1][i] for i in range(len(observations))]) / len(observations) * 100, 2))
print('Viterbi:   ' + ''.join(viter) + ' (' + percent(viter) + '%)')
print('Posterior: ' + ''.join(forw_back) + ' (' + percent(forw_back) + '%)')
