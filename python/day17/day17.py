from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

from advent_machine import AdventMachine, Paintbot


def part_one(_input):
    machine = AdventMachine(_input, return_output=True)

    scaffolds = list(map(chr, machine.execute()))
    print(','.join(scaffolds))

def part_two(_input):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=17)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
