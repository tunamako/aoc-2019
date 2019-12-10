from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

I_WIDTH = 46
I_HEIGHT = 36
LAYER_LEN = I_HEIGHT * I_WIDTH
BLACK = 0
WHITE = 1
TRANSPARENT = 2

def get_layers(data):
	for i in range(0, len(_input), LAYER_LEN):
		yield _input[i : i + LAYER_LEN]

def part_one(_input):
	min_zero = min(get_layers(_input), key=lambda l: l.count(0))
	return min_zero.count(1) * min_zero.count(2)

def part_two(_input):
    layers = get_layers(_input)
    final = [None for x in range(LAYER_LEN)]

    for l in layers:
    	for pix in range(LAYER_LEN):
    		if final[pix] is not None or l[pix] == TRANSPARENT:
    			continue
    		else:
    			final[pix] = '*' if l[pix] else ' '

    out = ''
    for i in range(0, LAYER_LEN, I_WIDTH):
    	out += ''.join(final[i : i + I_WIDTH]) + '\n'

    return out

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=8)
    _input = list(map(int, puzzle.input_data))
    _input = list(map(int, open('big_boy.txt').readlines()[0]))

    #print(part_one(_input))
    print(part_two(_input))
