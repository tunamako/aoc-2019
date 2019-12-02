from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


def part_one(_input):
	_input = _input.copy()
	for i in range(0, len(_input), 4):
		in_A, in_B, out =  _input[i+1:i + 4]

		if _input[i] == 1:
			_input[out] = _input[in_A] + _input[in_B]
		elif _input[i] == 2:
			_input[out] = _input[in_A] * _input[in_B]
		elif _input[i] == 99:
			return _input[0]


def part_two(_input):
	for noun in range(1, 99):
		for verb in range(1, 99):
			_input[1] = noun
			_input[2] = verb

			if part_one(_input) == 19690720:
				return 100 * noun + verb


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=2)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()
    _input[1] = 12
    _input[2] = 2

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
