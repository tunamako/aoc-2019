from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


def part_one(_input):
    total = 0
    for mass in _input:
        total += mass//3 - 2
    return total


def part_two(_input):
    total = 0
    for mass in _input:
        while (mass := mass//3 - 2) > 0:
            total += mass
    return total


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=1)
    _input = puzzle.input_data.split('\n')
    #_input = open('bigboy').readlines()

    _input = [int(line) for line in _input]

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
