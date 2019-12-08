from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


def get_layers(data):
	layers = []
	for i in range(0, len(_input), 25 * 6):
		layers.append(_input[i:i+25 * 6])
	return layers

def part_one(_input):
	layers = get_layers(_input)
	layer_fewest = None

	for i, l in enumerate(layers):
		if layer_fewest is None or l.count(0) < layer_fewest[1]:
			layer_fewest = (i, l.count(0))

	return layers[layer_fewest[0]].count(1) * layers[layer_fewest[0]].count(2)

def part_two(_input):
    layers = get_layers(_input)
    final = []
    for pix in range(len(layers[0])):
    	if all([l[pix] == 2 for l in layers]):
    		final.append(' ')
    	else:
    		final.append('x')
    	#if len(final) <= pix:


    for i in range(0, 25*6, 25):
    	print(''.join(map(str, final[i:i+25])))

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=8)
    _input = list(map(int, puzzle.input_data))
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
