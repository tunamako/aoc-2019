#from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

numbers = [(str(i)*2, str(i)*3) for i in range(10)]

def has_adj(s):
	for n in numbers:
		if n[0] in s and n[1] not in s:
			return True

	return False

def increases(string):
	i = 0
	while i < len(string) - 1:
		if string[i] > string[i+1]:
			return False
		i += 1
	return True

def part_one(_input):
    minimum, maximum = map(int, _input.split('-'))
    count = 0
    for i in range(minimum, maximum):
    	i = str(i)

    	if increases(i) and has_adj(i):
    		count += 1

    return count

def part_two(_input):
    pass


if __name__ == '__main__':
    #puzzle = Puzzle(year=2019, day=4)
    _input = "100000000-1000000000"
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    #print(part_two(_input))

    cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
