import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np
from advent_machine import AdventMachine, Paintbot
from pprint import pprint

Point = namedtuple("Point", ['x', 'y'])

def part_one(_input):
    machine = AdventMachine(_input, return_output=True)
    scaffolds = ''.join(list(map(chr, machine.execute())))

    scaffolds = [list(row) for row in scaffolds.split('\n')][:-2]
    scaffolds = np.swapaxes(np.array(scaffolds), 0, 1)

    total = 0
    for p in np.argwhere(scaffolds == '#'):
        try:
            if (scaffolds[p[0] + 1][p[1]] == '#' and \
                scaffolds[p[0] - 1][p[1]] == '#' and \
                scaffolds[p[0]][p[1] + 1] == '#' and \
                scaffolds[p[0]][p[1] - 1] == '#'):

                total += p[0] * p[1]
        except IndexError:
            pass

    return total

def part_two(_input):
    _input[0] = 2
    machine = AdventMachine(_input, return_output=True)

    movements = [
        ['A',',','B',',','A',',','C',',','A',',','B',',','C',',','A',',','B',',','C','\n'],
        ['R',',','1','2',',','R',',','4',',','R',',','1','0',',','R',',','1','2','\n'],
        ['R',',','6',',','L',',','8',',','R',',','1','0','\n'],
        ['L',',','8',',','R',',','4',',','R',',','4',',','R',',','6','\n'],
        ['n',',','\n']
    ]

    for m in movements:
        for c in m:
            machine.execute(ord(c))

    return machine.output[-1]

if __name__ == '__main__':
    #puzzle = Puzzle(year=2019, day=17)
    _input = list(map(int, open("input").readline().split(',')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
